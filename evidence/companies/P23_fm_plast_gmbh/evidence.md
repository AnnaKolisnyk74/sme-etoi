# P23 — FM-Plast GmbH

- Public brand: FM-Plast
- Legal entity: FM-Plast GmbH
- Manufacturing location: Lennestadt
- Eligibility decision: INCLUDE (probable SME)
- Review state: RESEARCHED

## Evidence

- `S-P23-01` confirms the exact legal entity.
- `S-P23-03` reports about 100 employees and EUR 22 million turnover. The
  Meding acquisition is noted; inclusion remains provisional pending final
  linked-enterprise reconciliation.
- `S-P23-02` documents electric injection-moulding machines, closed-loop mould
  cooling and use of machine waste heat for production and warehouse heating.
- `S-P23-04` is a direct TÜV NORD ISO 50001 certificate valid through 21 May
  2027. Certificate status is `VALID`; operational energy management and heat
  recovery remain coded `YES`.

## Open checks

- Reconcile the acquired entity under the EU linked-enterprise rule.
- Research operating schedule, load management and storage.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| temperature_fit_score | 10 | UNKNOWN | Recherche nötig | S-P23-02 |
| process_electrification_score | 7 | UNKNOWN | Recherche nötig | S-P23-02 |
| motor_drive_score | 5 | 5 | Geprüft | S-P23-02 |
| power_quality_score | 1 | 1 | Geprüft | S-P23-02 |
| measures_gap_score | 0 | 0 | Geprüft | S-P23-02 | S-P23-04 |
| management_gap_score | 0 | 0 | Geprüft | S-P23-04 |
| targets_gap_score | 5 | 3 | Geprüft | S-P23-01 | S-P23-02 | S-P23-04 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

- **temperature_fit_score**: The company documents fully electric injection-machine drives, not an actual process-heating route, operating temperature or remaining thermal substitution duty. Electric drive technology cannot establish process-heat temperature fit or thermal electrification. Need firm-specific thermal equipment/temperature/carrier evidence.

- **process_electrification_score**: The company documents fully electric injection-machine drives, not an actual process-heating route, operating temperature or remaining thermal substitution duty. Electric drive technology cannot establish process-heat temperature fit or thermal electrification. Need firm-specific thermal equipment/temperature/carrier evidence.

- **targets_gap_score**: The inspected own production/environment/energy pages describe an undated efficiency, environmental or lower-emission ambition. No quantified dated roadmap is established. Under the manual, vague ambition is anchor 3; absence of a DATED target is not sufficient for the no-target anchor 5. Internal targets remain unknown.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 10 zuvor offene Felder bearbeitet; 1 zusätzliche Felder quellen- und ankergeprüft; 9 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Own electric injection drives are evidenced. Drives, cooled mould water and hall heat recovery do not establish operating heat temperatures or a usable thermal store; withdrawn heat proposals stay UNKNOWN.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | The company documents fully electric injection-machine drives, not an actual process-heating route, operating temperature or remaining thermal substitution duty. Electric drive technology cannot establish process-heat temperature fit or thermal electrification. Need firm-specific thermal equipment/temperature/carrier evidence. |
| process_electrification_score | Weiter offen / UNKNOWN | The company documents fully electric injection-machine drives, not an actual process-heating route, operating temperature or remaining thermal substitution duty. Electric drive technology cannot establish process-heat temperature fit or thermal electrification. Need firm-specific thermal equipment/temperature/carrier evidence. |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | Current process-heat energy carrier and whether any material fossil thermal service remains at the Lennestadt site |
| power_conversion_score | Geprüft: 5 (C) | S-P23-02 |
| automation_control_score | Weiter offen / UNKNOWN | Firm-specific automation, sensing and coordinated machine/energy-control evidence |
| scheduling_flex_score | Weiter offen / UNKNOWN | Operating schedule, shift pattern and evidence of schedulable injection-moulding production |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | Dedicated thermal/cold storage, buffer capacity or evidence-backed usable thermal inertia |
| incremental_load_score | Weiter offen / UNKNOWN | Defined new electrification pathway or expansion sufficient for ordinal incremental-load relevance |
| onsite_integration_score | Weiter offen / UNKNOWN | Onsite generation, battery storage, microgrid or coordinated load-management evidence |
| investment_gap_score | Weiter offen / UNKNOWN | Dates and scope of recent energy-transition investments or a defined negative investment search over the lookback period |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.
