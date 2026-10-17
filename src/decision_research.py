"""Source-backed decision profiles, separate from canonical or personal approval."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path


def rows(root, relative):
    path = root / relative
    if not path.exists():
        return []
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def batches(root: Path):
    """Read dated research blocks in order; retain their frozen evidence trails."""
    return [(p.stem.rsplit('_', 1)[1], json.loads(p.read_text()))
            for p in sorted((root / 'evidence').glob('decision_research_profiles_*.json'))]


def base_profiles(root: Path):
    latest = {}
    for _, block in batches(root):
        latest.update({p['company_id']: p for p in block})
    return list(latest.values())


def followup_batches(root: Path):
    """Revisit existing profiles without pretending they are new field attempts."""
    return [(p.stem.rsplit('_', 1)[1], json.loads(p.read_text()))
            for p in sorted((root / 'evidence').glob('decision_research_followups_*.json'))]


def profile_digest(profile):
    return hashlib.sha256(json.dumps(profile, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def profiles(root: Path):
    latest = {p['company_id']: p for p in base_profiles(root)}
    for _, block in followup_batches(root):
        latest.update({p['company_id']: p for p in block})
    return list(latest.values())


def source_checks(root: Path):
    latest = {}
    for path in sorted((root / 'evidence').glob('decision_source_checks_*.csv')):
        latest.update({r['source_id']: r for r in rows(root, str(path.relative_to(root)))})
    return latest


def field_attempts(root: Path):
    paths = [* (root / 'evidence').glob('field_research_deep_*.csv'),
             * (root / 'evidence').glob('field_research_followup_*.csv')]
    return [r for path in sorted(paths, key=lambda p: p.stem.rsplit('_', 1)[1])
            for r in rows(root, str(path.relative_to(root)))]


def checked_reassessments(root: Path):
    """Retain explicit before/after decisions when new sources change old anchors."""
    return [r for path in sorted((root / 'evidence').glob('checked_field_reassessments_*.csv'))
            for r in rows(root, str(path.relative_to(root)))]


def select_companies(queue, size=10, identity_blocks=()):
    """Use the first unique company by decision rank after upstream blocks."""
    blocked = set(identity_blocks) | {r['company_id'] for r in queue
                                     if r['missing_fact'] == 'sme_eligibility'}
    selected = []
    seen = set()
    for row in sorted(queue, key=lambda r: int(r['research_rank'])):
        cid = row['company_id']
        if cid in blocked or cid in seen:
            continue
        selected.append(row)
        seen.add(cid)
        if len(selected) == size:
            break
    return selected


def select_field_companies(queue, size=10, identity_blocks=()):
    """Continue exhausted opportunity research using the frozen field-work rank.

    research_rank is the existing selection-file column; queue_source explicitly
    identifies that its value is a work_rank, not an opportunity research rank.
    """
    blocked = set(identity_blocks) | {r['company_id'] for r in queue
                                     if r['task_status'] == 'OPEN_GATE'}
    selected, seen = [], set()
    for row in sorted(queue, key=lambda r: int(r['work_rank'])):
        cid = row['company_id']
        if (cid in blocked or cid in seen or row['task_status'] != 'RESEARCH_NEEDED'
                or not row['research_gap_fields']):
            continue
        selected.append({**row, 'research_rank': row['work_rank'],
                         'missing_fact': row['research_gap_fields'],
                         'queue_source': 'SCORE_WORK_QUEUE'})
        seen.add(cid)
        if len(selected) == size:
            break
    return selected


def validate(root: Path):
    data = profiles(root)
    if not data:
        return []
    errors = []
    previous = {p['company_id']: p for p in base_profiles(root)}
    for stamp, block in followup_batches(root):
        if len({p['company_id'] for p in block}) != len(block):
            errors.append(f'{stamp}: duplicate follow-up profile')
        for p in block:
            old = previous.get(p['company_id'])
            if (old is None or p.get('previous_profile_sha256') != profile_digest(old)
                    or p.get('workstream') != old.get('workstream')
                    or p.get('legal_entity') != old.get('legal_entity')
                    or p.get('checked_date', '') < old.get('checked_date', '')
                    or not p.get('followup_reason')):
                errors.append(f"{stamp}: invalid follow-up provenance for {p['company_id']}")
            previous[p['company_id']] = p
        fields = rows(root, f'evidence/field_research_followup_{stamp}.csv')
        scoped = {p['company_id']: p['field_research_scope'] for p in block
                  if p.get('field_research_scope')}
        if scoped or fields:
            baseline = rows(root, f'data/history/score_coding_proposals_before_followup_{stamp}.csv')
            expected = {(p['company_id'], p['score_field']) for p in baseline
                        if p['company_id'] in scoped and p['proposal_status'] == 'NEEDS_RESEARCH'}
            declared = {(cid, f) for cid, fs in scoped.items() for f in fs}
            actual = {(f['company_id'], f['score_field']) for f in fields}
            if (not baseline or expected != declared or expected != actual
                    or len(actual) != len(fields)
                    or sum(map(len, scoped.values())) != len(declared)):
                errors.append(f'{stamp}: follow-up field attempts differ from frozen gaps')
    sources = {s['source_id']: s for s in rows(root, 'evidence/source_register.csv')}
    bodies = source_checks(root)
    for p in data:
        cid = p['company_id']
        if p['checked_by'] != 'Codex' or p['final_score_approval'] != 'NOT_GRANTED':
            errors.append(f'{cid}: decision research cannot claim personal approval')
        if not p['finding'] or not p['next_action']:
            errors.append(f'{cid}: missing decision finding or next action')
        if not p['source_ids'] and not p['outcome'].startswith('SOURCE_ACCESS_'):
            errors.append(f'{cid}: supported finding requires attributable content')
        for sid in p['source_ids']:
            s, b = sources.get(sid, {}), bodies.get(sid, {})
            if (s.get('candidate_id') != cid or b.get('company_id') != cid
                    or s.get('source_link') != b.get('source_url')
                    or b.get('retrieval_status') != 'RETRIEVABLE'
                    or b.get('content_review_status') != 'RECHECKED'
                    or not re.fullmatch('[0-9a-f]{64}', b.get('content_sha256', ''))
                    or not b.get('relevant_location') or not b.get('scope_note')):
                errors.append(f'{cid}: source {sid} lacks a reviewed attributable body')
    current = {(p['company_id'], p['score_field']): p
               for p in rows(root, 'data/score_coding_proposals.csv')}
    reassessed = {}
    for r in checked_reassessments(root):
        key = r['company_id'], r['score_field']
        stamp = r['checked_date'].replace('-', '')
        baseline = {(p['company_id'], p['score_field']): p for p in rows(
            root, f'data/history/score_coding_proposals_before_deep_{stamp}.csv')}
        old, new = baseline.get(key, {}), current.get(key, {})
        if (r['checked_by'] != 'Codex' or r['final_score_approval'] != 'NOT_GRANTED'
                or old.get('proposal_status') != 'CHECKED'
                or new.get('proposal_status') != 'CHECKED'):
            errors.append(f'{key}: invalid checked-field reassessment provenance')
        for field, before, after in (
                ('proposed_value', 'previous_value', 'checked_value'),
                ('proposal_confidence', 'previous_confidence', 'checked_confidence'),
                ('evidence_source_ids', 'previous_source_ids', 'checked_source_ids'),
                ('evidence_basis', 'previous_evidence_basis', 'checked_evidence_basis')):
            if old.get(field) != r.get(before) or new.get(field) != r.get(after):
                errors.append(f'{key}: reassessment differs from frozen/current {field}')
        for sid in r['checked_source_ids'].split(' | '):
            if sources.get(sid, {}).get('candidate_id') != key[0] or sid not in bodies:
                errors.append(f'{key}: reassessment has foreign or unreviewed evidence {sid}')
        reassessed[key] = r
    prior_ids = {'P109', 'P110'}
    for stamp, block in batches(root):
        if len({p['company_id'] for p in block}) != len(block):
            errors.append(f'{stamp}: duplicate decision profile')
        selections = rows(root, f'data/decision_research_selections_{stamp}.csv')
        frozen = rows(root, f'data/history/research_queue_before_deep_{stamp}.csv')
        if not selections or not frozen:
            errors.append(f'{stamp}: missing frozen selection or queue')
        expected = select_companies(frozen, identity_blocks=prior_ids)
        field_queue = rows(root, f'data/history/score_work_queue_before_deep_{stamp}.csv')
        if field_queue:
            if expected:
                errors.append(f'{stamp}: field fallback requires exhausted opportunity queue')
            expected = select_field_companies(field_queue, identity_blocks=prior_ids)
            if any(s.get('queue_source') != 'SCORE_WORK_QUEUE' or s.get('selection_rule') !=
                   'EXHAUSTED_RESEARCH_QUEUE_THEN_FIRST_UNIQUE_BY_WORK_RANK' for s in selections):
                errors.append(f'{stamp}: field selection lacks explicit work-rank provenance')
        if [s['company_id'] for s in selections] != [s['company_id'] for s in expected]:
            errors.append(f'{stamp}: selection differs from frozen queue')
        technical = sorted((p for p in block if p['workstream'] == 'TECHNICAL'),
                           key=lambda p: p['selection_rank'])
        if [p['company_id'] for p in technical] != [s['company_id'] for s in selections]:
            errors.append(f'{stamp}: technical profiles differ from selection')
        for s, q in zip(selections, expected):
            if s['research_rank'] != q['research_rank']:
                errors.append(f"{s['company_id']}: frozen selection rank changed")
        baseline = rows(root, f'data/history/score_coding_proposals_before_deep_{stamp}.csv')
        fields = rows(root, f'evidence/field_research_deep_{stamp}.csv')
        expected_fields = {(p['company_id'], p['score_field']) for p in baseline
                           if p['company_id'] in {s['company_id'] for s in selections}
                           and p['proposal_status'] == 'NEEDS_RESEARCH'}
        actual_fields = {(p['company_id'], p['score_field']) for p in fields}
        if not baseline or actual_fields != expected_fields or len(fields) != len(actual_fields):
            errors.append(f'{stamp}: field attempts do not cover frozen gaps exactly once')
        for old in baseline:
            key = old['company_id'], old['score_field']
            if old['proposal_status'] == 'CHECKED' and current.get(key) != old:
                decision = reassessed.get(key, {})
                if decision.get('checked_date', '').replace('-', '') < stamp:
                    errors.append(f'{key}: checked baseline changed without a later reassessment')
        prior_ids.update(p['company_id'] for p in block)
    current = {(p['company_id'], p['score_field']): p
               for p in rows(root, 'data/score_coding_proposals.csv')}
    latest_fields = {(f['company_id'], f['score_field']): f for f in field_attempts(root)}
    for field in latest_fields.values():
        key = field['company_id'], field['score_field']
        p = current.get(key, {})
        for sid in (s.strip() for s in field['reviewed_source_ids'].split('|') if s.strip()):
            if sources.get(sid, {}).get('candidate_id') != field['company_id'] or sid not in bodies:
                errors.append(f'{key}: field attempt has foreign or unreviewed evidence {sid}')
        if field['outcome'] == 'NEW_EVIDENCE':
            if p.get('proposal_status') != 'CHECKED' or not p.get('proposed_value'):
                errors.append(f'{key}: new field evidence is not a checked proposal')
        elif (field['outcome'] != 'STILL_UNKNOWN' or not field['remaining_fact']
              or p.get('proposed_value') or p.get('proposal_confidence') != 'UNKNOWN'):
            errors.append(f'{key}: unresolved evidence became a number or lost its gap')
    return errors


def summary(root: Path):
    data = profiles(root)
    fields = field_attempts(root)
    followup_blocks = followup_batches(root)
    followups = [p for _, block in followup_blocks for p in block]
    blocks = []
    for stamp, block in batches(root):
        attempts = rows(root, f'evidence/field_research_deep_{stamp}.csv')
        corrections = rows(root, f'evidence/checked_field_reassessments_{stamp}.csv')
        blocks.append({'checked_date': max((p['checked_date'] for p in block), default=''),
                       'profile_count': len(block), 'field_attempt_count': len(attempts),
                       'new_checked_field_count': sum(f['outcome'] == 'NEW_EVIDENCE' for f in attempts),
                       'still_unknown_field_count': sum(f['outcome'] == 'STILL_UNKNOWN' for f in attempts),
                       'reassessed_checked_field_count': len(corrections)})
    return {
        'checked_date': max((p['checked_date'] for p in data), default=''),
        'profile_count': len(data),
        'technical_company_count': sum(p['workstream'] == 'TECHNICAL' for p in data),
        'eligibility_company_count': sum(p['workstream'] == 'ELIGIBILITY' for p in data),
        'identity_company_count': sum(p['workstream'] == 'IDENTITY' for p in data),
        'field_attempt_count': len(fields),
        'new_checked_field_count': sum(f['outcome'] == 'NEW_EVIDENCE' for f in fields),
        'still_unknown_field_count': sum(f['outcome'] == 'STILL_UNKNOWN' for f in fields),
        'reassessed_checked_field_count': len(checked_reassessments(root)),
        'followup_count': len(followups),
        'followup_company_count': len({p['company_id'] for p in followups}),
        'latest_followup': ({'checked_date': max(p['checked_date'] for p in followup_blocks[-1][1]),
                             'company_count': len(followup_blocks[-1][1]),
                             'field_attempt_count': len(rows(root, f'evidence/field_research_followup_{followup_blocks[-1][0]}.csv')),
                             'new_checked_field_count': sum(f['outcome'] == 'NEW_EVIDENCE' for f in rows(root, f'evidence/field_research_followup_{followup_blocks[-1][0]}.csv')),
                             'still_unknown_field_count': sum(f['outcome'] == 'STILL_UNKNOWN' for f in rows(root, f'evidence/field_research_followup_{followup_blocks[-1][0]}.csv')),
                             'entity_clarified_company_count': sum(
                                 p['outcome'] == 'ENTITY_IDENTIFIED_ASSET_SCOPE_OPEN'
                                 for p in followup_blocks[-1][1])}
                            if followup_blocks else {}),
        'profiles': data,
        'batches': blocks,
        'latest_batch': blocks[-1] if blocks else {},
    }
