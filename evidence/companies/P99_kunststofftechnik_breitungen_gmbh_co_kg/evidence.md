# P99 — Kunststofftechnik Breitungen GmbH & Co. KG

## Provisional inclusion

- Process stratum: `plastics_processing`
- Process mapping: `PR001` — plastic injection moulding; toolmaking; finishing and assembly
- SME status: `probable`; final financial and linked-enterprise review pending
- Independent human review: `PENDING`

## Sources checked

1. [Legal entity / company information](https://www.kt-breitungen.de/)
2. [Production and process scope](https://www.kt-breitungen.de/)

## Coding note

The public sources support the legal-entity and process mapping used for provisional sample assembly. They do not establish actual energy consumption, buying intent, grid capacity or deployment of a specific energy solution. Certificate searches are recorded as `NOT_FOUND_AFTER_CHECK`; this means only that no direct public evidence was located in the defined check, not that a certificate or deployment does not exist.


## Completion to 100-company field assessment — 2026-10-07

NBCC-2026-10-07-07: selection frozen before enrichment. Final16 ranked eligible coding candidates; rank is documentary information gain, not score.

- S-P99-03: https://www.kt-breitungen.de/maschinenpark/ — Owner lists nine Arburg injection machines plus coating/printing. kN closing force and shot mass are not motor power; 520E model designation alone does not verify drive technology or machine commissioning.
- S-P99-04: https://www.kt-breitungen.de/qualitaet/ — Owner quality page checked. Quality certification and surface finishing are not evidence of ISO 50001/14001, energy equipment, measured savings or recent energy commissioning.

All15 fields assessed: 1 numeric proposals awaiting actual human review; 14 blank NEEDS_RESEARCH fields with UNKNOWN confidence. No aggregate score.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- | --- |
| temperature_fit_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| process_electrification_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| fossil_heat_displacement_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| motor_drive_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P99-03 |
| power_conversion_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| automation_control_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| scheduling_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| incremental_load_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| power_quality_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| onsite_integration_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| measures_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| management_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| targets_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |
| investment_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P99-03, S-P99-04 |

Exact field rationales/missing facts: data/score_coding_proposals.csv. Certificate bodies and relevant pages visually checked; holder, period, site and product-versus-process scope separated. Frömgen initial HTTP466 subsequently recovered through live HTTP200 primary-body retrieval; owned machining scope reviewed separately. Investment window2021-10-07 to2026-10-07. Previous proposals, canonical numeric/deployment/staff/confidence and actual human-review records preserved. AI first pass is not Anna human review.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| motor_drive_score | 5 | 5 | Geprüft | S-P99-03 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.


## Offene Felder: Recherche 2026-10-08

Prüfer: Codex. Status **Geprüft** bedeutet Quellen- und Ankerprüfung; persönliche Freigabe bleibt separat.

| Feld | Ergebnis | Belege |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | S-P99-03 |
| process_electrification_score | Weiter offen / UNKNOWN | S-P99-03 |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | S-P99-03 |
| power_conversion_score | Weiter offen / UNKNOWN | S-P99-03 |
| automation_control_score | Weiter offen / UNKNOWN | S-P99-03 |
| scheduling_flex_score | Weiter offen / UNKNOWN | S-P99-03 |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | S-P99-03 |
| incremental_load_score | Weiter offen / UNKNOWN | S-P99-03 |
| power_quality_score | Weiter offen / UNKNOWN | S-P99-03 |
| onsite_integration_score | Weiter offen / UNKNOWN | S-P99-03 |
| measures_gap_score | Weiter offen / UNKNOWN | S-P99-03 |
| management_gap_score | Weiter offen / UNKNOWN | S-P99-03 |
| targets_gap_score | Weiter offen / UNKNOWN | S-P99-03 |
| investment_gap_score | Weiter offen / UNKNOWN | S-P99-03 |

Own machine inventory was re-read. Arburg model designations and closing forces do not alone establish installed converter topology. Current manufacturer brochure describes newer series without proving the owned legacy machines configuration. No new field closed.

Feldweise Spur: `evidence/field_research_20261008.csv`; aktuelle Werte: `data/score_coding_proposals.csv`.
