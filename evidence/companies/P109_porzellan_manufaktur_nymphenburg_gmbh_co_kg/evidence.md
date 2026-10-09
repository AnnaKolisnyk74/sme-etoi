# P109 — Porzellan Manufaktur Nymphenburg GmbH & Co. KG

## Provisional inclusion

- Process stratum: `glass_ceramics`
- Process mapping: `PR007` — porcelain forming; glazing; painting and firing
- SME status: `probable`; final financial and linked-enterprise review pending
- Independent human review: `PENDING`

## Sources checked

1. [Legal entity / company information](https://www.nymphenburg.com/policies/legal-notice)
2. [Production and process scope](https://www.nymphenburg.com/)

## Coding note

The public sources support the legal-entity and process mapping used for provisional sample assembly. They do not establish actual energy consumption, buying intent, grid capacity or deployment of a specific energy solution. Certificate searches are recorded as `NOT_FOUND_AFTER_CHECK`; this means only that no direct public evidence was located in the defined check, not that a certificate or deployment does not exist.


## Continuous ranked fieldwise batch — 2026-10-07

NBCC-2026-10-07-06 frozen on main after PR #44 before enrichment. Historical fixtures preserve pre-enrichment sources/mapping and deterministic ranked selection; priority is documentary information gain, not score.

Own firing 950/about1400 C up to36h; water drives mechanical belts, not hydroelectric generation. More climate-friendly adapted kiln unspecified and undated.

- S-P109-03: https://www.nymphenburg.com/pages/brennerei — Own kiln route: first firing 950 C, glaze firing around 1400 C up to 36 hours, subsequent decorative firing. Duration is not available shift window. No actual heat carrier or nameplate load given.
- S-P109-04: https://www.nymphenburg.com/pages/wasserkraft — Water from Schlossbach drives mills, stirrer and pottery wheels through a mechanical belt network. This is mechanical hydropower, NOT evidence of owned hydroelectric generation, electric motor drives, inverter deployment, PV or grid export.
- S-P109-05: https://www.nymphenburg.com/pages/qualitatsversprechen — Owner states only firing technique adapted for more climate-friendly operation; no carrier, equipment model, date or quantified target. Mechanical water drive persists. Change is some measure, not independently verified electric kiln or recent investment.

All 15 fields assessed: 8 numeric proposals pending independent human review; 7 blank NEEDS_RESEARCH fields with UNKNOWN confidence. No aggregate score.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- |
| temperature_fit_score | 3 | C | AWAITING_HUMAN_REVIEW | S-P109-03 |
| process_electrification_score | 7 | C | AWAITING_HUMAN_REVIEW | S-P109-03 |
| fossil_heat_displacement_score | — | UNKNOWN | NEEDS_RESEARCH | S-P109-03, S-P109-04 |
| motor_drive_score | — | UNKNOWN | NEEDS_RESEARCH | S-P109-03, S-P109-04 |
| power_conversion_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P109-03 |
| automation_control_score | — | UNKNOWN | NEEDS_RESEARCH | S-P109-03, S-P109-04 |
| scheduling_flex_score | 2 | C | AWAITING_HUMAN_REVIEW | S-P109-03 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P109-03, S-P109-04 |
| incremental_load_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P109-03 |
| power_quality_score | 1 | C | AWAITING_HUMAN_REVIEW | S-P109-03 |
| onsite_integration_score | — | UNKNOWN | NEEDS_RESEARCH | S-P109-03, S-P109-04 |
| measures_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P109-04, S-P109-05 |
| management_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P109-03, S-P109-04 |
| targets_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P109-05 |
| investment_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P109-03, S-P109-04 |

Exact rationales and missing facts in data/score_coding_proposals.csv. Owner, issuer and public-agency facts distinguish retrieval, legal holder/site, reporting period and actual operation. Readable PDF text and relevant certificate/equipment image bodies checked. Investment window 2021-10-07 to 2026-10-07. Previous proposals, canonical numeric/deployment/staff/confidence and actual human-review records unchanged. AI first pass is never Anna human review.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| temperature_fit_score | 3 | 3 | Geprüft | S-P109-03 |
| process_electrification_score | 7 | 7 | Geprüft | S-P109-03 |
| power_conversion_score | 5 | 5 | Geprüft | S-P109-03 |
| scheduling_flex_score | 2 | 2 | Geprüft | S-P109-03 |
| incremental_load_score | 5 | 5 | Geprüft | S-P109-03 |
| power_quality_score | 1 | 1 | Geprüft | S-P109-03 |
| measures_gap_score | 3 | 3 | Geprüft | S-P109-04|S-P109-05 |
| targets_gap_score | 3 | 3 | Geprüft | S-P109-05 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 7 zuvor offene Felder bearbeitet; 0 zusätzliche Felder quellen- und ankergeprüft; 7 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Current imprint names Königliche Porzellan Manufaktur Nymphenburg GmbH&Co.KG, differing from dataset. Mechanical water drives are not electric converters/generation; no entity transfer or new numeric assessment made.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | Current company/site process heat carrier mix and attributable fossil thermal duty. No public evidence is not zero fossil heat. |
| motor_drive_score | Weiter offen / UNKNOWN | Owned electrical motor/compressor inventory, process roles and duty; mechanical drive not automatically electric. |
| automation_control_score | Weiter offen / UNKNOWN | Owned process control/monitoring inventory and operational coordination; quality claims not EnMS maturity. |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | Actual useful heat/cold buffer capacity, temperature, connection and timing freedom; thermal mass, room heat and electrical batteries not sufficient. |
| onsite_integration_score | Weiter offen / UNKNOWN | Owned electricity generation/storage/load-management topology; mechanical hydropower, purchased renewables or group assets not inherited. |
| management_gap_score | Weiter offen / UNKNOWN | Current direct ISO 50001/14001/EMAS or operational energy-management evidence for exact holder; quality-only and absent public certificate not no-management conclusion. |
| investment_gap_score | Weiter offen / UNKNOWN | Completed owned energy investments with commissioning dates in 2021-10-07 to 2026-10-07. Operation/report/filename dates, generic annual CAPEX and other group companies not sufficient. |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.


## Vertiefte Entscheidungsrecherche — 2026-10-08

Aktuelles Impressum: Königliche Porzellan Manufaktur Nymphenburg GmbH & Co. KG, München HRA 48197; gespeicherter Name ist verkürzt.

**Ergebnis:** NAME_CORRECTION_PROPOSED. **Nächster Schritt:** Registeridentität gegen historischen Datensatz bestätigen und dann exakten Rechtsnamen konsistent übernehmen; bis dahin aktuelle Bezeichnung separat zeigen.

- S-P109-01: https://www.nymphenburg.com/policies/legal-notice — Aktuelles Impressum nennt Königliche Porzellan Manufaktur Nymphenburg GmbH & Co. KG, München HRA 48197. Der gespeicherte Name lässt Königliche aus; keine belegte Rechtsnachfolge allein aus der Website ableiten.

Quellenprüfung durch Codex. Geprüfte Feldvorschläge sind keine finale Score-Freigabe. Nicht belegte Felder bleiben UNKNOWN.
