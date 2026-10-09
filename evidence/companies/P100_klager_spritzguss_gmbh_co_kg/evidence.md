# P100 — Kläger Spritzguss GmbH & Co. KG

## Provisional inclusion

- Process stratum: `plastics_processing`
- Process mapping: `PR001` — plastic injection moulding; toolmaking and series production
- SME status: `probable`; final financial and linked-enterprise review pending
- Independent human review: `PENDING`

## Sources checked

1. [Legal entity / company information](https://kunststoffspritzguss-produzent.de/)
2. [Production and process scope](https://klaeger.de/)

## Coding note

The public sources support the legal-entity and process mapping used for provisional sample assembly. They do not establish actual energy consumption, buying intent, grid capacity or deployment of a specific energy solution. Certificate searches are recorded as `NOT_FOUND_AFTER_CHECK`; this means only that no direct public evidence was located in the defined check, not that a certificate or deployment does not exist.


## Continuous ranked fieldwise batch — 2026-10-07

NBCC-2026-10-07-06 frozen on main after PR #44 before enrichment. Historical fixtures preserve pre-enrichment sources/mapping and deterministic ranked selection; priority is documentary information gain, not score.

Owned Dornstetten machine and ceramic PDFs establish actual electric machines and more than 20 sintering systems at 1400/1650 C. SPC new-machine news is excluded; own room heat pumps and 2010 PV are separately bounded.

- S-P100-03: https://klaeger.de/unternehmen/nachhaltikgeit/ — Own Dornstetten page describes heat pumps/heat exchangers using production waste heat for OPERATING ROOMS and onsite PV since 2010. Room heat not process-heat temperature; 85 tonnes CO2 claim not measured energy demand. No dated future target or recent commissioning date.
- S-P100-04: https://klaeger.de/wp-content/uploads/Maschinenpark-Klaeger_2023.pdf — PDF body names Kläger Spritzguss GmbH & Co. KG, Hochgerichtstrasse 33 Dornstetten: 40 injection machines, several Zeres machines labelled elektrisch, CNC/EDM, automated islands and full parameter monitoring/archiving. Closing force in kN is not electric power. Filename 2023 does not date machine commissioning.
- S-P100-05: https://klaeger.de/wp-content/uploads/Prozessbeschreibung-Keramikspritzguss.pdf — Own named Dornstetten body lists all in-house debinding routes and more than 20 sintering systems; process sintering examples ZrO2 about 1400 C and Al2O3 about 1650 C. Actual heat carrier, duty/load and timing constraints not given.
- S-P100-06: https://klaeger-group.com/news/automatisierung-neue-spritzgussmaschine/ — News explicitly concerns Kläger SPC, including SAB support, not the Dornstetten legal entity. Its newly commissioned electric KraussMaffei machine and automation are NOT attributed to P100; no group-asset or investment inheritance.
- S-P100-07: https://klaeger.de/downloads-2/ — Own index provides machine/process PDFs and ISO 9001 documents. Quality certificates do not establish ISO 50001/14001/EMAS or a mature EnMS; group Spraying/SPC certificates cannot be inherited.

All 15 fields assessed: 11 numeric proposals pending independent human review; 4 blank NEEDS_RESEARCH fields with UNKNOWN confidence. No aggregate score.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- |
| temperature_fit_score | 3 | C | AWAITING_HUMAN_REVIEW | S-P100-05 |
| process_electrification_score | 7 | C | AWAITING_HUMAN_REVIEW | S-P100-05 |
| fossil_heat_displacement_score | — | UNKNOWN | NEEDS_RESEARCH | S-P100-03, S-P100-04 |
| motor_drive_score | 5 | B | AWAITING_HUMAN_REVIEW | S-P100-04 |
| power_conversion_score | 8 | C | AWAITING_HUMAN_REVIEW | S-P100-04, S-P100-03 |
| automation_control_score | 4 | B | AWAITING_HUMAN_REVIEW | S-P100-04 |
| scheduling_flex_score | 2 | C | AWAITING_HUMAN_REVIEW | S-P100-05 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P100-03, S-P100-04 |
| incremental_load_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P100-05 |
| power_quality_score | 3 | C | AWAITING_HUMAN_REVIEW | S-P100-04, S-P100-03 |
| onsite_integration_score | 2 | B | AWAITING_HUMAN_REVIEW | S-P100-03 |
| measures_gap_score | 0 | B | AWAITING_HUMAN_REVIEW | S-P100-03, S-P100-04 |
| management_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P100-03, S-P100-04 |
| targets_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P100-03 |
| investment_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P100-03, S-P100-04 |

Exact rationales and missing facts in data/score_coding_proposals.csv. Owner, issuer and public-agency facts distinguish retrieval, legal holder/site, reporting period and actual operation. Readable PDF text and relevant certificate/equipment image bodies checked. Investment window 2021-10-07 to 2026-10-07. Previous proposals, canonical numeric/deployment/staff/confidence and actual human-review records unchanged. AI first pass is never Anna human review.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| temperature_fit_score | 3 | 3 | Geprüft | S-P100-05 |
| process_electrification_score | 7 | 7 | Geprüft | S-P100-05 |
| motor_drive_score | 5 | 5 | Geprüft | S-P100-04 |
| power_conversion_score | 8 | 8 | Geprüft | S-P100-04|S-P100-03 |
| automation_control_score | 4 | 4 | Geprüft | S-P100-04 |
| scheduling_flex_score | 2 | 2 | Geprüft | S-P100-05 |
| incremental_load_score | 5 | 5 | Geprüft | S-P100-05 |
| power_quality_score | 3 | 3 | Geprüft | S-P100-04|S-P100-03 |
| onsite_integration_score | 2 | 2 | Geprüft | S-P100-03 |
| measures_gap_score | 0 | 0 | Geprüft | S-P100-03|S-P100-04 |
| targets_gap_score | 3 | 3 | Geprüft | S-P100-03 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 4 zuvor offene Felder bearbeitet; 0 zusätzliche Felder quellen- und ankergeprüft; 4 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Group Kläger SPC new electric machine must not be transferred to Kläger Spritzguss without entity/site attribution.2010PV is outside lookback; room heat recovery does not establish production fuel remainder.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | Current company/site process heat carrier mix and attributable fossil thermal duty. No public evidence is not zero fossil heat. |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | Actual useful heat/cold buffer capacity, temperature, connection and timing freedom; thermal mass, room heat and electrical batteries not sufficient. |
| management_gap_score | Weiter offen / UNKNOWN | Current direct ISO 50001/14001/EMAS or operational energy-management evidence for exact holder; quality-only and absent public certificate not no-management conclusion. |
| investment_gap_score | Weiter offen / UNKNOWN | Completed owned energy investments with commissioning dates in 2021-10-07 to 2026-10-07. Operation/report/filename dates, generic annual CAPEX and other group companies not sufficient. |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.


## Vertiefte Entscheidungsrecherche — 2026-10-08

Kunststoff- und Keramikspritzguss, Entbindern und Sintern; aktuelle Sinterenergieträger fehlen. Eigene PV und Rückgewinnung für Gebäudeheizung belegt; neue Maschine der anderen Gruppengesellschaft nicht zurechnen.

**Ergebnis:** PARTIAL_EVIDENCE. **Nächster Schritt:** Verbraucher der Rückgewinnung, genaue Brennstoffe und datierte abgeschlossene Investitionen beim eigenen Werk prüfen.

Auswahl: Rang 3 der zehn verschiedenen Firmen ohne offenes KMU-Gate; ursprünglicher Research-Rang 18.

- S-P100-03: https://klaeger.de/unternehmen/nachhaltikgeit/ — Kläger nennt eigene Photovoltaik und Wärmerückgewinnung für Heizungszwecke. Bau-/Raumwärme ist keine belegte elektrische Sinterwärme.
- S-P100-05: https://klaeger.de/wp-content/uploads/Prozessbeschreibung-Keramikspritzguss.pdf — Eigenes Keramikspritzguss-Dokument beschreibt Entbinderung und Sinterung; genaue aktuelle Brennstoffe und Restwärmelasten bleiben offen.

Quellenprüfung durch Codex. Geprüfte Feldvorschläge sind keine finale Score-Freigabe. Nicht belegte Felder bleiben UNKNOWN.

| Feld | Ergebnis | Weiterhin benötigter Beleg |
|---|---|---|
| fossil_heat_displacement_score | Offen | Current company/site process heat carrier mix and attributable fossil thermal duty. No public evidence is not zero fossil heat. Continuation2026-10-08: Group Kläger SPC new electric machine must not be transferred to Kläger Spritzguss without entity/site attribution.2010PV is outside lookback; room heat recovery does not establish production fuel remainder. Vertiefung 2026-10-08: Verbraucher der Rückgewinnung, genaue Brennstoffe und datierte abgeschlossene Investitionen beim eigenen Werk prüfen. |
| thermal_storage_flex_score | Offen | Actual useful heat/cold buffer capacity, temperature, connection and timing freedom; thermal mass, room heat and electrical batteries not sufficient. Continuation2026-10-08: Group Kläger SPC new electric machine must not be transferred to Kläger Spritzguss without entity/site attribution.2010PV is outside lookback; room heat recovery does not establish production fuel remainder. Vertiefung 2026-10-08: Verbraucher der Rückgewinnung, genaue Brennstoffe und datierte abgeschlossene Investitionen beim eigenen Werk prüfen. |
| management_gap_score | Offen | Current direct ISO 50001/14001/EMAS or operational energy-management evidence for exact holder; quality-only and absent public certificate not no-management conclusion. Continuation2026-10-08: Group Kläger SPC new electric machine must not be transferred to Kläger Spritzguss without entity/site attribution.2010PV is outside lookback; room heat recovery does not establish production fuel remainder. Vertiefung 2026-10-08: Verbraucher der Rückgewinnung, genaue Brennstoffe und datierte abgeschlossene Investitionen beim eigenen Werk prüfen. |
| investment_gap_score | Offen | Completed owned energy investments with commissioning dates in 2021-10-07 to 2026-10-07. Operation/report/filename dates, generic annual CAPEX and other group companies not sufficient. Continuation2026-10-08: Group Kläger SPC new electric machine must not be transferred to Kläger Spritzguss without entity/site attribution.2010PV is outside lookback; room heat recovery does not establish production fuel remainder. Vertiefung 2026-10-08: Verbraucher der Rückgewinnung, genaue Brennstoffe und datierte abgeschlossene Investitionen beim eigenen Werk prüfen. |
