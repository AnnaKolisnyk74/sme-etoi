# P93 — Brauerei Schimpfle GmbH & Co. KG

## Provisional inclusion

- Process stratum: `food_beverage`
- Process mapping: `PR003` — brewing; open fermentation; beverage filling
- SME status: `probable`; final financial and linked-enterprise review pending
- Independent human review: `PENDING`

## Sources checked

1. [Legal entity / company information](https://www.brauerei-schimpfle.de/impressum/)
2. [Production and process scope](https://www.brauerei-schimpfle.de/)

## Coding note

The public sources support the legal-entity and process mapping used for provisional sample assembly. They do not establish actual energy consumption, buying intent, grid capacity or deployment of a specific energy solution. Certificate searches are recorded as `NOT_FOUND_AFTER_CHECK`; this means only that no direct public evidence was located in the defined check, not that a certificate or deployment does not exist.


## Public-source retrieval audit — 2026-10-06 (AI first pass)

- Original: https://www.brauerei-schimpfle.de/impressum/ — REPLACEMENT_FOUND. Replacement/context IDs: `S-P93-03`. Exact entity, address and register on current company imprint.

See `evidence/source_link_audit.csv` for GET status and `evidence/source_recovery.csv` for exact scope. Retrieval/recovery is not Anna's Human Review; scores, certificate validity and deployment UNKNOWNs are unchanged.


## Continuous ranked fieldwise batch — 2026-10-07

NBCC-2026-10-07-05 frozen on main after PR#43 before enrichment: B/B confidence, QA PASS, PROCESS-only coverage, MEDIUM documentary gain,15 unassessed fields and two verified distinct URLs each. ID is final deterministic tie-breaker, not score/yield. Historical fixtures preserve selection before source/mapping corrections.

Actual compressors/heat recovery/metering, primary2024PV908modules/1500m2 and2023transformer;0C maturation not heating fit/storage, transformer not measured harmonic issue.

- S-P93-04: https://www.brauerei-schimpfle.de/brauerei — Own power-regulated refrigeration compressors, desuperheater heat recovery and monitored water/wastewater plus RO.0C maturation not heating-temperature fit or dispatchable thermal store.
- S-P93-05: https://de.linkedin.com/posts/brauerei-schimpfle_brauerei-schimpfle-photovoltaik-activity-7207281589314031616-LBi4 — Public own company post14/06/2024 confirms PV commissioned/running on production/logistics roof:908modules/1500m2, not kWp/kWh. Date from primary post structured metadata, current2026 operation not independently measured.
- S-P93-06: https://www.brauerei-schimpfle.de/blog-collection/jahresruckblick — Own2023 year review published03/01/2024: transformer station INSTALLED for then-coming PV. Packing/tanks capacity not extra proven energy investment. Transformer not measured harmonic issue.

All 15 fields assessed: 8 numeric proposals pending independent human review; 7 blank NEEDS_RESEARCH fields with UNKNOWN confidence. No aggregate score.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- |
| temperature_fit_score | — | UNKNOWN | NEEDS_RESEARCH | S-P93-04 |
| process_electrification_score | — | UNKNOWN | NEEDS_RESEARCH | S-P93-04 |
| fossil_heat_displacement_score | — | UNKNOWN | NEEDS_RESEARCH | S-P93-04 |
| motor_drive_score | 5 | B | AWAITING_HUMAN_REVIEW | S-P93-04 |
| power_conversion_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P93-05 |
| automation_control_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P93-04 |
| scheduling_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P93-04 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P93-04 |
| incremental_load_score | — | UNKNOWN | NEEDS_RESEARCH | S-P93-04 |
| power_quality_score | 1 | C | AWAITING_HUMAN_REVIEW | S-P93-04, S-P93-05, S-P93-06 |
| onsite_integration_score | 2 | C | AWAITING_HUMAN_REVIEW | S-P93-05 |
| measures_gap_score | 0 | B | AWAITING_HUMAN_REVIEW | S-P93-04, S-P93-05 |
| management_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P93-04 |
| targets_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P93-04, S-P93-05 |
| investment_gap_score | 0 | B | AWAITING_HUMAN_REVIEW | S-P93-05, S-P93-06 |

Exact field rationales/gaps in data/score_coding_proposals.csv. Primary own/issuer/project/public agency pages, exact-name energy/certificate/target checks, rendered report/certificate bodies checked 07/10/2026. Availability, attribution, data/report period and current operating continuity separate. Lookback 2021-10-07 to 2026-10-07. Prior proposals, canonical numeric/deployment/staff/confidence and human review unchanged. AI first pass never Anna human review.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| motor_drive_score | 5 | 5 | Geprüft | S-P93-04 |
| power_conversion_score | 5 | 5 | Geprüft | S-P93-05 |
| automation_control_score | 3 | 3 | Geprüft | S-P93-04 |
| power_quality_score | 1 | 1 | Geprüft | S-P93-04 | S-P93-05 | S-P93-06 |
| onsite_integration_score | 2 | 2 | Geprüft | S-P93-05 |
| measures_gap_score | 0 | 0 | Geprüft | S-P93-04 | S-P93-05 |
| targets_gap_score | 3 | 3 | Geprüft | S-P93-04 | S-P93-05 |
| investment_gap_score | 0 | 2 | Geprüft | S-P93-05 | S-P93-06 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

- **investment_gap_score**: The own 2023 review describes a transformer installed partly FOR the forthcoming PV; the own June 2024 post confirms that PV was commissioned. The evidence supports one integrated completed PV/infrastructure project, not two proven independent energy investments.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 7 zuvor offene Felder bearbeitet; 0 zusätzliche Felder quellen- und ankergeprüft; 7 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Cold maturation and installed pressure tanks are not useful thermal buffers. Heat recovery from controlled compressors does not establish hot-process temperatures or remaining heat fuel.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | Actual process-heating temperatures and supported electric-heat fit, rather than part dimensions, cold maturation, material/customer ratings or historical boiler baselines. Actual compressors/heat recovery/metering, primary2024PV908modules/1500m2 and2023transformer;0C maturation not heating fit/storage, transformer not measured harmonic issue. |
| process_electrification_score | Weiter offen / UNKNOWN | Named own actual/planned electric thermal route; electrochemical coating, generic production or customer energy applications alone do not establish electric process heat. Actual compressors/heat recovery/metering, primary2024PV908modules/1500m2 and2023transformer;0C maturation not heating fit/storage, transformer not measured harmonic issue. |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | Actual current fossil thermal carrier, centrality and displacement materiality; unspecified CHP/ovens and historic gas baselines do not establish remaining fuel mix. Actual compressors/heat recovery/metering, primary2024PV908modules/1500m2 and2023transformer;0C maturation not heating fit/storage, transformer not measured harmonic issue. |
| scheduling_flex_score | Weiter offen / UNKNOWN | Admissible operating/start/interruption windows and actual buffers; product maturation, process cycles or programmable furnace recipes are not dispatch permission. Actual compressors/heat recovery/metering, primary2024PV908modules/1500m2 and2023transformer;0C maturation not heating fit/storage, transformer not measured harmonic issue. |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | Named own usable heat/cold store or validated thermal inertia with operating window; cooling, absorption chilling, production tanks and glass melt mass alone do not establish storage. Actual compressors/heat recovery/metering, primary2024PV908modules/1500m2 and2023transformer;0C maturation not heating fit/storage, transformer not measured harmonic issue. |
| incremental_load_score | Weiter offen / UNKNOWN | Defined additional thermal electrification route and ordinal new-load materiality; existing electric assets, PV expansion and EV charging are not an additional heat-route load. Actual compressors/heat recovery/metering, primary2024PV908modules/1500m2 and2023transformer;0C maturation not heating fit/storage, transformer not measured harmonic issue. |
| management_gap_score | Weiter offen / UNKNOWN | Current verified site EnMS/environmental system or bounded claim; ISO9001, an inaccessible/staging certificate page and missing evidence are not certified mature EnMS. Actual compressors/heat recovery/metering, primary2024PV908modules/1500m2 and2023transformer;0C maturation not heating fit/storage, transformer not measured harmonic issue. |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.
