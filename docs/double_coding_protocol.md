# Independent double-coding protocol

## Purpose

The second reviewer checks the complete 100-company sample independently after
all provisional records have been assembled. The goal is to
measure whether another person reaches the same categorical decisions from the
registered public evidence. This is a research-validity check, not a request to
make the existing coding look consistent.

## Blind-review sequence

1. Create a private working copy of `data/pilot_double_code.csv`.
2. Filter `data/pilot_review_sources.csv` by the value in
   `source_manifest_filter` and review the linked original sources. The neutral
   manifest deliberately excludes earlier evidence interpretations.
3. Do not open company dossiers, `data/company_intelligence.csv`,
   `data/company_process_map.csv`, `evidence/qa_review.csv` or generated
   opportunity outputs before finishing the row.
4. Enter the reviewer name and ISO review date (`YYYY-MM-DD`).
5. Code every required field using only the allowed values below.
6. Record the source IDs actually checked, separated by ` | `.
7. Set `review_status` to `COMPLETE` only when every required field is coded.
8. Run `python src/inter_rater_reliability.py` after saving the completed rows.

Do not resolve disagreements by editing the independent coding. The generated
`outputs/double_code_conflicts.csv` is the adjudication queue. Canonical data
changes only after the two coders document why one interpretation is better.

## Allowed values

| Field | Values |
|---|---|
| `review_status` | `PENDING`, `COMPLETE` |
| `entity_check` | `CONFIRMED`, `CORRECTION_REQUIRED`, `UNKNOWN` |
| `sme_status` | `eligible`, `probable`, `ineligible`, `UNKNOWN` |
| `group_check` | the canonical group categories, including `independent`, `probable_independent`, `family_owned`, `small_group`, `partner_or_linked_sme`, `linked_enterprise_check`, `foundation_owned`, `unknown`, or reviewer value `UNKNOWN` |
| `process_ids` | one or more IDs from `data/process_library.csv`, separated by `|` |
| ISO/EMAS status | `VALID`, `EXPIRED`, `DOCUMENT_FOUND_VALIDITY_UNCLEAR`, `CLAIM_ONLY`, `NOT_FOUND_AFTER_CHECK`, `UNKNOWN` |
| deployment fields | `YES`, `UNKNOWN` |
| `evidence_confidence` | `A`, `B`, `C`, `UNKNOWN` |

`UNKNOWN` must remain available whenever the public evidence does not support a
decision. `NOT_FOUND_AFTER_CHECK` means only that the defined public search did
not locate evidence. It never means that a certification or deployment does
not exist.

## Interpretation

The script reports exact agreement and Cohen's kappa separately for each field.
Kappa is intentionally not pooled across fields because their category systems
are different. A field containing only one observed category receives
`NOT_DEFINED_SINGLE_CATEGORY`; its percentage agreement remains visible.

All disagreements require adjudication. A high overall percentage is not a
reason to ignore a small number of commercially important conflicts.
