# P102 — Rudolf Clauss GmbH & Co. KG

## Provisional inclusion

- Process stratum: `metal_surface_heat`
- Process mapping: `PR005` — electroplating; silvering; tinning; zinc coating and hard anodising
- SME status: `probable`; final financial and linked-enterprise review pending
- Independent human review: `PENDING`

## Sources checked

1. [Legal entity / company information](https://www.rudolf-clauss.de/)
2. [Production and process scope](https://www.rudolf-clauss.de/)

## Coding note

The public sources support the legal-entity and process mapping used for provisional sample assembly. They do not establish actual energy consumption, buying intent, grid capacity or deployment of a specific energy solution. Certificate searches are recorded as `NOT_FOUND_AFTER_CHECK`; this means only that no direct public evidence was located in the defined check, not that a certificate or deployment does not exist.


## Completion to 100-company field assessment — 2026-10-07

NBCC-2026-10-07-07: selection frozen before enrichment. Final16 ranked eligible coding candidates; rank is documentary information gain, not score.

- S-P102-03: https://www.rudolf-clauss.de/de/nachhaltigkeit/ — Owner environmental statements distinguish own galvanic finishing from downstream lighter-product/customer fuel benefits. Those customer benefits are not owner energy savings, owned PV or completed energy projects.

All15 fields assessed: 2 numeric proposals awaiting actual human review; 13 blank NEEDS_RESEARCH fields with UNKNOWN confidence. No aggregate score.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- | --- |
| temperature_fit_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |
| process_electrification_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |
| fossil_heat_displacement_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |
| motor_drive_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |
| power_conversion_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P102-02 |
| automation_control_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |
| scheduling_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |
| incremental_load_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |
| power_quality_score | 3 | C | AWAITING_HUMAN_REVIEW | S-P102-02 |
| onsite_integration_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |
| measures_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |
| management_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |
| targets_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |
| investment_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P102-03 |

Exact field rationales/missing facts: data/score_coding_proposals.csv. Certificate bodies and relevant pages visually checked; holder, period, site and product-versus-process scope separated. Frömgen initial HTTP466 subsequently recovered through live HTTP200 primary-body retrieval; owned machining scope reviewed separately. Investment window2021-10-07 to2026-10-07. Previous proposals, canonical numeric/deployment/staff/confidence and actual human-review records preserved. AI first pass is not Anna human review.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| power_conversion_score | 5 | 5 | Geprüft | S-P102-02 |
| power_quality_score | 3 | 1 | Geprüft | S-P102-02 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

- **power_quality_score**: Own electrochemical production supports possible rectifier-related harmonic/peak relevance as an engineering hypothesis. The source does not establish a specific rectifier inventory/topology, explicit peak constraint or measured disturbance. Use the possible-signal anchor consistently; chemical nickel and product properties are not additional converter evidence.
