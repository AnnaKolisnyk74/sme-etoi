# P10 — Oskar Lehmann GmbH & Co. KG

## Identity

- **Public/market name:** Oskar Lehmann / OL
- **Legal entity:** Oskar Lehmann GmbH & Co. KG
- **Registered office and manufacturing site:** Alte Chaussee 59–70,
  32825 Blomberg-Donop, Germany
- **Register:** Amtsgericht Lemgo, HRA 3897
- **General partner:** Oskar Lehmann Beteiligungs GmbH, Amtsgericht Lemgo,
  HRB 5257
- **Identity source:** [Official imprint](https://www.oskar-lehmann.de/en/imprint.html)
  — `S-P10-01`.

## EU SME eligibility

**Current decision:** `INCLUDE` (provisional)  
**SME status:** `probable`  
**Group check:** `partner_or_linked_sme`

The published 2023 annual-report text reports an average of 231 employees and
EUR 36.499 million revenue (`S-P10-04`). Both figures are below the basic EU
SME ceilings. The company is nevertheless close to the 250-employee threshold
and the report describes an operating-company split. The general partner and
other related Lehmann entities therefore require final aggregation before the
pilot methodology is frozen.

The provisional inclusion is suitable for pilot coding but is not a final
legal determination of SME status.

## Process evidence

The company describes a vertically integrated production chain with development,
toolmaking, injection moulding, assembly and logistics (`S-P10-02` and
`S-P10-03`). Firm-specific scale signals include:

- more than 100 injection-moulding machines with clamping forces from 100 to
  5,500 kN;
- processing of more than 2,000 tonnes of thermoplastics annually;
- three-shift production;
- conventional, gas-assisted, two-component and hybrid injection moulding;
- CNC machining, robotics and operating-data collection;
- internal toolmaking, SLS prototyping, assembly and selected surface finishing.

These observations support strong relevance for motor drives, controlled
electric heating, cooling, automation and power conversion. They do not establish
actual site demand, peak load, power quality or remaining fossil-heat use.

## Existing transition measures

Public evidence identifies:

- a company-hosted 2019 technical report naming an internal
  energy-management officer and documenting internal evaluations of energy
  savings from new servo-driven injection-moulding equipment (`S-P10-08`);
- historical participation in Energieeffizienz-Netzwerk LEEN OWL II with a
  company statement that saved energy costs had resulted (`S-P10-09`);
- a BDE system used to monitor machine availability, production flows and
  process data; this is not coded as an energy-management or load-management
  system without direct evidence (`S-P10-08`);
- process-efficiency and automation improvements in the 2023 management report;
- reuse of internal plastic waste and purchased recycled materials
  (`S-P10-07`);
- development and use of bio-based plastics;
- participation as an initial signatory in the IHK initiative
  “gemeinsam klimaneutral 2030” (`S-P10-06`).

No quantified site-energy reduction, PV capacity, heat recovery, heat pump,
battery storage, demand response, renewable-electricity share or measured
CO2 result was located in the reviewed source set. The 2023 report records
EUR 153 thousand of investment, but does not identify it as a decarbonisation
investment.

## Certificate review

The [official download page](https://www.oskar-lehmann.de/en/download-en.html)
lists ISO 9001, IATF 16949, recycling and material-compliance documents. The
mandatory energy-transition certificate checks produced:

- **ISO 50001 — `NOT_FOUND_AFTER_CHECK`**
- **ISO 14001 — `NOT_FOUND_AFTER_CHECK`**
- **EMAS — `NOT_FOUND_AFTER_CHECK`**

No direct public certificate or authoritative register entry for these three
systems was located on the official site or in exact-legal-name searches on
12 September 2026. This is absence of public evidence, not proof that the
company has no such certification. The auditable rows are stored in
`evidence/certificate_register.csv`.

## Provisional SME-ETOI coding

| Dimension | Score | Rationale |
| --- | ---: | --- |
| Process-electrification potential | 16/25 | Injection moulding, toolmaking and cooling provide clear electric-process relevance; no material fossil process-heat displacement is documented. |
| Power-electronics relevance | 20/20 | More than 100 moulding machines, CNC equipment, robotics and automated data collection create multiple strong drive and conversion signals. |
| Load-flexibility potential | 7/15 | Many parallel machines and three-shift operation suggest scheduling options; no thermal storage is documented. |
| Grid and power-quality relevance | 8/15 | Numerous controlled loads create power-quality and onsite-integration relevance, but major incremental electrification load is not established. |
| Publicly observed transition gap | 19/25 | A 2030 initiative and material-circularity measures are visible, but quantified energy measures, current ISO 50001/14001/EMAS evidence and relevant investment proof are absent. |
| **Total** | **70/100** | **Provisional band: HIGH** |

Evidence coverage is 100% across the company website, public annual-report
text, identity/register information, certification source and credible
independent sources. With the latest precisely dated material used for the
automated confidence calculation from 7 March 2024, the provisional confidence
grade is **B** as of 12 September 2026.

The score is a transparent public-data classification. It is not a purchasing
prediction and does not estimate site load.

## Interpretation for energy-solution providers

P10 is a potentially meaningful industrial case for machine-level energy
monitoring, drive and hydraulic-system optimisation, process cooling, peak-load
management, power-quality analysis and coordinated onsite generation or storage.
The strongest research finding is the contrast between very specific production
scale and comparatively sparse public disclosure of quantified energy measures.

## Open questions

1. What are the aggregated employees, turnover and balance-sheet total of all
   linked or partner Lehmann entities?
2. Which injection-moulding machines are hydraulic, hybrid or fully electric?
3. What are the site's measured baseload, peak load and cooling demand?
4. Are PV, heat recovery, storage or load-management systems already operating
   but not publicly disclosed?
5. Does a non-public or successor ISO 50001, ISO 14001 or EMAS record exist?

## Research Queue checks — 2026-09-13

### Energy management

Task `RQ-P10-EMS-20260913` found positive historical energy-management
activity: an internal energy-management officer, energy-saving evaluations and
LEEN participation (`S-P10-08`, `S-P10-09`). The current official certificate
index and exact-legal-name searches did not establish a valid ISO 50001
certificate or a clearly defined operational EnMS.

Result: `PARTIAL_EVIDENCE`; `energy_management_deployed` remains `UNKNOWN`.
An energy-management role or activity is not treated as proof of a deployed
system or certification.

### Flexibility

Task `RQ-P10-FLEX-20260913` checked the official website and news archive, the
company-hosted technical report, exact-name searches and energy-efficiency
network sources. The BDE system, LEEN participation and three-shift production
do not demonstrate load management, demand response, flexibility-market
participation or controllable-load operation.

Result: `NOT_FOUND_AFTER_CHECK`; `flexibility_solution_deployed` remains
`UNKNOWN`. Recheck both tasks by 2027-03-13.

## Review

- Research status: `RESEARCHED`
- User review: `NOT_REVIEWED`
- Research date: 2026-09-12


## Completion to 100-company field assessment — 2026-10-07

GATE-ASSESS-2026-10-07: selection frozen before enrichment. Documentary scope only; upstream group gate retained and canonical score remains blocked.


All15 fields assessed: 4 numeric proposals awaiting actual human review; 11 blank NEEDS_RESEARCH fields with UNKNOWN confidence. No aggregate score.

| Field | Proposal | Confidence | Status | Sources |
| --- | ---: | --- | --- | --- | --- |
| temperature_fit_score | — | UNKNOWN | NEEDS_RESEARCH | S-P10-01, S-P10-02 |
| process_electrification_score | — | UNKNOWN | NEEDS_RESEARCH | S-P10-01, S-P10-02 |
| fossil_heat_displacement_score | — | UNKNOWN | NEEDS_RESEARCH | S-P10-01, S-P10-02 |
| motor_drive_score | 5 | C | AWAITING_HUMAN_REVIEW | S-P10-02, S-P10-03 |
| power_conversion_score | 2 | C | AWAITING_HUMAN_REVIEW | S-P10-08 |
| automation_control_score | 4 | B | AWAITING_HUMAN_REVIEW | S-P10-03 |
| scheduling_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P10-01, S-P10-02 |
| thermal_storage_flex_score | — | UNKNOWN | NEEDS_RESEARCH | S-P10-01, S-P10-02 |
| incremental_load_score | — | UNKNOWN | NEEDS_RESEARCH | S-P10-01, S-P10-02 |
| power_quality_score | — | UNKNOWN | NEEDS_RESEARCH | S-P10-01, S-P10-02 |
| onsite_integration_score | — | UNKNOWN | NEEDS_RESEARCH | S-P10-01, S-P10-02 |
| measures_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P10-01, S-P10-02 |
| management_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P10-01, S-P10-02 |
| targets_gap_score | 2 | B | AWAITING_HUMAN_REVIEW | S-P10-06 |
| investment_gap_score | — | UNKNOWN | NEEDS_RESEARCH | S-P10-01, S-P10-02 |

Exact field rationales/missing facts: data/score_coding_proposals.csv. Certificate bodies and relevant pages visually checked; holder, period, site and product-versus-process scope separated. Frömgen initial HTTP466 subsequently recovered through live HTTP200 primary-body retrieval; owned machining scope reviewed separately. Investment window2021-10-07 to2026-10-07. Previous proposals, canonical numeric/deployment/staff/confidence and actual human-review records preserved. AI first pass is not Anna human review.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| motor_drive_score | 5 | 5 | Geprüft | S-P10-02|S-P10-03 |
| power_conversion_score | 2 | 2 | Geprüft | S-P10-08 |
| automation_control_score | 4 | 4 | Geprüft | S-P10-03 |
| targets_gap_score | 2 | 2 | Geprüft | S-P10-06 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.


## Offene Felder: Recherche 2026-10-08

Prüfer: Codex. Status **Geprüft** bedeutet Quellen- und Ankerprüfung; persönliche Freigabe bleibt separat.

| Feld | Ergebnis | Belege |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | S-P10-10 |
| process_electrification_score | Weiter offen / UNKNOWN | S-P10-10 |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | S-P10-10 |
| scheduling_flex_score | Weiter offen / UNKNOWN | S-P10-10 |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | S-P10-10 |
| incremental_load_score | Weiter offen / UNKNOWN | S-P10-10 |
| power_quality_score | Weiter offen / UNKNOWN | S-P10-10 |
| onsite_integration_score | Weiter offen / UNKNOWN | S-P10-10 |
| measures_gap_score | Weiter offen / UNKNOWN | S-P10-10 |
| management_gap_score | Weiter offen / UNKNOWN | S-P10-10 |
| investment_gap_score | Weiter offen / UNKNOWN | S-P10-10 |

Owner news archive was inspected. No new owned thermal carrier, onsite generation, current system maturity or energy-project commissioning proof found. Historical LEEN participation/2019 drives are not updated into current energy deployment; upstream SME gate remains open.

Feldweise Spur: `evidence/field_research_20261008.csv`; aktuelle Werte: `data/score_coding_proposals.csv`.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 11 zuvor offene Felder bearbeitet; 0 zusätzliche Felder quellen- und ankergeprüft; 11 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Own news archive supplies no new heat carrier, store or dated energy project. Historical LEEN/drives are not a current management certificate or complete plant inventory; SME gate remains separate.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Owned process operating temperatures and actual heat/cold duties; separate product ratings and room heating. |
| process_electrification_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Named owned thermal route, current heat carrier and feasible remaining substitution case; separate electric drives and room heat. |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Current company/site process heat carrier mix and attributable fossil thermal duty. No public evidence is not zero fossil heat. |
| scheduling_flex_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Permitted timing shifts, quality/cooling/order constraints and spare capacity. Batch/24h operation alone not flexibility permission. |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Actual useful heat/cold buffer capacity, temperature, connection and timing freedom; thermal mass, room heat and electrical batteries not sufficient. |
| incremental_load_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Owned feasible thermal substitution case and baseline remaining thermal duty; no grid capacity or kW inferred. |
| power_quality_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Owned relevant converter/peak topology or measured harmonic/reactive/voltage findings; product resistance/current amps not measured power-quality evidence. |
| onsite_integration_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Owned electricity generation/storage/load-management topology; mechanical hydropower, purchased renewables or group assets not inherited. |
| measures_gap_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Named current implemented energy measures with exact entity/site/technology scope. Generic efficient/green production and resource recycling not adequate negative-search proof. |
| management_gap_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Current direct ISO 50001/14001/EMAS or operational energy-management evidence for exact holder; quality-only and absent public certificate not no-management conclusion. |
| investment_gap_score | Weiter offen / UNKNOWN | Documentary first pass only: upstream group eligibility remains OPEN_GATE; no canonical scoring or human approval. Completed owned energy investments with commissioning dates in 2021-10-07 to 2026-10-07. Operation/report/filename dates, generic annual CAPEX and other group companies not sufficient. |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.


## Vertiefte Entscheidungsrecherche — 2026-10-08

Komplementär-GmbH ist belegt. Einzelgesellschafts-Umsatz und Mitarbeiterzahl ersetzen keine vollständige Partner-/Verbundaggregation.

**Ergebnis:** AGGREGATION_OPEN. **Nächster Schritt:** Anteile der KG und Beteiligungs-GmbH, weitere verbundene Firmen und gleichperiodige aggregierte Zahlen beschaffen.

- S-P10-01: https://www.oskar-lehmann.de/en/imprint.html — KG HRA 3897 und persönlich haftende Oskar Lehmann Beteiligungs GmbH HRB 5257; Managementnamen belegen keine vollständigen Eigentumsquoten.

Quellenprüfung durch Codex. Geprüfte Feldvorschläge sind keine finale Score-Freigabe. Nicht belegte Felder bleiben UNKNOWN.
