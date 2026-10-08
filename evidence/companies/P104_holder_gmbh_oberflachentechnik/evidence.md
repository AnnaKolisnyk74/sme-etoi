# P104 — Holder GmbH Oberflächentechnik

## Provisional inclusion

- Process stratum: `metal_surface_heat`
- Process mapping: `PR005` — zinc; zinc-nickel; chemical nickel; anodising and heat treatment
- SME status: `probable`; final financial and linked-enterprise review pending
- Independent human review: `PENDING`

## Sources checked

1. [Legal entity / company information](https://holder-oft.de/impressum/)
2. [Production and process scope](https://holder-oft.de/)

## Coding note

The public sources support the legal-entity and process mapping used for provisional sample assembly. They do not establish actual energy consumption, buying intent, grid capacity or deployment of a specific energy solution. Certificate searches are recorded as `NOT_FOUND_AFTER_CHECK`; this means only that no direct public evidence was located in the defined check, not that a certificate or deployment does not exist.


## Completion to 100-company field assessment — 2026-10-07

GATE-ASSESS-2026-10-07: selection frozen before enrichment. Documentary scope only; upstream group gate retained and canonical score remains blocked.

- S-P104-03: https://holder-oft.de/kompetenzzentrum/zertifikate/ — Owner lists exact Holder ISO 50001 and ISO 14001 bodies/annexes. Holder sites in annex are distinct from upstream group eligibility; filename year is not validity start.
- S-P104-04: https://holder-oft.de/unternehmen/qualitaet-und-umwelt/ — Owner energy/environment policy concerns continuous efficiency and resource improvement. A vague energy ambition is not a quantified dated roadmap, energy investment commissioning or downstream crash-energy savings.
- S-P104-05: https://holder-oft.de/oberflaechenverfahren/waermebehandlung-von-aluminium/ — Owner aluminium process page describes owned heat treatment and controlled adaptation to material/part needs. Crash energy absorption is a product property, not process energy consumption; no actual operating temperature or heat carrier.
- S-P104-06: https://holder-oft.de/wp-content/uploads/Zertifikat-ISO-500012018-2025.pdf — TÜV Rheinland Cert GmbH: Holder GmbH Oberflächentechnik, 01 407 061926; current period 2024-06-14 to 2027-06-13. Exact Holder body and annex: Kirchheim, Lenningen and Laichingen; filename 2025 not validity start.
- S-P104-07: https://holder-oft.de/wp-content/uploads/Zertifikat-ISO-140012015-2025.pdf — TÜV Rheinland Cert GmbH: Holder GmbH Oberflächentechnik, 01 104 061926; current period 2023-11-15 to 2026-11-14. Exact Holder body; valid on check date but near expiry. Group gate remains open.

All15 fields assessed: 5 numeric proposals awaiting actual human review; 10 blank NEEDS_RESEARCH fields with UNKNOWN confidence. No aggregate score.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- | --- |
| temperature_fit_score | — | UNKNOWN | NEEDS_RESEARCH | S-P104-03, S-P104-04 |
| process_electrification_score | 7 | C | AWAITING_HUMAN_REVIEW | S-P104-05 |
| fossil_heat_displacement_score | — | UNKNOWN | NEEDS_RESEARCH | S-P104-03, S-P104-04 |
| motor_drive_score | — | UNKNOWN | NEEDS_RESEARCH | S-P104-03, S-P104-04 |
| power_conversion_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P104-05, S-P104-02 |
| automation_control_score | — | UNKNOWN | NEEDS_RESEARCH | S-P104-03, S-P104-04 |
| scheduling_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P104-03, S-P104-04 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P104-03, S-P104-04 |
| incremental_load_score | — | UNKNOWN | NEEDS_RESEARCH | S-P104-03, S-P104-04 |
| power_quality_score | 3 | C | AWAITING_HUMAN_REVIEW | S-P104-05, S-P104-02 |
| onsite_integration_score | — | UNKNOWN | NEEDS_RESEARCH | S-P104-03, S-P104-04 |
| measures_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P104-03, S-P104-04 |
| management_gap_score | 0 | B | AWAITING_HUMAN_REVIEW | S-P104-06 |
| targets_gap_score | 3 | B | AWAITING_HUMAN_REVIEW | S-P104-04 |
| investment_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P104-03, S-P104-04 |

Exact field rationales/missing facts: data/score_coding_proposals.csv. Certificate bodies and relevant pages visually checked; holder, period, site and product-versus-process scope separated. Frömgen initial HTTP466 subsequently recovered through live HTTP200 primary-body retrieval; owned machining scope reviewed separately. Investment window2021-10-07 to2026-10-07. Previous proposals, canonical numeric/deployment/staff/confidence and actual human-review records preserved. AI first pass is not Anna human review.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| process_electrification_score | 7 | 7 | Geprüft | S-P104-05 |
| power_conversion_score | 5 | 5 | Geprüft | S-P104-05|S-P104-02 |
| power_quality_score | 3 | 1 | Geprüft | S-P104-05|S-P104-02 |
| management_gap_score | 0 | 0 | Geprüft | S-P104-06 |
| targets_gap_score | 3 | 3 | Geprüft | S-P104-04 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

- **power_quality_score**: Own electrochemical production supports possible rectifier-related harmonic/peak relevance as an engineering hypothesis. The source does not establish a specific rectifier inventory/topology, explicit peak constraint or measured disturbance. Use the possible-signal anchor consistently; chemical nickel and product properties are not additional converter evidence.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 10 zuvor offene Felder bearbeitet; 0 zusätzliche Felder quellen- und ankergeprüft; 10 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Owner describes controlled aluminium heat treatment but publishes no operating temperatures, heating carrier or energy powers. Existing certificate assessment remains separate from new plant research.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Owned process operating temperatures and actual heat/cold duties; separate product ratings and room heating. |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Current company/site process heat carrier mix and attributable fossil thermal duty. No public evidence is not zero fossil heat. |
| motor_drive_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Owned electrical motor/compressor inventory, process roles and duty; mechanical drive not automatically electric. |
| automation_control_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Owned process control/monitoring inventory and operational coordination; quality claims not EnMS maturity. |
| scheduling_flex_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Permitted timing shifts, quality/cooling/order constraints and spare capacity. Batch/24h operation alone not flexibility permission. |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Actual useful heat/cold buffer capacity, temperature, connection and timing freedom; thermal mass, room heat and electrical batteries not sufficient. |
| incremental_load_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Owned feasible thermal substitution case and baseline remaining thermal duty; no grid capacity or kW inferred. |
| onsite_integration_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Owned electricity generation/storage/load-management topology; mechanical hydropower, purchased renewables or group assets not inherited. |
| measures_gap_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Named current implemented energy measures with exact entity/site/technology scope. Generic efficient/green production and resource recycling not adequate negative-search proof. |
| investment_gap_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Completed owned energy investments with commissioning dates in 2021-10-07 to 2026-10-07. Operation/report/filename dates, generic annual CAPEX and other group companies not sufficient. |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.
