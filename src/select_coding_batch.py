"""Freeze a ranked first-pass coding batch without approving or scoring companies."""
from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path
import tempfile

from company_work_priority import ROOT, read_csv
from run_pipeline import (
    build_outputs, build_score_readiness, build_score_work_queue,
    build_company_work_priority, run_pipeline,
)

SELECTION_FIELDS = [
    'batch_id', 'selected_date', 'selection_rank', 'company_id', 'legal_entity',
    'priority_version', 'evidence_confidence', 'process_confidence', 'qa_result',
    'verified_source_count', 'source_coverage', 'coverage_source_ids',
    'unassessed_field_count', 'expected_information_gain', 'priority_reason',
]


def select_batch(priority_rows: list[dict[str, str]], batch_id: str,
                 selected_date: str, size: int = 2) -> list[dict[str, str]]:
    if not batch_id.strip():
        raise ValueError('A nonempty batch ID is required')
    if date.fromisoformat(selected_date).isoformat() != selected_date:
        raise ValueError('Use an ISO YYYY-MM-DD selection date')
    if size < 1:
        raise ValueError('Batch size must be positive')
    ranked = sorted((r for r in priority_rows if r.get('workflow_action') == 'CODE_NOW'),
                    key=lambda r: int(r['coding_rank']))
    ranks = [int(r['coding_rank']) for r in ranked]
    if ranks != list(range(1, len(ranked) + 1)):
        raise ValueError('Coding ranks must be unique and dense')
    if any(r.get('qa_result') != 'PASS' or int(r.get('open_gate_tasks') or 0) for r in ranked):
        raise ValueError('Coding candidates must pass QA and have no eligibility gate')
    if len({r['company_id'] for r in ranked}) != len(ranked):
        raise ValueError('Duplicate company in ranking')
    if not ranked:
        raise ValueError('No company is ready for first-pass coding')
    return [{field: {'batch_id': batch_id.strip(), 'selected_date': selected_date,
                    'selection_rank': r['coding_rank']}.get(field, r.get(field, ''))
             for field in SELECTION_FIELDS} for r in ranked[:size]]


def append_selection(path: Path, selected: list[dict[str, str]]) -> None:
    if not selected or len({r['batch_id'] for r in selected}) != 1:
        raise ValueError('Write exactly one nonempty selection batch')
    existing = read_csv(path)
    batch_id = selected[0]['batch_id']
    frozen = [r for r in existing if r['batch_id'] == batch_id]
    if frozen:
        if frozen == selected:
            return  # Exact retries are byte-preserving, including after unrelated batches.
        raise ValueError(f'Batch {batch_id} is frozen; use a new ID instead of overwriting it')
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='',
                                         dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            writer = csv.DictWriter(handle, fieldnames=SELECTION_FIELDS, lineterminator='\n')
            writer.writeheader()
            writer.writerows(existing + selected)
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def run(root: Path, batch_id: str, selected_date: str, size: int = 2):
    # Do not select from a potentially stale generated CSV: validate and rebuild in memory.
    run_pipeline(root, write_outputs=False, include_reliability=False)
    companies, _, research = build_outputs(root)
    readiness = build_score_readiness(root, companies)
    work = build_score_work_queue(root, companies, readiness, research)
    priority = build_company_work_priority(work, root)
    selected = select_batch(priority, batch_id, selected_date, size)
    append_selection(root / 'data/coding_batch_selections.csv', selected)
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--batch-id', required=True)
    parser.add_argument('--selected-date', required=True)
    parser.add_argument('--size', type=int, default=2)
    args = parser.parse_args()
    try:
        selected = run(args.root, args.batch_id, args.selected_date, args.size)
    except ValueError as error:
        parser.exit(1, f'ERROR: {error}\n')
    print(f"Frozen {args.batch_id}: " + ', '.join(r['company_id'] for r in selected))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
