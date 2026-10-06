"""Offline completeness and recovery scope for public-source retrieval audits."""
from collections import Counter
from pathlib import Path
import csv

from audit_source_links import ROOT, csv_rows, inventory

RETRIEVABLE = {'HTTP_OK', 'REDIRECT_OK'}


def rows(root, path):
    file = root / path
    return csv_rows(file) if file.exists() else []


def validate(root: Path = ROOT):
    audit = rows(root, 'evidence/source_link_audit.csv')
    if not audit:
        return ['Public-source retrieval audit is missing']
    by_url = {r['url']: r for r in audit}
    errors = []
    if len(by_url) != len(audit):
        errors.append('Duplicate audit URL')
    for url in inventory(root):
        if url not in by_url:
            errors.append(f'Uninspected public evidence URL: {url}')
    recovery = rows(root, 'evidence/source_recovery.csv')
    source = {r['source_id']: r for r in rows(root, 'evidence/source_register.csv')}
    for row in recovery:
        if row.get('reviewer') or row.get('review_date'):
            errors.append('AI recovery cannot claim human review')
        if row['resolution_status'] != 'REPLACEMENT_FOUND' and not row['remaining_gap']:
            errors.append(f"Recovery gap missing for {row['original_url']}")
        for sid in row['replacement_source_ids'].split(' | '):
            if sid and (sid not in source or source[sid]['candidate_id'] != row['company_id']):
                errors.append(f'Foreign or missing recovery source: {sid}')
    for row in audit:
        if row['retrieval_status'] not in RETRIEVABLE:
            # Failed final targets differing only by a slash belong to the original case.
            if not any(r['original_url'].rstrip('/') == row['url'].rstrip('/') for r in recovery):
                errors.append(f"No recovery investigation for {row['url']}")
    for s in source.values():
        result = by_url.get(s['source_link'], {})
        if result.get('retrieval_status') not in RETRIEVABLE and s['link_check_status'] in {'VERIFIED', 'REDIRECT_VERIFIED'}:
            errors.append(f"Failed retrieval still marked verified: {s['source_id']}")
    return errors


def build(root: Path = ROOT):
    audit = rows(root, 'evidence/source_link_audit.csv')
    recovery = rows(root, 'evidence/source_recovery.csv')
    companies = rows(root, 'data/company_intelligence.csv')
    sources = rows(root, 'evidence/source_register.csv')
    proposals = rows(root, 'data/score_coding_proposals.csv')
    assessed = {r['company_id'] for r in proposals}
    required_by_company = {}
    for url, entry in inventory(root).items():
        for cid in entry['company_ids'].split(' | '):
            required_by_company.setdefault(cid, set()).add(url)
    checked_urls = {r['url'] for r in audit}
    company_rows = []
    for company in companies:
        cid = company['company_id']
        links = [r for r in audit if cid in r['company_ids'].split(' | ')]
        cases = [r for r in recovery if r['company_id'] == cid]
        owned = [r for r in sources if r['candidate_id'] == cid]
        company_rows.append({
            'company_id': cid, 'legal_entity': company['legal_entity'],
            'has_coding_assessment': 'YES' if cid in assessed else 'NO',
            'audited_url_count': len(links),
            'retrievable_url_count': sum(r['retrieval_status'] in RETRIEVABLE for r in links),
            'retrieval_issue_count': sum(r['retrieval_status'] not in RETRIEVABLE for r in links),
            'registered_source_count': len(owned),
            'scope_gap_count': sum(bool(r['remaining_gap']) and r['resolution_status'] != 'REPLACEMENT_FOUND' for r in cases),
            'recovery_case_count': len(cases),
            'audit_status': 'CHECKED' if links and required_by_company.get(cid, set()) <= checked_urls
                            else 'INCOMPLETE' if links else 'NOT_CHECKED',
            'last_checked_at': max((r['checked_at'] for r in links), default=''),
        })
    return {
        'checked_company_count': sum(r['audit_status'] == 'CHECKED' for r in company_rows),
        'sample_company_count': len(companies), 'registered_source_count': len(sources),
        'audited_url_count': len(audit),
        'retrievable_url_count': sum(r['retrieval_status'] in RETRIEVABLE for r in audit),
        'retrieval_status_counts': dict(sorted(Counter(r['retrieval_status'] for r in audit).items())),
        'recovery_status_counts': dict(sorted(Counter(r['resolution_status'] for r in recovery).items())),
        'last_checked_at': max((r['checked_at'] for r in audit), default=''),
        'human_review_status': 'PENDING',
        'companies': company_rows,
        'recovery_cases': recovery,
    }


def write_company_summary(root: Path = ROOT):
    company_rows = build(root)['companies']
    path = root / 'outputs/source_audit_by_company.csv'
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(company_rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(company_rows)
