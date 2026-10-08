# P107 — Dibbern Porzellanmanufaktur GmbH

## Provisional inclusion

- Process stratum: `glass_ceramics`
- Process mapping: `PR007` — fine bone china forming; glazing and firing
- SME status: `probable`; final financial and linked-enterprise review pending
- Independent human review: `PENDING`

## Sources checked

1. [Legal entity / company information](https://www.dibbern.de/en/about-us/)
2. [Production and process scope](https://www.dibbern.de/en/about-dibbern/manufactory/)

## Coding note

The public sources support the legal-entity and process mapping used for provisional sample assembly. They do not establish actual energy consumption, buying intent, grid capacity or deployment of a specific energy solution. Certificate searches are recorded as `NOT_FOUND_AFTER_CHECK`; this means only that no direct public evidence was located in the defined check, not that a certificate or deployment does not exist.


## Public-source retrieval audit — 2026-10-06 (AI first pass)

- Original: https://www.dibbern.de/en/about-us/ — REPLACEMENT_FOUND. Replacement/context IDs: `S-P107-03`. Government-backed named record identifies the exact candidate and Hohenberg address. Open: DIBBERN GmbH imprint must not be assigned to the separate production entity.
- Original: https://www.dibbern.de/en/about-dibbern/manufactory/ — PARTIAL_REPLACEMENT. Replacement/context IDs: `S-P107-03 | S-P107-04`. Exact candidate profile supports porcelain production and hand forming; brand manufacturing page retained as scoped context. Open: Candidate-specific glazing/firing operator attribution and deployment remain unresolved.

See `evidence/source_link_audit.csv` for GET status and `evidence/source_recovery.csv` for exact scope. Retrieval/recovery is not Anna's Human Review; scores, certificate validity and deployment UNKNOWNs are unchanged.


## Completion to 100-company field assessment — 2026-10-07

NBCC-2026-10-07-07: selection frozen before enrichment. Final16 ranked eligible coding candidates; rank is documentary information gain, not score.


All15 fields assessed: 3 numeric proposals awaiting actual human review; 12 blank NEEDS_RESEARCH fields with UNKNOWN confidence. No aggregate score.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- | --- |
| temperature_fit_score | — | UNKNOWN | NEEDS_RESEARCH | S-P107-01, S-P107-02 |
| process_electrification_score | 7 | C | AWAITING_HUMAN_REVIEW | S-P107-04, S-P107-03 |
| fossil_heat_displacement_score | — | UNKNOWN | NEEDS_RESEARCH | S-P107-01, S-P107-02 |
| motor_drive_score | — | UNKNOWN | NEEDS_RESEARCH | S-P107-01, S-P107-02 |
| power_conversion_score | — | UNKNOWN | NEEDS_RESEARCH | S-P107-01, S-P107-02 |
| automation_control_score | — | UNKNOWN | NEEDS_RESEARCH | S-P107-01, S-P107-02 |
| scheduling_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P107-01, S-P107-02 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P107-01, S-P107-02 |
| incremental_load_score | — | UNKNOWN | NEEDS_RESEARCH | S-P107-01, S-P107-02 |
| power_quality_score | — | UNKNOWN | NEEDS_RESEARCH | S-P107-01, S-P107-02 |
| onsite_integration_score | — | UNKNOWN | NEEDS_RESEARCH | S-P107-01, S-P107-02 |
| measures_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P107-04 |
| management_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P107-01, S-P107-02 |
| targets_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P107-04 |
| investment_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P107-01, S-P107-02 |

Exact field rationales/missing facts: data/score_coding_proposals.csv. Certificate bodies and relevant pages visually checked; holder, period, site and product-versus-process scope separated. Frömgen initial HTTP466 subsequently recovered through live HTTP200 primary-body retrieval; owned machining scope reviewed separately. Investment window2021-10-07 to2026-10-07. Previous proposals, canonical numeric/deployment/staff/confidence and actual human-review records preserved. AI first pass is not Anna human review.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| process_electrification_score | 7 | 7 | Geprüft | S-P107-04|S-P107-03 |
| measures_gap_score | 3 | 3 | Geprüft | S-P107-04 |
| targets_gap_score | 3 | 3 | Geprüft | S-P107-04 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 12 zuvor offene Felder bearbeitet; 0 zusätzliche Felder quellen- und ankergeprüft; 12 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Own kiln heat recovery retained. Main Dibbern pages/catalogues return403; parent-brand assets are not inherited into the manufacturing entity and fuel/control facts remain unknown.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | Owned process operating temperatures and actual heat/cold duties; separate product ratings and room heating. |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | Current company/site process heat carrier mix and attributable fossil thermal duty. No public evidence is not zero fossil heat. |
| motor_drive_score | Weiter offen / UNKNOWN | Owned electrical motor/compressor inventory, process roles and duty; mechanical drive not automatically electric. |
| power_conversion_score | Weiter offen / UNKNOWN | Owned rectifier/inverter/controlled-electric-heat applications, scope and duty; mechanical water power not electricity generation. |
| automation_control_score | Weiter offen / UNKNOWN | Owned process control/monitoring inventory and operational coordination; quality claims not EnMS maturity. |
| scheduling_flex_score | Weiter offen / UNKNOWN | Permitted timing shifts, quality/cooling/order constraints and spare capacity. Batch/24h operation alone not flexibility permission. |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | Actual useful heat/cold buffer capacity, temperature, connection and timing freedom; thermal mass, room heat and electrical batteries not sufficient. |
| incremental_load_score | Weiter offen / UNKNOWN | Owned feasible thermal substitution case and baseline remaining thermal duty; no grid capacity or kW inferred. |
| power_quality_score | Weiter offen / UNKNOWN | Owned relevant converter/peak topology or measured harmonic/reactive/voltage findings; product resistance/current amps not measured power-quality evidence. |
| onsite_integration_score | Weiter offen / UNKNOWN | Owned electricity generation/storage/load-management topology; mechanical hydropower, purchased renewables or group assets not inherited. |
| management_gap_score | Weiter offen / UNKNOWN | Current direct ISO 50001/14001/EMAS or operational energy-management evidence for exact holder; quality-only and absent public certificate not no-management conclusion. |
| investment_gap_score | Weiter offen / UNKNOWN | Completed owned energy investments with commissioning dates in 2021-10-07 to 2026-10-07. Operation/report/filename dates, generic annual CAPEX and other group companies not sufficient. |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.
