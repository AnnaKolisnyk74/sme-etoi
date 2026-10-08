# P92 — Familienbrauerei M. Ketterer GmbH & Co. KG

## Provisional inclusion

- Process stratum: `food_beverage`
- Process mapping: `PR003` — brewing; boiling; fermentation; maturation and filling
- SME status: `probable`; final financial and linked-enterprise review pending
- Independent human review: `PENDING`

## Sources checked

1. [Legal entity / company information](https://www.kettererbier.de/impressum/)
2. [Production and process scope](https://www.kettererbier.de/)

## Coding note

The public sources support the legal-entity and process mapping used for provisional sample assembly. They do not establish actual energy consumption, buying intent, grid capacity or deployment of a specific energy solution. Certificate searches are recorded as `NOT_FOUND_AFTER_CHECK`; this means only that no direct public evidence was located in the defined check, not that a certificate or deployment does not exist.


## Continuous ranked fieldwise batch — 2026-10-07

NBCC-2026-10-07-05 frozen on main after PR#43 before enrichment: B/B confidence, QA PASS, PROCESS-only coverage, MEDIUM documentary gain,15 unassessed fields and two verified distinct URLs each. ID is final deterministic tie-breaker, not score/yield. Historical fixtures preserve selection before source/mapping corrections.

Own woodchip operating-heat claim, PV2021monthunknown; nitrogen dates2021/2023 conflict; biomass not electric heat, cold tanks not dispatch buffers.

- S-P92-03: https://www.kettererbier.de/netterer-welt/umweltschutz — Own current woodchips since2006, purchased green electricity, PV2021 (month unavailable) and nitrogen generatorSPRING2023. Other own Hornberger brand page saysSPRING2021 for nitrogen; discrepancy retained. Nitrogen resource substitution not automatically proved energy CAPEX.
- S-P92-04: https://www.kettererbier.de/brauerei/brauereirundgang — Own brewery pump transfers, temperature-regulated yeast process and Schoko vacuum boil; no actual heating degrees stated. Explicit all operating heat exclusively woodchips since2006; scope thermal service only, not transport/whole-plant zero carbon.
- S-P92-05: https://www.kettererbier.de/brauerei/geschichte — Historical automated brewhouse and tanks; age/history not flexible operating/thermal-buffer window or recent energy investment.
- S-P92-06: https://www.hornberger-lebensquell.de/wir-ueber-uns — Own Hornberger/Ketterer brand account claims2021 PV/hall and nitrogen generatorin same spring, differing from current brewery page2023 nitrogen. Preserve distinct date/scope; no averaging or invented month.

All 15 fields assessed: 8 numeric proposals pending independent human review; 7 blank NEEDS_RESEARCH fields with UNKNOWN confidence. No aggregate score.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- |
| temperature_fit_score | — | UNKNOWN | NEEDS_RESEARCH | S-P92-03 |
| process_electrification_score | — | UNKNOWN | NEEDS_RESEARCH | S-P92-03 |
| fossil_heat_displacement_score | 0 | C | AWAITING_HUMAN_REVIEW | S-P92-03, S-P92-04 |
| motor_drive_score | 2 | B | AWAITING_HUMAN_REVIEW | S-P92-04 |
| power_conversion_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P92-03 |
| automation_control_score | 1 | B | AWAITING_HUMAN_REVIEW | S-P92-04 |
| scheduling_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P92-03 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P92-03 |
| incremental_load_score | — | UNKNOWN | NEEDS_RESEARCH | S-P92-03 |
| power_quality_score | 1 | C | AWAITING_HUMAN_REVIEW | S-P92-03 |
| onsite_integration_score | 2 | B | AWAITING_HUMAN_REVIEW | S-P92-03 |
| measures_gap_score | 0 | B | AWAITING_HUMAN_REVIEW | S-P92-03, S-P92-04 |
| management_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P92-03 |
| targets_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P92-03, S-P92-04 |
| investment_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P92-03 |

Exact field rationales/gaps in data/score_coding_proposals.csv. Primary own/issuer/project/public agency pages, exact-name energy/certificate/target checks, rendered report/certificate bodies checked 07/10/2026. Availability, attribution, data/report period and current operating continuity separate. Lookback 2021-10-07 to 2026-10-07. Prior proposals, canonical numeric/deployment/staff/confidence and human review unchanged. AI first pass never Anna human review.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| fossil_heat_displacement_score | 0 | 0 | Geprüft | S-P92-03 | S-P92-04 |
| motor_drive_score | 2 | 2 | Geprüft | S-P92-04 |
| power_conversion_score | 5 | 5 | Geprüft | S-P92-03 |
| automation_control_score | 1 | 1 | Geprüft | S-P92-04 |
| power_quality_score | 1 | 1 | Geprüft | S-P92-03 |
| onsite_integration_score | 2 | 2 | Geprüft | S-P92-03 |
| measures_gap_score | 0 | 0 | Geprüft | S-P92-03 | S-P92-04 |
| targets_gap_score | 3 | 3 | Geprüft | S-P92-03 | S-P92-04 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.
