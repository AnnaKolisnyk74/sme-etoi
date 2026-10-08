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
