# P22 — RIEDENBURGER BRAUHAUS Michael Krieger GmbH & Co. KG

- Public brand: Riedenburger Brauhaus
- Legal entity: RIEDENBURGER BRAUHAUS Michael Krieger GmbH & Co. KG
- Manufacturing location: Riedenburg
- Eligibility decision: INCLUDE (probable SME)
- Review state: RESEARCHED

## Evidence

- `S-P22-01` confirms the exact legal entity and family management.
- `S-P22-03` reports about 40 employees and approximately 30,000 hl annual
  output.
- `S-P22-02` directly documents the new fossil-free process-heat system: own
  PV, heat pumps, waste-heat recovery, vacuum vapour compression and three
  thermal stores. The largest stores about 5,000 kWh in 55,000 litres of water.
- The same source explicitly describes peak reduction and time-shifted energy
  use, supporting deployed flexibility and thermal-storage coding.

## Safeguard

No battery storage is inferred from the documented PV or thermal stores.

## Open checks

- Verify commissioning state after ramp-up of the new brewery.
- Obtain current financial statements and any direct EnMS certificate.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| temperature_fit_score | 10 | 10 | Geprüft | S-P22-02 |
| process_electrification_score | 10 | 10 | Geprüft | S-P22-02 |
| fossil_heat_displacement_score | 5 | UNKNOWN | Recherche nötig | S-P22-02 |
| motor_drive_score | 5 | 5 | Geprüft | S-P22-02 |
| power_conversion_score | 5 | 5 | Geprüft | S-P22-02 |
| automation_control_score | 4 | 4 | Geprüft | S-P22-02 |
| scheduling_flex_score | 8 | 5 | Geprüft | S-P22-02 |
| thermal_storage_flex_score | 7 | 7 | Geprüft | S-P22-02 |
| incremental_load_score | 8 | 8 | Geprüft | S-P22-02 |
| power_quality_score | 1 | 1 | Geprüft | S-P22-02 |
| onsite_integration_score | 3 | 3 | Geprüft | S-P22-02 |
| measures_gap_score | 0 | 7 | Geprüft | S-P22-02 |
| management_gap_score | 5 | 5 | Geprüft | S-P22-01 | S-P22-02 | S-P22-03 |
| targets_gap_score | 3 | 3 | Geprüft | S-P22-02 |
| investment_gap_score | 0 | 3 | Geprüft | S-P22-02 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

- **temperature_fit_score**: The 2026-04-23 primary article describes a planned brewery heat-pump/vacuum-vapour-compression route. This supports strong established technology fit for the named brewery thermal service, not proof of commissioned site operation or an actual reported operating temperature.

- **process_electrification_score**: The primary project describes planned heat pumps and vacuum vapour compression as distinct supported thermal applications. The article says the new energy concept is being built; several proposed use cases are evidenced, but operating deployment is unverified.

- **fossil_heat_displacement_score**: The article describes a future fossil-free new-production concept. Its 500-litre-oil comparison is an energy-equivalent illustration, not the existing plant fossil-fuel baseline. Need actual remaining fossil thermal supply and substitution scope; neither zero nor maximum displacement is established.

- **motor_drive_score**: Planned heat pumps and vapour compression establish a material compressor-drive use case conditional on the named demonstration. Commissioned operation, ratings and several intensive current applications are unverified.

- **power_conversion_score**: The named demonstration combines planned own PV with heat pumps and vapour compression. One material converter/controlled-heat integration case is supported as engineering relevance; actual installed topology and commissioned operation are unverified.

- **automation_control_score**: The planned system explicitly coordinates PV charging, heat storage and process use to reduce peaks. Strong coordinated-control relevance is supported for this design; current operational dispatch is not verified.

- **scheduling_flex_score**: The article explicitly describes charging thermal stores with available PV and supplying the brewery later. This is one clear planned shifting/buffering route; multiple independently usable production-shift windows and commissioned dispatch are not established.

- **thermal_storage_flex_score**: The article describes delivery/installation of two buffer stores and one brewing-water store, including 55,000 litres/about 5,000 kWh for the largest. Substantial multi-use storage relevance is supported for the planned system; fully commissioned operation remains unverified.

- **incremental_load_score**: The source describes central new-brewery thermal demand and multiple planned electrically supplied heat technologies. This supports major ordinal future load-growth relevance IF the design is implemented. It does not establish present electrical demand, a remaining fossil baseline or grid headroom.

- **onsite_integration_score**: The planned design explicitly coordinates own PV, heat pumps, vapour compression and thermal stores. Coordinated onsite-integration fit is supported conditionally; completed deployment is not established by the April 2026 construction article.

- **measures_gap_score**: The article describes a new demonstration under construction and store delivery/installation that week. It does not verify commissioned operation of the full PV/heat-pump/vapour-compression system. Count a concrete pilot/project only, not several completed operational measures.

- **investment_gap_score**: The 2026-04-23 article describes ONE integrated new-brewery demonstration under construction. Its PV, heat pumps, vapour compression and stores are components of that project, not independent completed investments. No commissioning/completion date is verified.
