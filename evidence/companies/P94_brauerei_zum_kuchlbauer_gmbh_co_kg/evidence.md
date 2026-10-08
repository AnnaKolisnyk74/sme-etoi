# P94 — Brauerei zum Kuchlbauer GmbH & Co. KG

## Provisional inclusion

- Process stratum: `food_beverage`
- Process mapping: `PR003` — wheat-beer brewing; boiling; fermentation; maturation and filling
- SME status: `probable`; final financial and linked-enterprise review pending
- Independent human review: `PENDING`

## Sources checked

1. [Legal entity / company information](https://kuchlbauer.de/impressum/)
2. [Production and process scope](https://kuchlbauer.de/)

## Coding note

The public sources support the legal-entity and process mapping used for provisional sample assembly. They do not establish actual energy consumption, buying intent, grid capacity or deployment of a specific energy solution. Certificate searches are recorded as `NOT_FOUND_AFTER_CHECK`; this means only that no direct public evidence was located in the defined check, not that a certificate or deployment does not exist.


## Continuous ranked fieldwise batch — 2026-10-07

NBCC-2026-10-07-05 frozen on main after PR#43 before enrichment: B/B confidence, QA PASS, PROCESS-only coverage, MEDIUM documentary gain,15 unassessed fields and two verified distinct URLs each. ID is final deterministic tie-breaker, not score/yield. Historical fixtures preserve selection before source/mapping corrections.

Actual logistics PV/battery/room HP/charging; builder2024-09-21opening. Room heat not brewery process heat; electrical battery not thermal store; centre climate-positive not whole-company neutrality.

- S-P94-03: https://kuchlbauer.de/bier-und-kunst/logistikzentrum/ — Own logistics centre integrates PV/electrical storage/charging with heat/cold heat pump for ROOMS. Building heat is not brewery process heat; battery not thermal store. Climate-positive claim pertains logistics centre, not whole brewery or independent lifecycle proof.
- S-P94-04: https://stanglmeier-bau.de/aktuelles/beitrag/eroeffnung-kuchlbauer-weissbier-quartier.html — Actual project builder says centre opened21/09/2024, construction sinceearly2023. Bounds one completed integrated energy/site project, not each technology separate commissioning date or whole-brewery energy demand.

All 15 fields assessed: 7 numeric proposals pending independent human review; 8 blank NEEDS_RESEARCH fields with UNKNOWN confidence. No aggregate score.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- |
| temperature_fit_score | — | UNKNOWN | NEEDS_RESEARCH | S-P94-03 |
| process_electrification_score | — | UNKNOWN | NEEDS_RESEARCH | S-P94-03 |
| fossil_heat_displacement_score | — | UNKNOWN | NEEDS_RESEARCH | S-P94-03 |
| motor_drive_score | 2 | C | AWAITING_HUMAN_REVIEW | S-P94-03 |
| power_conversion_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P94-03 |
| automation_control_score | — | UNKNOWN | NEEDS_RESEARCH | S-P94-03 |
| scheduling_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P94-03 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P94-03 |
| incremental_load_score | — | UNKNOWN | NEEDS_RESEARCH | S-P94-03 |
| power_quality_score | 1 | C | AWAITING_HUMAN_REVIEW | S-P94-03 |
| onsite_integration_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P94-03 |
| measures_gap_score | 0 | B | AWAITING_HUMAN_REVIEW | S-P94-03 |
| management_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P94-03 |
| targets_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P94-03 |
| investment_gap_score | 2 | B | AWAITING_HUMAN_REVIEW | S-P94-03, S-P94-04 |

Exact field rationales/gaps in data/score_coding_proposals.csv. Primary own/issuer/project/public agency pages, exact-name energy/certificate/target checks, rendered report/certificate bodies checked 07/10/2026. Availability, attribution, data/report period and current operating continuity separate. Lookback 2021-10-07 to 2026-10-07. Prior proposals, canonical numeric/deployment/staff/confidence and human review unchanged. AI first pass never Anna human review.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| motor_drive_score | 2 | 2 | Geprüft | S-P94-03 |
| power_conversion_score | 5 | 5 | Geprüft | S-P94-03 |
| power_quality_score | 1 | 1 | Geprüft | S-P94-03 |
| onsite_integration_score | 3 | 3 | Geprüft | S-P94-03 |
| measures_gap_score | 0 | 0 | Geprüft | S-P94-03 |
| targets_gap_score | 3 | 3 | Geprüft | S-P94-03 |
| investment_gap_score | 2 | 2 | Geprüft | S-P94-03 | S-P94-04 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 8 zuvor offene Felder bearbeitet; 0 zusätzliche Felder quellen- und ankergeprüft; 8 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Logistics PV/electrical storage/room heat pump are separate from brewery process heat. Electrical storage is not a thermal store; no own admissible process dispatch windows found.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | Actual process-heating temperatures and supported electric-heat fit, rather than part dimensions, cold maturation, material/customer ratings or historical boiler baselines. Actual logistics PV/battery/room HP/charging; builder2024-09-21opening. Room heat not brewery process heat; electrical battery not thermal store; centre climate-positive not whole-company neutrality. |
| process_electrification_score | Weiter offen / UNKNOWN | Named own actual/planned electric thermal route; electrochemical coating, generic production or customer energy applications alone do not establish electric process heat. Actual logistics PV/battery/room HP/charging; builder2024-09-21opening. Room heat not brewery process heat; electrical battery not thermal store; centre climate-positive not whole-company neutrality. |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | Actual current fossil thermal carrier, centrality and displacement materiality; unspecified CHP/ovens and historic gas baselines do not establish remaining fuel mix. Actual logistics PV/battery/room HP/charging; builder2024-09-21opening. Room heat not brewery process heat; electrical battery not thermal store; centre climate-positive not whole-company neutrality. |
| automation_control_score | Weiter offen / UNKNOWN | Actual current owned sensing/control applications and coordination; generic modernity or staging-site claims need corroboration. Actual logistics PV/battery/room HP/charging; builder2024-09-21opening. Room heat not brewery process heat; electrical battery not thermal store; centre climate-positive not whole-company neutrality. |
| scheduling_flex_score | Weiter offen / UNKNOWN | Admissible operating/start/interruption windows and actual buffers; product maturation, process cycles or programmable furnace recipes are not dispatch permission. Actual logistics PV/battery/room HP/charging; builder2024-09-21opening. Room heat not brewery process heat; electrical battery not thermal store; centre climate-positive not whole-company neutrality. |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | Named own usable heat/cold store or validated thermal inertia with operating window; cooling, absorption chilling, production tanks and glass melt mass alone do not establish storage. Actual logistics PV/battery/room HP/charging; builder2024-09-21opening. Room heat not brewery process heat; electrical battery not thermal store; centre climate-positive not whole-company neutrality. |
| incremental_load_score | Weiter offen / UNKNOWN | Defined additional thermal electrification route and ordinal new-load materiality; existing electric assets, PV expansion and EV charging are not an additional heat-route load. Actual logistics PV/battery/room HP/charging; builder2024-09-21opening. Room heat not brewery process heat; electrical battery not thermal store; centre climate-positive not whole-company neutrality. |
| management_gap_score | Weiter offen / UNKNOWN | Current verified site EnMS/environmental system or bounded claim; ISO9001, an inaccessible/staging certificate page and missing evidence are not certified mature EnMS. Actual logistics PV/battery/room HP/charging; builder2024-09-21opening. Room heat not brewery process heat; electrical battery not thermal store; centre climate-positive not whole-company neutrality. |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.
