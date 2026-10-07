# P25 — Scheplast GmbH

- Public brand: Scheplast
- Legal entity: Scheplast GmbH
- Manufacturing location: Schwendi
- Eligibility decision: INCLUDE (probable SME)
- Review state: RESEARCHED

## Evidence

- `S-P25-01` confirms the exact legal entity and owner management.
- `S-P25-02` retains the historical 2026-09-13 extraction of 50 employees,
  recycling and annual solar generation. Those figures were not reproduced on
  the current homepage and are blocked by CONTENT_REVIEW_REQUIRED. The legacy
  staff record is not newly confirmed; the undated process page says around 40.
- `S-P25-03` documents injection moulding. PV is not treated as evidence of
  battery storage, and no load-management deployment is inferred.
- `S-P25-04` is a direct ISO 14001 certificate, but it expired on 26 February
  2024. It remains VERIFIED_EXPIRED as historical evidence. The direct successor
  `S-P25-06` now establishes current ISO 14001 validity through 2027-02-26.

## Open checks

- Verify the financial threshold and resolve undated staff/machine-count
  inconsistencies; the ISO 14001 successor check is now complete.
- Research load profile, cooling and storage.


## Ranked first-pass follow-up — 2026-10-07

Batch NBCC-2026-10-07-01 was frozen from PR #39 main before source enrichment. Evidence/process B/B, QA PASS and PROCESS-only coverage yielded MEDIUM documentary information gain; this proxy does not predict numeric yield.

PV, waste heat and current environmental certificate: S-P25-05 documents own PV/self-consumption and waste-heat utilisation. S-P25-06 is the exact-holder direct current environmental certificate. S-P25-07 explicitly describes robots; its bioenergy/bio-refinery vision does not prove CHP deployment. Machine closing force is not temperature or power. Generic material knowledge, own PV and ISO 14001 cannot close thermal-electrification/storage gaps.

8 numeric fields await independent human review; 7 fields are NEEDS_RESEARCH with blank values and UNKNOWN confidence. No aggregate score is published.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- |
| temperature_fit_score | — | UNKNOWN | NEEDS_RESEARCH | S-P25-03 |
| process_electrification_score | — | UNKNOWN | NEEDS_RESEARCH | S-P25-03, S-P25-05, S-P25-07 |
| fossil_heat_displacement_score | — | UNKNOWN | NEEDS_RESEARCH | S-P25-05, S-P25-07 |
| motor_drive_score | 2 | C | AWAITING_HUMAN_REVIEW | S-P25-07 |
| power_conversion_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P25-05 |
| automation_control_score | 1 | C | AWAITING_HUMAN_REVIEW | S-P25-07 |
| scheduling_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P25-03, S-P25-07 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P25-05 |
| incremental_load_score | — | UNKNOWN | NEEDS_RESEARCH | S-P25-03, S-P25-05 |
| power_quality_score | 1 | C | AWAITING_HUMAN_REVIEW | S-P25-05 |
| onsite_integration_score | 2 | B | AWAITING_HUMAN_REVIEW | S-P25-05 |
| measures_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P25-05 |
| management_gap_score | 2 | B | AWAITING_HUMAN_REVIEW | S-P25-06 |
| targets_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P25-05, S-P25-07 |
| investment_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P25-05, S-P25-06, S-P25-07 |

Gap details and rationale are recorded field by field in data/score_coding_proposals.csv. The investment window is 2021-10-07 through 2026-10-07. Company pages, process/energy statements, direct certificate and exact-name public energy/target/certification searches were checked on 2026-10-07. No current extra certificate or deployment was inferred from a missing search result. Canonical deployment columns, confidence grades, numeric scoring inputs and human review records are unchanged; the Scheplast ISO 14001 successor is a factual certificate correction only.
