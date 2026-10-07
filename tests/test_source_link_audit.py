"""Offline tests of retrieval semantics; no live network in CI."""
import csv
import io
from pathlib import Path
import sys
import tempfile
import unittest
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from audit_source_links import check_url, classify_content, inventory, sync_register
import source_audit_summary
from export_web_data import build_web_payload
import shutil


class Response(io.BytesIO):
    status = 200

    def __init__(self, body=b'<title>Company</title>', url='https://company.test/', kind='text/html'):
        super().__init__(body)
        self.url = url
        self.headers = {'Content-Type': kind}

    def geturl(self):
        return self.url


class SourceLinkAuditTests(unittest.TestCase):
    def test_get_retrieval_and_redirect_are_not_claim_validation(self):
        requests = []
        def opener(request, timeout):
            requests.append(request.get_method())
            return Response(url='https://company.test/new')
        result = check_url('https://company.test/', opener=opener)
        self.assertEqual(requests, ['GET'])
        self.assertEqual(result['retrieval_status'], 'REDIRECT_OK')
        self.assertIn('require separate review', result['detail'])
        self.assertNotIn('reviewer', result)
        self.assertNotIn('proposed_value', result)

    def test_http_404_and_access_block_are_different(self):
        for code, expected in [(404, 'NOT_FOUND'), (410, 'NOT_FOUND'), (403, 'ACCESS_BLOCKED'), (429, 'ACCESS_BLOCKED')]:
            def opener(request, timeout):
                raise urllib.error.HTTPError(request.full_url, code, 'failure', {}, None)
            row = check_url('https://company.test/', opener=opener)
            self.assertEqual(row['retrieval_status'], expected)
            self.assertIn('no deployment inference', row['detail'])

    def test_timeout_retries_without_inventing_a_status_or_final_url(self):
        def opener(request, timeout):
            raise TimeoutError('timeout')
        row = check_url('https://company.test/', opener=opener)
        self.assertEqual(row['attempts'], 2)
        self.assertEqual(row['retrieval_status'], 'NETWORK_ERROR')
        self.assertEqual(row['http_status'], '')
        self.assertEqual(row['final_url'], '')

    def test_soft_404_and_challenge_pages_do_not_pass_http_200(self):
        for title, expected in [('404 Page not found', 'NOT_FOUND'), ('Just a moment...', 'ACCESS_BLOCKED'), ('Domain for sale', 'CONTENT_REVIEW_REQUIRED')]:
            status, _, _ = classify_content('https://a.test/', 'https://a.test/', 'text/html', f'<title>{title}</title>'.encode())
            self.assertEqual(status, expected)

    def test_pdf_redirect_to_homepage_is_not_document_verification(self):
        status, _, _ = classify_content('https://a.test/certificate.pdf', 'https://a.test/', 'text/html', b'<title>Welcome</title>')
        self.assertEqual(status, 'CONTENT_REVIEW_REQUIRED')
        status, _, _ = classify_content('https://a.test/certificate.pdf', 'https://a.test/certificate.pdf', 'application/pdf', b'%PDF-1.7')
        self.assertEqual(status, 'HTTP_OK')

    def test_inventory_deduplicates_and_keeps_ownership_and_markdown_delimiters(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir(); (root / 'evidence/companies/P01_company').mkdir(parents=True)
            with (root / 'evidence/source_register.csv').open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=['candidate_id', 'source_id', 'source_link'])
                writer.writeheader()
                writer.writerows([{'candidate_id': 'P01', 'source_id': 'S1', 'source_link': 'https://a.test/'},
                                  {'candidate_id': 'SYN001', 'source_id': '', 'source_link': 'https://example.invalid'}])
            (root / 'evidence/companies/P01_company/evidence.md').write_text('[Page](https://a.test/): fact')
            result = inventory(root)
            self.assertEqual(list(result), ['https://a.test/'])
            self.assertEqual(result['https://a.test/']['source_ids'], 'S1')
            self.assertIn('evidence.md', result['https://a.test/']['references'])

    def test_inventory_covers_every_sample_company_and_registered_source(self):
        found = inventory(ROOT)
        companies = {c for row in found.values() for c in row['company_ids'].split(' | ')}
        with (ROOT / 'data/company_intelligence.csv').open() as handle:
            self.assertTrue({r['company_id'] for r in csv.DictReader(handle)} <= companies)
        source_ids = {s for row in found.values() for s in row['source_ids'].split(' | ')}
        with (ROOT / 'evidence/source_register.csv').open() as handle:
            self.assertTrue({r['source_id'] for r in csv.DictReader(handle)} <= source_ids)

    def test_committed_audit_covers_every_url_and_investigates_every_failure(self):
        self.assertEqual(source_audit_summary.validate(ROOT), [])
        payload = source_audit_summary.build(ROOT)
        self.assertEqual(payload['checked_company_count'], 100)
        self.assertEqual(payload['sample_company_count'], 100)
        self.assertTrue(all(r['audited_url_count'] > 0 for r in payload['companies']))
        self.assertEqual(payload['human_review_status'], 'PENDING')
        for case in payload['recovery_cases']:
            self.assertEqual(case['reviewer'], '')
            self.assertEqual(case['review_date'], '')
        self.assertTrue(any(r['has_coding_assessment'] == 'YES' for r in payload['companies']))
        self.assertTrue(all(r['has_coding_assessment'] == 'YES' for r in payload['companies']))

    def test_incomplete_audit_and_foreign_recovery_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'data', root / 'data')
            shutil.copytree(ROOT / 'evidence', root / 'evidence')
            p = root / 'evidence/source_link_audit.csv'
            with p.open() as f: rows = list(csv.DictReader(f))
            with p.open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows[1:])
            self.assertTrue(any('Uninspected' in e for e in source_audit_summary.validate(root)))
            self.assertLess(source_audit_summary.build(root)['checked_company_count'], 100)
            p = root / 'evidence/source_recovery.csv'
            with p.open() as f: rows = list(csv.DictReader(f))
            rows[0]['replacement_source_ids'] = 'S-P04-01'
            with p.open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
            self.assertTrue(any('Foreign' in e for e in source_audit_summary.validate(root)))

    def test_status_sync_preserves_scope_validity_review_and_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / 'evidence').mkdir()
            p = root / 'evidence/source_register.csv'
            fields = ['source_id', 'source_link', 'final_url', 'link_check_status', 'link_check_date', 'review_status', 'evidence_fact']
            original = [dict(source_id=str(i), source_link=f'https://a.test/{i}', final_url='',
                             link_check_status=status, link_check_date='2020-01-01', review_status='PENDING', evidence_fact='UNKNOWN')
                        for i, status in enumerate(['CONTENT_REVIEW_REQUIRED', 'VERIFIED_EXPIRED', 'VERIFIED'])]
            with p.open('w', newline='') as f:
                w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(original)
            audit = [dict(url=r['source_link'], final_url=r['source_link'], checked_at='2026-10-06T12:00:00+00:00',
                          retrieval_status='NOT_FOUND' if i == 2 else 'HTTP_OK') for i, r in enumerate(original)]
            sync_register(root, audit)
            with p.open() as f: changed = list(csv.DictReader(f))
            self.assertEqual([r['link_check_status'] for r in changed], ['CONTENT_REVIEW_REQUIRED', 'VERIFIED_EXPIRED', 'NOT_FOUND'])
            self.assertTrue(all(r['review_status'] == 'PENDING' and r['evidence_fact'] == 'UNKNOWN' for r in changed))
            audit[0]['retrieval_status'] = 'NOT_FOUND'
            sync_register(root, audit)
            audit[0]['retrieval_status'] = 'HTTP_OK'
            sync_register(root, audit)
            with p.open() as f: changed = list(csv.DictReader(f))
            self.assertEqual(changed[0]['link_check_status'], 'CONTENT_REVIEW_REQUIRED')
            audit[1]['retrieval_status'] = 'NOT_FOUND'
            sync_register(root, audit)
            audit[1]['retrieval_status'] = 'HTTP_OK'
            sync_register(root, audit)
            with p.open() as f: changed = list(csv.DictReader(f))
            self.assertEqual(changed[1]['link_check_status'], 'VERIFIED_EXPIRED')
            frozen = p.read_bytes()
            with self.assertRaises(ValueError): sync_register(root, audit[:1])
            self.assertEqual(p.read_bytes(), frozen)

    def test_brand_holder_is_not_the_production_entity_or_current_emas_proof(self):
        summary = source_audit_summary.build(ROOT)
        cases = {(r['company_id'], r['original_url']): r for r in summary['recovery_cases']}
        case = cases['P107', 'https://www.dibbern.de/en/about-dibbern/manufactory/']
        self.assertEqual(case['resolution_status'], 'PARTIAL_REPLACEMENT')
        self.assertIn('operator attribution', case['remaining_gap'])
        with (ROOT / 'evidence/source_register.csv').open() as f: sources = {r['source_id']: r for r in csv.DictReader(f)}
        self.assertEqual(sources['S-P107-04']['link_check_status'], 'CONTENT_REVIEW_REQUIRED')
        self.assertEqual(sources['S-P107-03']['link_check_status'], 'VERIFIED')
        case = cases['P30', 'https://www.zoetler.de/download/zoetler-nachhaltigkeitsbericht_emas2023.pdf']
        self.assertEqual(case['resolution_status'], 'NO_EQUIVALENT_FOUND')
        self.assertIn('validity', case['remaining_gap'])

    def test_web_and_company_export_keep_availability_and_scope_separate(self):
        payload = build_web_payload(ROOT)
        summary = payload['source_audit_summary']
        self.assertEqual(summary, source_audit_summary.build(ROOT))
        with (ROOT / 'outputs/source_audit_by_company.csv').open() as f: exported = list(csv.DictReader(f))
        self.assertEqual(len(exported), 100)
        for row, live in zip(exported, summary['companies']):
            self.assertEqual(row, {k: str(v) for k, v in live.items()})
        for company in payload['companies']:
            self.assertEqual(company['source_audit']['audit_status'], 'CHECKED')
            for source in company['sources']:
                self.assertNotEqual(source['retrieval_status'], 'NOT_CHECKED')
                self.assertTrue(source['link_check_date'])
