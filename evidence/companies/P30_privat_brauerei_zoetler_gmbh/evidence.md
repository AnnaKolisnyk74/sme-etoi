# P30 — Privat-Brauerei Zötler GmbH

## Inclusion status

- Batch: 02 (companies 21-40 of the planned 100-company final study)
- Process stratum: `food_beverage`
- SME status: `probable`; final financial and linked-enterprise review remains open
- Independent human source review: `PENDING`

## Supported process relevance

The checked public evidence supports **brewing; boiling; fermentation; maturation and filling**. The company is mapped to `PR003` for technical screening. This mapping does not prove a specific energy technology is installed and does not imply buying intent.

## Certificates and deployments

- ISO 50001: `NOT_FOUND_AFTER_CHECK`
- ISO 14001: `NOT_FOUND_AFTER_CHECK`
- EMAS: `DOCUMENT_FOUND_VALIDITY_UNCLEAR`
- Unverified deployment fields remain `UNKNOWN`.
- `NOT_FOUND_AFTER_CHECK` means only that no public direct evidence was located in the defined check.

## Sources

- `S-P30-01` — [Privat-Brauerei Zötler: Impressum](https://www.familien-braukunst.de/impressum/) — Exact legal entity and production location.
- `S-P30-02` — [Privat-Brauerei Zötler: Quality and sustainability](https://www.zoetler.de/) — Brewing and EMAS company statement; registration validity open.

## AI first-pass coding — 2026-10-06

Frozen selection: `NBCC-2026-10-06-02`, rank 1, v2 policy, B/B confidence,
QA PASS, HIGH documentary gain. This is automated selection, not Anna's review.

- `S-P30-03` — [Quality and environment](https://www.zoetler.de/qualitaet-und-umwelt.html): company energy measures and EMAS claim. The linked 2023 report returned HTTP 404; current validity remains unresolved.
- `S-P30-04` — [Maturation cellar](https://www.zoetler.de/reifekeller.html): 2025 completion and individually controlled jacket cooling; no independently verified savings or usable load shifting.
- `S-P30-05` — [Brewing motivation](https://www.zoetler.de/motivation.html): individual brews and fermentation/maturation durations, not a proven thermal buffer.

Seven proposals cover control, weak scheduling, one onsite use case, observed
measures, unresolved management validity, vague targets and one dated investment.
All remain `AWAITING_HUMAN_REVIEW`; reviewer and review date are blank.
Eight fields remain `NEEDS_RESEARCH`: temperature fit, process electrification,
fossil-heat displacement, motors, power conversion, thermal storage,
incremental load and power quality. Their values remain blank, confidence UNKNOWN.
No canonical deployments, certification records or scores are changed.

## Remaining limitations after coding

The legal entity and process are supported, but complete financial aggregation, ownership links, certification validity and site-level energy deployments remain subject to Anna's final review after the 100-company sample is assembled.


## Public-source retrieval audit — 2026-10-06 (AI first pass)

- Original: https://www.zoetler.de/download/zoetler-nachhaltigkeitsbericht_emas2023.pdf — NO_EQUIVALENT_FOUND. Replacement/context IDs: `S-P30-03`. Reachable company sustainability page states that declaration is being revised; only company EMAS claim remains. Open: Direct current environmental statement and registration validity remain unresolved.

See `evidence/source_link_audit.csv` for GET status and `evidence/source_recovery.csv` for exact scope. Retrieval/recovery is not Anna's Human Review; scores, certificate validity and deployment UNKNOWNs are unchanged.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| automation_control_score | 3 | 3 | Geprüft | S-P30-04 |
| scheduling_flex_score | 2 | 2 | Geprüft | S-P30-05 |
| onsite_integration_score | 2 | 2 | Geprüft | S-P30-03 |
| measures_gap_score | 3 | 3 | Geprüft | S-P30-03 | S-P30-04 |
| management_gap_score | 3 | 3 | Geprüft | S-P30-03 |
| targets_gap_score | 3 | 3 | Geprüft | S-P30-03 |
| investment_gap_score | 2 | 2 | Geprüft | S-P30-04 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 8 zuvor offene Felder bearbeitet; 0 zusätzliche Felder quellen- und ankergeprüft; 8 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Fermentation/cold maturation descriptions do not establish heat-process temperatures or an independently usable dispatchable thermal store.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | A company-specific electric-heat technology/temperature fit; cold maturation temperatures alone do not establish process-heat electrification fit. |
| process_electrification_score | Weiter offen / UNKNOWN | A firm-specific industrial electric-heat route; efficient cooling, biomass heat and electric logistics do not prove such a route. |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | Fuel and materiality of remaining fossil process heat; an unspecified CHP fuel cannot be assumed fossil. |
| motor_drive_score | Weiter offen / UNKNOWN | Firm-specific motor/compressor equipment and application intensity, beyond cooled tanks and unspecified refrigeration supply. |
| power_conversion_score | Weiter offen / UNKNOWN | Rectifier/converter/controlled-heat equipment topology and materiality; PV existence alone does not document production conversion equipment. |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | A controllable heat/cold buffer or documented usable thermal inertia respecting product-quality constraints; maturation duration is not a storage-service proof. |
| incremental_load_score | Weiter offen / UNKNOWN | An identified additional industrial electrification route and ordinal incremental-load relevance; EVs do not establish a process-heat route. |
| power_quality_score | Weiter offen / UNKNOWN | Documented harmonic/reactive-power/peak-load signals or relevant electrical topology; renewable supply alone is insufficient. |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.
