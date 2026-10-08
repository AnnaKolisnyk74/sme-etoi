"""Validate source-backed proposal checks separately from personal approval."""
from __future__ import annotations

import csv
import re
from datetime import date, datetime
from pathlib import Path


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8-sig') as handle:
        return list(csv.DictReader(handle))


def ids(value: str) -> set[str]:
    return {s.strip() for s in value.split('|') if s.strip()}


def validate(proposals: list[dict[str, str]], root: Path) -> list[str]:
    """Fail closed on missing, mismatched or falsely attributed check records."""
    errors = []
    records = rows(root / 'evidence/score_proposal_checks.csv')
    source_checks = rows(root / 'evidence/proposal_source_checks.csv')
    sources = {r['source_id']: r for r in rows(root / 'evidence/source_register.csv')}
    checked = {(r['company_id'], r['score_field']): r for r in records}
    bodies = {r['source_id']: r for r in source_checks}
    if len(checked) != len(records):
        errors.append('Duplicate proposal check')
    if len(bodies) != len(source_checks):
        errors.append('Duplicate source-content check')
    baseline = rows(root / 'data/history/score_coding_proposals_before_recheck_20261007.csv')
    original = {(r['company_id'], r['score_field']): r for r in baseline}
    original_numeric = {key for key, row in original.items() if row['proposed_value']}
    additions = {key for key in checked if key not in original_numeric}
    if records and (not original_numeric.issubset(checked)
                    or not set(checked).issubset(original)):
        errors.append('Proposal-check coverage differs from frozen numeric baseline')
    expected_sources = set().union(*(ids(r['original_source_ids']) | ids(r['checked_source_ids'])
                                     for r in records)) if records else set()
    if records and set(bodies) != expected_sources:
        errors.append('Source-content check coverage differs from proposal evidence trail')
    for sid, body in bodies.items():
        source = sources.get(sid, {})
        if (body.get('company_id') != source.get('candidate_id')
                or body.get('source_url') != source.get('source_link')
                or body.get('checked_by') != 'Codex'):
            errors.append(f'{sid}: source-check owner, URL or provenance mismatch')
        try:
            datetime.fromisoformat(body.get('checked_at', ''))
        except ValueError:
            errors.append(f'{sid}: invalid retrieval timestamp')
        if body.get('retrieval_status') == 'RETRIEVABLE' and (
                body.get('http_status') != '200'
                or body.get('content_kind') not in {'PDF', 'HTML', 'IMAGE'}
                or not re.fullmatch(r'[0-9a-f]{64}', body.get('content_sha256', ''))):
            errors.append(f'{sid}: retrievable body lacks valid provenance')
    for key, check in checked.items():
        if check.get('original_value') != original.get(key, {}).get('proposed_value'):
            errors.append(f'{key}: original value differs from frozen baseline')
        if check.get('original_source_ids') != original.get(key, {}).get('evidence_source_ids'):
            errors.append(f'{key}: original source trail differs from frozen baseline')
        if (check.get('checked_by') != 'Codex'
                or check.get('check_method') != 'PRIMARY_SOURCE_RECHECK_AND_ANCHOR_REVIEW'
                or check.get('final_score_approval') != 'NOT_GRANTED'):
            errors.append(f'{key}: invalid check provenance or approval claim')
        try:
            date.fromisoformat(check.get('checked_date', ''))
        except ValueError:
            errors.append(f'{key}: invalid check date')
        outcome = check.get('outcome')
        if outcome not in {'CONFIRMED', 'CORRECTED', 'NEEDS_RESEARCH', 'NEW_EVIDENCE'}:
            errors.append(f'{key}: invalid check outcome')
        if key in additions and (outcome != 'NEW_EVIDENCE'
                                or original.get(key, {}).get('proposal_status') != 'NEEDS_RESEARCH'
                                or original.get(key, {}).get('proposal_confidence') != 'UNKNOWN'
                                or check.get('original_confidence') != 'UNKNOWN'):
            errors.append(f'{key}: new evidence must originate from a frozen UNKNOWN field')
        if key in original_numeric and outcome == 'NEW_EVIDENCE':
            errors.append(f'{key}: original numeric recheck cannot become new evidence')
        if bool(check.get('checked_value')) != (outcome != 'NEEDS_RESEARCH'):
            errors.append(f'{key}: outcome/value disagreement')
        if not check.get('decision_note') or not check.get('checked_evidence_basis'):
            errors.append(f'{key}: missing substantive check rationale')
    for row in proposals:
        key = row['company_id'], row['score_field']
        status = row['proposal_status']
        check = checked.get(key)
        if status == 'CHECKED' and not check:
            errors.append(f'{key}: CHECKED requires a source-backed check record')
            continue
        if not check or status not in {'CHECKED', 'NEEDS_RESEARCH'}:
            continue
        expected_status = 'CHECKED' if check['checked_value'] else 'NEEDS_RESEARCH'
        if status != expected_status:
            errors.append(f'{key}: status differs from recorded outcome')
        for field, recorded in (
                ('proposed_value', 'checked_value'), ('proposal_confidence', 'checked_confidence'),
                ('evidence_basis', 'checked_evidence_basis')):
            if row.get(field) != check.get(recorded):
                errors.append(f'{key}: {field} differs from check record')
        if ids(row['evidence_source_ids']) != ids(check['checked_source_ids']):
            errors.append(f'{key}: checked sources differ from proposal')
        if status == 'CHECKED':
            if any(row.get(f) for f in ('reviewer', 'review_date', 'review_note')):
                errors.append(f'{key}: source check cannot claim personal approval')
            for sid in ids(row['evidence_source_ids']):
                body = bodies.get(sid, {})
                source = sources.get(sid, {})
                if (body.get('company_id') != row['company_id']
                        or body.get('source_url') != source.get('source_link')
                        or body.get('retrieval_status') != 'RETRIEVABLE'
                        or body.get('content_review_status') != 'RECHECKED'
                        or body.get('checked_by') != 'Codex'
                        or not re.fullmatch(r'[0-9a-f]{64}', body.get('content_sha256', ''))
                        or not body.get('scope_note') or not body.get('relevant_location')):
                    # An unavailable historical certificate may document a claim gap,
                    # but it must never authenticate a current certificate.
                    historical_gap = (row['score_field'] == 'management_gap_score'
                                      and row['proposed_value'] == '3'
                                      and body.get('content_review_status') == 'UNAVAILABLE'
                                      and body.get('company_id') == row['company_id']
                                      and body.get('source_url') == source.get('source_link')
                                      and body.get('retrieval_status') == 'RETRIEVAL_FAILED'
                                      and 'claim' in row['evidence_basis'].lower())
                    if not historical_gap:
                        errors.append(f'{key}: source {sid} has no reviewed attributable body')
    return errors


def summary(root: Path) -> dict:
    from collections import Counter
    checks = rows(root / 'evidence/score_proposal_checks.csv')
    sources = rows(root / 'evidence/proposal_source_checks.csv')
    return {
        'reviewed_proposal_count': len(checks),
        'outcome_counts': dict(sorted(Counter(r['outcome'] for r in checks).items())),
        'source_check_count': len(sources),
        'retrievable_source_count': sum(r['retrieval_status'] == 'RETRIEVABLE' for r in sources),
        'checked_date': max((r['checked_date'] for r in checks), default=''),
        'checked_by': 'Codex',
        'final_score_approval': 'NOT_GRANTED',
    }
