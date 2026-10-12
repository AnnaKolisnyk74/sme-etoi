"""Source-body coverage of the registered inventory, separate from score approval.

RECHECKED means the stated section was inspected within its documented scope.
CONTEXT_ONLY and UNAVAILABLE are assessed boundaries, never verified claims.
Downloaded third-party bodies remain temporary inspection material.
"""
from collections import Counter
from datetime import datetime
from pathlib import Path
import re

import decision_research
from source_audit_summary import rows

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {'RECHECKED', 'CONTEXT_ONLY', 'UNAVAILABLE'}


def new_checks(root=ROOT):
    result = {}
    for path in sorted((root / 'evidence').glob('source_content_checks_*.csv')):
        for row in rows(root, path.relative_to(root)):
            result[row['source_id']] = row
    return result


def checks(root=ROOT):
    result = {r['source_id']: r for r in rows(root, 'evidence/proposal_source_checks.csv')}
    result.update(decision_research.source_checks(root))
    result.update(new_checks(root))
    return result


def build(root=ROOT):
    sources = rows(root, 'evidence/source_register.csv')
    reviewed = checks(root)
    counts = Counter(reviewed.get(s['source_id'], {}).get('content_review_status')
                     or 'NOT_RECORDED' for s in sources)
    missing = [s['source_id'] for s in sources if s['source_id'] not in reviewed]
    return {
        'registered_source_count': len(sources),
        'assessed_source_count': sum(counts[s] for s in STATUSES),
        'rechecked_source_count': counts['RECHECKED'],
        'context_only_source_count': counts['CONTEXT_ONLY'],
        'unavailable_source_count': counts['UNAVAILABLE'],
        'missing_source_count': counts['NOT_RECORDED'],
        'missing_source_ids': missing,
        'coverage_status': 'COMPLETE' if sum(counts[s] for s in STATUSES) == len(sources) else 'INCOMPLETE',
        'status_counts': dict(sorted(counts.items())),
        'last_checked_at': max((r.get('checked_at', '') for r in reviewed.values()), default=''),
        'human_review_status': 'PENDING',
        'boundary_sources': [{
            'source_id': s['source_id'], 'company_id': s['candidate_id'],
            'document_title': s['document_title'], 'source_url': s['source_link'],
            'content_review_status': reviewed.get(s['source_id'], {}).get('content_review_status', 'NOT_RECORDED'),
            'scope_note': reviewed.get(s['source_id'], {}).get('scope_note', ''),
        } for s in sources if reviewed.get(s['source_id'], {}).get('content_review_status') != 'RECHECKED'],
    }


def validate(root=ROOT):
    sources = {r['source_id']: r for r in rows(root, 'evidence/source_register.csv')}
    errors, seen = [], set()
    for path in sorted((root / 'evidence').glob('source_content_checks_*.csv')):
        for r in rows(root, path.relative_to(root)):
            sid = r['source_id']
            if sid in seen:
                errors.append(f'Duplicate source-content check: {sid}')
            seen.add(sid)
            source = sources.get(sid, {})
            if not source or r['company_id'] != source.get('candidate_id') or r['source_url'] != source.get('source_link'):
                errors.append(f'Foreign or mismatched source-content check: {sid}')
            status = r.get('content_review_status')
            if status not in STATUSES:
                errors.append(f'Invalid source-content status: {sid}')
            if not r.get('scope_note') or not r.get('checked_fact') or not r.get('checked_by'):
                errors.append(f'Missing inspected scope/finding: {sid}')
            try:
                if datetime.fromisoformat(r['checked_at']).tzinfo is None:
                    raise ValueError('Timezone required')
            except (KeyError, ValueError):
                errors.append(f'Invalid source-content timestamp: {sid}')
            if status != 'UNAVAILABLE':
                if not re.fullmatch('[0-9a-f]{64}', r.get('content_sha256', '')) or not r.get('final_url') or not r.get('content_kind'):
                    errors.append(f'Missing retrieved-body fingerprint: {sid}')
                if r.get('retrieval_status') != 'RETRIEVABLE':
                    errors.append(f'Content review without readable body: {sid}')
            elif r.get('retrieval_status') == 'RETRIEVABLE':
                errors.append(f'Unavailable source claimed retrievable: {sid}')
            if status in {'CONTEXT_ONLY', 'UNAVAILABLE'} and not r.get('remaining_gap'):
                errors.append(f'Missing source boundary: {sid}')
            if r.get('reviewer') or r.get('review_date'):
                errors.append(f'AI source-content audit claims human review: {sid}')
    # A frozen selection prevents silently dropping one of the 231 outstanding records.
    selected = {r['source_id'] for r in rows(root, 'data/source_content_review_selection_20261012.csv')}
    for sid in sorted(selected - seen):
        errors.append(f'Selected source-content review missing: {sid}')
    for sid in sorted(seen - selected):
        errors.append(f'Unselected source-content check: {sid}')
    return errors
