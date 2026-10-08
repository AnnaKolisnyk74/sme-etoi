# P95 — Winkler-Bräu GmbH & Co. KG

## Provisional inclusion

- Process stratum: `food_beverage`
- Process mapping: `PR003` — brewing; open fermentation; maturation and filling
- SME status: `probable`; final financial and linked-enterprise review pending
- Independent human review: `PENDING`

## Sources checked

1. [Legal entity / company information](https://www.winkler-braeu.de/impressum/)
2. [Production and process scope](https://www.winkler-braeu.de/)

## Coding note

The public sources support the legal-entity and process mapping used for provisional sample assembly. They do not establish actual energy consumption, buying intent, grid capacity or deployment of a specific energy solution. Certificate searches are recorded as `NOT_FOUND_AFTER_CHECK`; this means only that no direct public evidence was located in the defined check, not that a certificate or deployment does not exist.


## Public-source retrieval audit — 2026-10-06 (AI first pass)

- Original: https://www.winkler-braeu.de/impressum/ — REPLACEMENT_FOUND. Replacement/context IDs: `S-P95-03`. Company-specific official state-backed directory names brewery at expected address. Open: Hotel and brewery entities remain distinct; financial/group gates unchanged.

See `evidence/source_link_audit.csv` for GET status and `evidence/source_recovery.csv` for exact scope. Retrieval/recovery is not Anna's Human Review; scores, certificate validity and deployment UNKNOWNs are unchanged.


## Continuous ranked fieldwise batch — 2026-10-07

NBCC-2026-10-07-06 frozen on main after PR #44 before enrichment. Historical fixtures preserve pre-enrichment sources/mapping and deterministic ranked selection; priority is documentary information gain, not score.

Lengenfeld brewery distinct from Amberg/Weissenohe and from the hotel entity. Undated brewhouse modernisation does not establish recent energy CAPEX.

- S-P95-04: https://www.winkler-braeu.de/privatbrauerei-bayern/brauhandwerk — Own brewery describes hand brewing, modernised brewhouse and slow open fermentation. No process temperature, heat carrier, refrigeration inventory, commissioning date or shift permission. Not Brauerei Winkler Amberg or Weissenohe; hotel legal entity is separate.
- S-P95-05: https://www.winkler-braeu.de/fileadmin/files/PDF/2024_WinklerBraeu_Unternehmensphilosophie.pdf — Joint hotel/brewery philosophy includes continuing brewery equipment modernisation and general responsible operations. Hotel/building commitments cannot establish brewery energy assets, dated energy targets or recent energy CAPEX.

All 15 fields assessed: 1 numeric proposals pending independent human review; 14 blank NEEDS_RESEARCH fields with UNKNOWN confidence. No aggregate score.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- |
| temperature_fit_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| process_electrification_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| fossil_heat_displacement_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| motor_drive_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| power_conversion_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| automation_control_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| scheduling_flex_score | 2 | C | AWAITING_HUMAN_REVIEW | S-P95-04 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| incremental_load_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| power_quality_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| onsite_integration_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| measures_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| management_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| targets_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |
| investment_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P95-04, S-P95-05 |

Exact rationales and missing facts in data/score_coding_proposals.csv. Owner, issuer and public-agency facts distinguish retrieval, legal holder/site, reporting period and actual operation. Readable PDF text and relevant certificate/equipment image bodies checked. Investment window 2021-10-07 to 2026-10-07. Previous proposals, canonical numeric/deployment/staff/confidence and actual human-review records unchanged. AI first pass is never Anna human review.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| scheduling_flex_score | 2 | 2 | Geprüft | S-P95-04 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.


## Offene Felder: Recherche 2026-10-08

Prüfer: Codex. Status **Geprüft** bedeutet Quellen- und Ankerprüfung; persönliche Freigabe bleibt separat.

| Feld | Ergebnis | Belege |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | S-P95-06 |
| process_electrification_score | Weiter offen / UNKNOWN | S-P95-06 |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | S-P95-06 |
| motor_drive_score | Geprüft: 5 | S-P95-06 |
| power_conversion_score | Weiter offen / UNKNOWN | S-P95-06 |
| automation_control_score | Geprüft: 4 | S-P95-06 |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | S-P95-06 |
| incremental_load_score | Weiter offen / UNKNOWN | S-P95-06 |
| power_quality_score | Weiter offen / UNKNOWN | S-P95-06 |
| onsite_integration_score | Weiter offen / UNKNOWN | S-P95-06 |
| measures_gap_score | Weiter offen / UNKNOWN | S-P95-06 |
| management_gap_score | Weiter offen / UNKNOWN | S-P95-06 |
| targets_gap_score | Weiter offen / UNKNOWN | S-P95-06 |
| investment_gap_score | Weiter offen / UNKNOWN | S-P95-06 |

Supplier corroborates own brewery process equipment. The2017 cooling automation is historical; a2023 publication date is not its commissioning date. No energy savings, useful thermal store, current heat carrier or admissible shift window found; hotel assets remain separate.

Feldweise Spur: `evidence/field_research_20261008.csv`; aktuelle Werte: `data/score_coding_proposals.csv`.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 12 zuvor offene Felder bearbeitet; 0 zusätzliche Felder quellen- und ankergeprüft; 12 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Previously inspected brewery supplier case retained. Hotel assets and Amberg namesake are excluded; no new heat fuel, usable thermal storage, temperature or energy CAPEX established.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | Owned process operating temperatures and actual heat/cold duties; separate product ratings and room heating. |
| process_electrification_score | Weiter offen / UNKNOWN | Named owned thermal route, current heat carrier and feasible remaining substitution case; separate electric drives and room heat. |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | Current company/site process heat carrier mix and attributable fossil thermal duty. No public evidence is not zero fossil heat. |
| power_conversion_score | Weiter offen / UNKNOWN | Owned rectifier/inverter/controlled-electric-heat applications, scope and duty; mechanical water power not electricity generation. |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | Actual useful heat/cold buffer capacity, temperature, connection and timing freedom; thermal mass, room heat and electrical batteries not sufficient. |
| incremental_load_score | Weiter offen / UNKNOWN | Owned feasible thermal substitution case and baseline remaining thermal duty; no grid capacity or kW inferred. |
| power_quality_score | Weiter offen / UNKNOWN | Owned relevant converter/peak topology or measured harmonic/reactive/voltage findings; product resistance/current amps not measured power-quality evidence. |
| onsite_integration_score | Weiter offen / UNKNOWN | Owned electricity generation/storage/load-management topology; mechanical hydropower, purchased renewables or group assets not inherited. |
| measures_gap_score | Weiter offen / UNKNOWN | Named current implemented energy measures with exact entity/site/technology scope. Generic efficient/green production and resource recycling not adequate negative-search proof. |
| management_gap_score | Weiter offen / UNKNOWN | Current direct ISO 50001/14001/EMAS or operational energy-management evidence for exact holder; quality-only and absent public certificate not no-management conclusion. |
| targets_gap_score | Weiter offen / UNKNOWN | Owned energy/climate target, date, scope and roadmap, or documented sufficient defined search. General quality/resource sustainability not energy target. |
| investment_gap_score | Weiter offen / UNKNOWN | Completed owned energy investments with commissioning dates in 2021-10-07 to 2026-10-07. Operation/report/filename dates, generic annual CAPEX and other group companies not sufficient. |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.
