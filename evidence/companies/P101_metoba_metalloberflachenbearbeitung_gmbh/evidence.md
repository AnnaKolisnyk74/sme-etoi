# P101 — Metoba Metalloberflächenbearbeitung GmbH

## Provisional inclusion

- Process stratum: `metal_surface_heat`
- Process mapping: `PR005` — band; rack and barrel electroplating; selective plating
- SME status: `probable`; final financial and linked-enterprise review pending
- Independent human review: `PENDING`

## Sources checked

1. [Legal entity / company information](https://www.metoba.de/impressum/)
2. [Production and process scope](https://www.metoba.de/)

## Coding note

The public sources support the legal-entity and process mapping used for provisional sample assembly. They do not establish actual energy consumption, buying intent, grid capacity or deployment of a specific energy solution. Certificate searches are recorded as `NOT_FOUND_AFTER_CHECK`; this means only that no direct public evidence was located in the defined check, not that a certificate or deployment does not exist.


## Continuous ranked fieldwise batch — 2026-10-07

NBCC-2026-10-07-06 frozen on main after PR #44 before enrichment. Historical fixtures preserve pre-enrichment sources/mapping and deterministic ranked selection; priority is documentary information gain, not score.

Image-only EMAS certificate visually checked: issued 15 January 2026, valid until 30 September 2029, despite 2025 filename. Historical ISO-50001-based EnMS explicitly not certified. BHKW operation is not its commissioning date.

- S-P101-03: https://www.metoba.de/wp-content/uploads/2019/10/Metoba-Imagebrosch%C3%BCre.pdf — Own brochure describes band/barrel/rack/selective galvanic processes and automatically controlled/documented process data. Page 13 explicitly says EnMS on ISO 50001 basis is NOT certified; historical undated brochure does not establish current certification or dated energy CAPEX.
- S-P101-04: https://www.metoba.de/emas-registrierungsurkunde-2025/ — Rendered primary certificate names Metoba, Koenigsberger Strasse 23-33 Luedenscheid, DE-130-00026; first registration 1999-06-30; issue 2026-01-15, valid until 2029-09-30. URL filename 2025 is not issue year. Environmental system is not certified ISO 50001.
- S-P101-05: https://www.gws-mk.de/oekoprofit-workshop-nachhaltigkeit-und-ressourceneffizienz-im-fokus/ — Public development agency reports actual BHKW operation and Metoba EMAS history in 2024 context. Operation-date not commissioning-date; fuel, thermal scope and CHP electrical size unknown. Workshop discussion of ISO 50001 is not Metoba certification.
- S-P101-06: https://www.emas.de/fileadmin/user_upload/4-daten-stat/EMAS-TN-Register.pdf — Official active-register snapshot 2026-09-01 includes Metoba Metalloberflaechenbearbeitung GmbH, DE-130-00026, Luedenscheid. Confirms entity registration independently of own brochure; employee line is not copied to canonical staff.

All 15 fields assessed: 9 numeric proposals pending independent human review; 6 blank NEEDS_RESEARCH fields with UNKNOWN confidence. No aggregate score.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- |
| temperature_fit_score | — | UNKNOWN | NEEDS_RESEARCH | S-P101-03, S-P101-04 |
| process_electrification_score | — | UNKNOWN | NEEDS_RESEARCH | S-P101-03, S-P101-04 |
| fossil_heat_displacement_score | — | UNKNOWN | NEEDS_RESEARCH | S-P101-03, S-P101-04 |
| motor_drive_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P101-03 |
| power_conversion_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P101-03 |
| automation_control_score | 4 | B | AWAITING_HUMAN_REVIEW | S-P101-03 |
| scheduling_flex_score | 2 | C | AWAITING_HUMAN_REVIEW | S-P101-03 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P101-03, S-P101-04 |
| incremental_load_score | — | UNKNOWN | NEEDS_RESEARCH | S-P101-03, S-P101-04 |
| power_quality_score | 3 | C | AWAITING_HUMAN_REVIEW | S-P101-03 |
| onsite_integration_score | 2 | B | AWAITING_HUMAN_REVIEW | S-P101-05 |
| measures_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P101-05 |
| management_gap_score | 2 | B | AWAITING_HUMAN_REVIEW | S-P101-04, S-P101-06, S-P101-03 |
| targets_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P101-03 |
| investment_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P101-03, S-P101-04 |

Exact rationales and missing facts in data/score_coding_proposals.csv. Owner, issuer and public-agency facts distinguish retrieval, legal holder/site, reporting period and actual operation. Readable PDF text and relevant certificate/equipment image bodies checked. Investment window 2021-10-07 to 2026-10-07. Previous proposals, canonical numeric/deployment/staff/confidence and actual human-review records unchanged. AI first pass is never Anna human review.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| motor_drive_score | 5 | 5 | Geprüft | S-P101-03 |
| power_conversion_score | 5 | 5 | Geprüft | S-P101-03 |
| automation_control_score | 4 | 4 | Geprüft | S-P101-03 |
| scheduling_flex_score | 2 | 2 | Geprüft | S-P101-03 |
| power_quality_score | 3 | 1 | Geprüft | S-P101-03 |
| onsite_integration_score | 2 | 2 | Geprüft | S-P101-05 |
| measures_gap_score | 3 | 3 | Geprüft | S-P101-05 |
| management_gap_score | 2 | 2 | Geprüft | S-P101-04|S-P101-06|S-P101-03 |
| targets_gap_score | 3 | 3 | Geprüft | S-P101-03 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

- **power_quality_score**: Own electrochemical production supports possible rectifier-related harmonic/peak relevance as an engineering hypothesis. The source does not establish a specific rectifier inventory/topology, explicit peak constraint or measured disturbance. Use the possible-signal anchor consistently; chemical nickel and product properties are not additional converter evidence.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 6 zuvor offene Felder bearbeitet; 0 zusätzliche Felder quellen- und ankergeprüft; 6 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Ökoprofit workshop explains standards generally; hosting it is not current ISO50001certification or completed energy investment. Existing brochure heat temperatures/fuels remain unspecified.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | Owned process operating temperatures and actual heat/cold duties; separate product ratings and room heating. |
| process_electrification_score | Weiter offen / UNKNOWN | Named owned thermal route, current heat carrier and feasible remaining substitution case; separate electric drives and room heat. |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | Current company/site process heat carrier mix and attributable fossil thermal duty. No public evidence is not zero fossil heat. |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | Actual useful heat/cold buffer capacity, temperature, connection and timing freedom; thermal mass, room heat and electrical batteries not sufficient. |
| incremental_load_score | Weiter offen / UNKNOWN | Owned feasible thermal substitution case and baseline remaining thermal duty; no grid capacity or kW inferred. |
| investment_gap_score | Weiter offen / UNKNOWN | Completed owned energy investments with commissioning dates in 2021-10-07 to 2026-10-07. Operation/report/filename dates, generic annual CAPEX and other group companies not sufficient. |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.


## Continued open-field research —2026-10-09

Metobas Nachrichten enthalten Vorträge über Wärmepumpen, B&T-Studie und Hillebrand-Klimapläne; dies sind keine eigenen Metoba-Anlagen. Altes eigenes Management-/Prozessmaterial ersetzt keine aktuelle Wärme-/Investitionsinventur.

Nächster Schritt: Eigene aktuelle Umwelterklärung, Badtemperaturen/Heizmedien und datierte Anlagenmaßnahmen beschaffen.

- S-P101-07 — https://www.metoba.de/newsarchiv/ — Heat-pump presentations, B&T feasibility study and Hillebrand climate plans belong to speakers/other firms, not Metoba installations. No owned current heat-electrification or investment inferred.
- S-P101-03 — https://www.metoba.de/wp-content/uploads/2019/10/Metoba-Imagebrosch%C3%BCre.pdf — Historical Metoba environmental management and non-accredited ISO50001-based energy management; no current process temperatures/fuel, thermal storage or recent investment date.

| Feld | Ergebnis | Beleg / verbleibende Frage |
| --- | --- | --- |
| temperature_fit_score | STILL_UNKNOWN | Owned process operating temperatures and actual heat/cold duties; separate product ratings and room heating. Continuation2026-10-08: Ökoprofit workshop explains standards generally; hosting it is not current ISO50001certification or completed energy investment. Existing brochure heat temperatures/fuels remain unspecified. Vertiefung2026-10-09: Eigene aktuelle Umwelterklärung, Badtemperaturen/Heizmedien und datierte Anlagenmaßnahmen beschaffen. |
| process_electrification_score | STILL_UNKNOWN | Named owned thermal route, current heat carrier and feasible remaining substitution case; separate electric drives and room heat. Continuation2026-10-08: Ökoprofit workshop explains standards generally; hosting it is not current ISO50001certification or completed energy investment. Existing brochure heat temperatures/fuels remain unspecified. Vertiefung2026-10-09: Eigene aktuelle Umwelterklärung, Badtemperaturen/Heizmedien und datierte Anlagenmaßnahmen beschaffen. |
| fossil_heat_displacement_score | STILL_UNKNOWN | Current company/site process heat carrier mix and attributable fossil thermal duty. No public evidence is not zero fossil heat. Continuation2026-10-08: Ökoprofit workshop explains standards generally; hosting it is not current ISO50001certification or completed energy investment. Existing brochure heat temperatures/fuels remain unspecified. Vertiefung2026-10-09: Eigene aktuelle Umwelterklärung, Badtemperaturen/Heizmedien und datierte Anlagenmaßnahmen beschaffen. |
| thermal_storage_flex_score | STILL_UNKNOWN | Actual useful heat/cold buffer capacity, temperature, connection and timing freedom; thermal mass, room heat and electrical batteries not sufficient. Continuation2026-10-08: Ökoprofit workshop explains standards generally; hosting it is not current ISO50001certification or completed energy investment. Existing brochure heat temperatures/fuels remain unspecified. Vertiefung2026-10-09: Eigene aktuelle Umwelterklärung, Badtemperaturen/Heizmedien und datierte Anlagenmaßnahmen beschaffen. |
| incremental_load_score | STILL_UNKNOWN | Owned feasible thermal substitution case and baseline remaining thermal duty; no grid capacity or kW inferred. Continuation2026-10-08: Ökoprofit workshop explains standards generally; hosting it is not current ISO50001certification or completed energy investment. Existing brochure heat temperatures/fuels remain unspecified. Vertiefung2026-10-09: Eigene aktuelle Umwelterklärung, Badtemperaturen/Heizmedien und datierte Anlagenmaßnahmen beschaffen. |
| investment_gap_score | STILL_UNKNOWN | Completed owned energy investments with commissioning dates in 2021-10-07 to 2026-10-07. Operation/report/filename dates, generic annual CAPEX and other group companies not sufficient. Continuation2026-10-08: Ökoprofit workshop explains standards generally; hosting it is not current ISO50001certification or completed energy investment. Existing brochure heat temperatures/fuels remain unspecified. Vertiefung2026-10-09: Eigene aktuelle Umwelterklärung, Badtemperaturen/Heizmedien und datierte Anlagenmaßnahmen beschaffen. |

Geprüft bezeichnet Quellen-/Ankerprüfung durch Codex; keine persönliche oder finale Score-Freigabe.
