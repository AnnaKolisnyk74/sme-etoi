# P31 — Brauerei Clemens Härle KG

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
- EMAS: `NOT_FOUND_AFTER_CHECK`
- Unverified deployment fields remain `UNKNOWN`.
- `NOT_FOUND_AFTER_CHECK` means only that no public direct evidence was located in the defined check.

## Sources

- `S-P31-01` — [Brauerei Clemens Härle: Impressum](https://www.haerle.de/impressum) — Exact legal entity and production location.
- `S-P31-02` — [Baden-Württemberg Ministry of the Environment: Environmental award 2024: Brauerei Clemens Härle](https://um.baden-wuerttemberg.de/de/umwelt-natur/umwelt-und-wirtschaft/angebote-fuer-unternehmen/umweltpreis-fuer-unternehmen/umweltpreis-2024/brauerei-clemens-haerle) — Beer production, family ownership and renewable-energy measures.

## AI first-pass coding — 2026-10-06

Frozen selection: `NBCC-2026-10-06-02`, rank 2, v2 policy, B/B confidence,
QA PASS, HIGH documentary gain. This is automated selection, not Anna's review.

- `S-P31-02` was rechecked: the 2024 state agency case supports the documented wood/biogas heat baseline, a partial KLIMAWIN framework and the 2028 electricity self-sufficiency target.
- `S-P31-03` — [Green energy](https://www.haerle.de/die-gruene-brauerei/wir-arbeiten-mit-gruener-energie): company heat/PV and electric delivery trucks dated July 2023 and September 2026; vehicle electrification is not electric process heat.
- `S-P31-04` — [Brewing process](https://www.haerle.de/das-herzstueck/so-brauen-wir): heat efficiency and fermentation/maturation temperatures and durations, not equipment topology or usable load shifting.

Seven proposals cover fossil displacement for the documented renewable baseline,
weak scheduling, onsite PV, several observed measures, partial management,
a dated target and recent investments. All remain `AWAITING_HUMAN_REVIEW`;
reviewer and review date are blank. The zero fossil-displacement proposal rests
on positive baseline evidence, not an absence of public deployment evidence.
Eight fields remain `NEEDS_RESEARCH`: temperature fit, process electrification,
motors, power conversion, control topology, thermal storage, incremental load
and power quality. Their values remain blank, confidence UNKNOWN. No canonical
deployments, certification records or scores are changed.

## Remaining limitations after coding

The legal entity and process are supported, but complete financial aggregation, ownership links, certification validity and site-level energy deployments remain subject to Anna's final review after the 100-company sample is assembled.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| fossil_heat_displacement_score | 0 | 0 | Geprüft | S-P31-02 |
| scheduling_flex_score | 2 | 2 | Geprüft | S-P31-04 |
| onsite_integration_score | 2 | 2 | Geprüft | S-P31-03 |
| measures_gap_score | 0 | 0 | Geprüft | S-P31-02 | S-P31-03 | S-P31-04 |
| management_gap_score | 2 | 2 | Geprüft | S-P31-02 |
| targets_gap_score | 2 | 2 | Geprüft | S-P31-02 |
| investment_gap_score | 0 | 0 | Geprüft | S-P31-03 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 8 zuvor offene Felder bearbeitet; 0 zusätzliche Felder quellen- und ankergeprüft; 8 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Existing biomass/biogas/PV facts retained. Cold fermentation temperature is not thermal electrification fit; no additional drive inventory or useful thermal store identified.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | A company-specific electric-heat technology/temperature fit; cold maturation temperatures alone do not establish process-heat electrification fit. |
| process_electrification_score | Weiter offen / UNKNOWN | A firm-specific industrial electric-heat route; efficient cooling, biomass heat and electric logistics do not prove such a route. |
| motor_drive_score | Weiter offen / UNKNOWN | Firm-specific motor/compressor equipment and application intensity, beyond cooled tanks and unspecified refrigeration supply. |
| power_conversion_score | Weiter offen / UNKNOWN | Rectifier/converter/controlled-heat equipment topology and materiality; PV existence alone does not document production conversion equipment. |
| automation_control_score | Weiter offen / UNKNOWN | Firm-specific process automation or control equipment; manual quality checks and climate-framework participation are insufficient. |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | A controllable heat/cold buffer or documented usable thermal inertia respecting product-quality constraints; maturation duration is not a storage-service proof. |
| incremental_load_score | Weiter offen / UNKNOWN | An identified additional industrial electrification route and ordinal incremental-load relevance; EVs do not establish a process-heat route. |
| power_quality_score | Weiter offen / UNKNOWN | Documented harmonic/reactive-power/peak-load signals or relevant electrical topology; renewable supply alone is insufficient. |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.
