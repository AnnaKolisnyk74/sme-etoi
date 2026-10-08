"""Audit public evidence URLs with GET requests; retrieval is not human review.

Network checks are opt-in CLI work, never a dependency of the offline pipeline.
Full downloaded pages are temporary inspection material, not repository artifacts.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import socket
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['url', 'company_ids', 'source_ids', 'references', 'checked_at',
          'retrieval_status', 'http_status', 'final_url', 'content_type',
          'page_title', 'sample_sha256', 'attempts', 'detail']
USER_AGENT = 'Mozilla/5.0 (compatible; SME-ETOI-Public-Source-Audit/1.0)'


def csv_rows(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def inventory(root: Path = ROOT):
    """Include all candidate evidence, even excluded candidates; omit synthetic demos."""
    found = {}

    def add(url, company, reference, source=''):
        if not re.fullmatch(r'P\d+', company):
            return
        item = found.setdefault(url, {'company_ids': set(), 'source_ids': set(), 'references': set()})
        item['company_ids'].add(company)
        item['references'].add(reference)
        if source:
            item['source_ids'].add(source)

    for folder in ['data', 'evidence']:
        for path in sorted((root / folder).glob('*.csv')):
            if path.name.startswith('source_link_audit') or path.name.startswith('source_recovery'):
                continue
            for row in csv_rows(path):
                company = row.get('candidate_id') or row.get('company_id', '')
                for field, value in row.items():
                    # Search discoveries are a candidate pool, not inspected evidence.
                    # Actual retrievals enter inventory through their source_url ledger.
                    if path.name.startswith('research_queries_') and field == 'discovered_urls':
                        continue
                    # Explicit URL fields retain valid parentheses; prose URLs stop at Markdown delimiters.
                    if field in {'source_link', 'final_url', 'website', 'source_url', 'process_evidence_url',
                                 'direct_certificate_url', 'certificate_index_url'}:
                        urls = [v.strip() for v in (value or '').split('|') if v.strip().startswith(('https://', 'http://'))]
                    else:
                        urls = [u.rstrip('.,;') for u in re.findall(r'https?://[^\s|<>`)]+', value or '')]
                    for url in urls:
                        add(url, company, f'{path.relative_to(root)}:{field}', row.get('source_id', ''))
    for path in sorted((root / 'evidence/companies').glob('*/evidence.md')):
        company = path.parent.name.split('_')[0]
        for url in re.findall(r'https?://[^\s<>`)]+', path.read_text(encoding='utf-8')):
            add(url.rstrip('.,;'), company, str(path.relative_to(root)))
    return {url: {k: ' | '.join(sorted(values)) for k, values in item.items()}
            for url, item in sorted(found.items())}


def classify_content(url, final_url, content_type, body):
    text = body.decode('utf-8', errors='replace')
    match = re.search(r'<title[^>]*>(.*?)</title>', text, re.I | re.S)
    title = re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', match.group(1))).strip()[:240] if match else ''
    if re.search(r'(?i)(just a moment|access denied|attention required|robot check|verify you are human)', title):
        return 'ACCESS_BLOCKED', title, 'HTTP success contains an access challenge; evidence not inspected.'
    if re.search(r'(?i)(\b404\b|page not found|seite nicht gefunden|error 404)', title):
        return 'NOT_FOUND', title, 'HTTP success contains a missing-page title (soft 404).'
    if re.search(r'(?i)(domain (is )?for sale|domain kaufen|buy this domain|website coming soon)', title):
        return 'CONTENT_REVIEW_REQUIRED', title, 'Possible parked or placeholder page; factual relevance unresolved.'
    if urllib.parse.urlsplit(url).path.lower().endswith('.pdf') and not body.lstrip().startswith(b'%PDF-'):
        return 'CONTENT_REVIEW_REQUIRED', title, 'Requested PDF did not return a PDF; replacement document unresolved.'
    if not body:
        return 'CONTENT_REVIEW_REQUIRED', title, 'Empty response body.'
    status = 'REDIRECT_OK' if final_url != url else 'HTTP_OK'
    return status, title, 'GET retrieval succeeded; entity, claim, currency and certificate validity require separate review.'


def check_url(url, *, timeout=15, opener=urllib.request.urlopen, cache_dir=None):
    row = dict(url=url, checked_at=datetime.now(timezone.utc).isoformat(timespec='seconds'),
               retrieval_status='NETWORK_ERROR', http_status='', final_url='', content_type='',
               page_title='', sample_sha256='', attempts=0, detail='')
    for attempt in range(1, 3):
        row['attempts'] = attempt
        try:
            request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept': '*/*'})
            with opener(request, timeout=timeout) as response:
                body = response.read(524288)
                row.update(http_status=str(response.status), final_url=response.geturl(),
                           content_type=response.headers.get('Content-Type', ''),
                           sample_sha256=hashlib.sha256(body).hexdigest())
                status, title, detail = classify_content(url, row['final_url'], row['content_type'], body)
                row.update(retrieval_status=status, page_title=title, detail=detail)
                if cache_dir:
                    cache_dir.mkdir(parents=True, exist_ok=True)
                    (cache_dir / (hashlib.sha256(url.encode()).hexdigest() + '.body')).write_bytes(body)
                return row
        except urllib.error.HTTPError as error:
            row.update(http_status=str(error.code), final_url=error.geturl(),
                       retrieval_status='NOT_FOUND' if error.code in {404, 410} else
                       'ACCESS_BLOCKED' if error.code in {401, 403, 429} else 'HTTP_ERROR',
                       detail=f'HTTP {error.code}; availability only, no deployment inference.')
            if error.code not in {429, 500, 502, 503, 504}:
                return row
        except (urllib.error.URLError, TimeoutError, socket.timeout, OSError, ValueError) as error:
            row.update(retrieval_status='NETWORK_ERROR', detail=f'{type(error).__name__}: {error}'[:500])
    return row


def audit(root=ROOT, workers=12, timeout=15, cache_dir=None):
    urls = inventory(root)
    rows = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(check_url, url, timeout=timeout, cache_dir=cache_dir): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            rows.append({**future.result(), **urls[url]})
            if len(rows) % 25 == 0:
                print(f'Checked {len(rows)}/{len(urls)} URLs', flush=True)
    rows.sort(key=lambda r: r['url'])
    path = root / 'evidence/source_link_audit.csv'
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    from collections import Counter
    print(json.dumps(dict(Counter(r['retrieval_status'] for r in rows)), sort_keys=True), flush=True)
    return rows


def sync_register(root, audit_rows):
    """Update retrieval metadata only. A content-scope blocker needs separate review."""
    results = {r['url']: r for r in audit_rows}
    path = root / 'evidence/source_register.csv'
    sources = csv_rows(path)
    if any(s['source_link'] not in results for s in sources):
        raise ValueError('Cannot synchronize an incomplete source-register audit')
    status_map = {'HTTP_OK': 'VERIFIED', 'REDIRECT_OK': 'REDIRECT_VERIFIED',
                  'NOT_FOUND': 'NOT_FOUND', 'ACCESS_BLOCKED': 'EXISTS_ACCESS_CHALLENGE',
                  'HTTP_ERROR': 'CHECK_INCONCLUSIVE', 'NETWORK_ERROR': 'CHECK_INCONCLUSIVE',
                  'CONTENT_REVIEW_REQUIRED': 'CONTENT_REVIEW_REQUIRED'}
    for source in sources:
        result = results[source['source_link']]
        old = source['link_check_status']
        retrieved = result['retrieval_status'] in {'HTTP_OK', 'REDIRECT_OK'}
        if not (old in {'CONTENT_REVIEW_REQUIRED', 'VERIFIED_EXPIRED'} or retrieved and old == 'VERIFIED_INDEX'):
            source['link_check_status'] = status_map[result['retrieval_status']]
        source['link_check_date'] = result['checked_at'][:10]
        if result['final_url']:
            source['final_url'] = result['final_url']
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(sources[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(sources)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--workers', type=int, default=12)
    parser.add_argument('--timeout', type=float, default=15)
    parser.add_argument('--cache-dir', type=Path)
    parser.add_argument('--sync-register', action='store_true', help='Synchronize retrieval metadata only; preserve content blockers and validity caveats')
    args = parser.parse_args()
    if args.workers < 1 or args.timeout <= 0:
        parser.error('Workers and timeout must be positive')
    checked = audit(args.root, args.workers, args.timeout, args.cache_dir)
    if args.sync_register:
        sync_register(args.root, checked)
