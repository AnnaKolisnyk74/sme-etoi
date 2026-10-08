# P04 — Neumarkter Lammsbräu Gebr. Ehrnsperger KG

- Public brand: Neumarkter Lammsbräu
- Legal entity: Neumarkter Lammsbräu Gebr. Ehrnsperger KG
- Manufacturing location: Neumarkt in der Oberpfalz
- Eligibility decision: INCLUDE (probable SME)
- Review state: RESEARCHED

## Evidence

- `S-P04-01` establishes the exact legal entity, address and register identity.
- `S-P04-02` reports 142 employees and EUR 31.7 million turnover for 2024.
- Public company information describes the business as family-owned.
- `S-P04-06`, the official 2023 sustainability report with integrated EMAS
  declaration, documents the brewing, malting and cooling processes; an
  operational energy-management system and software; 125 kWp PV; and a
  predominantly gas-based heat supply.
- The same report documents a 42% Scope 1 and 2 reduction target by 2030 and
  plans to electrify heat supply using, among other measures, heat pumps and
  solar systems. Planned measures are not coded as deployed.

## Certificate review

- **ISO 50001 — `NOT_FOUND_AFTER_CHECK`:** no direct public certificate or
  official register entry was located in the defined checks. This is not proof
  that no certification exists.
- **ISO 14001 — `EXPIRED`:** the
  [direct certificate](https://www.lammsbraeu.de/hubfs/NeumarkterLammsbraeu/blog/images/2022/2022%20-%20Blog%20-%20Zertifizierungen/Zert._2022-06-02_Re-ZA%2014k_Neumarkter%20Lammsbr%C3%A4u.pdf)
  is certificate UG0573-2022, issued by Intechnica Cert GmbH and valid only
  through 2 June 2025. No current successor was located.
- **EMAS — `DOCUMENT_FOUND_VALIDITY_UNCLEAR`:** the
  [official certificate page](https://www.lammsbraeu.de/blog/unsere-zertifizierungen)
  states EMAS participation and links a
  [direct EMAS document](https://www.lammsbraeu.de/hubfs/NeumarkterLammsbraeu/blog/images/2022/2022%20-%20Blog%20-%20Zertifizierungen/IHK%20Urkunde%20EMAS.pdf);
  exact current validity metadata could not be established.

The supporting sources are recorded as `S-P04-03` to `S-P04-05`.

## Open checks

- Verify linked entities in the official register before final approval.
- Verify current EMAS and ISO 14001 validity metadata.
- Verify whether planned heat-electrification measures have been commissioned.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| temperature_fit_score | 10 | 10 | Geprüft | S-P04-06 |
| process_electrification_score | 7 | 7 | Geprüft | S-P04-06 |
| fossil_heat_displacement_score | 5 | 5 | Geprüft | S-P04-06 |
| motor_drive_score | 5 | 5 | Geprüft | S-P04-06 |
| power_conversion_score | 5 | 5 | Geprüft | S-P04-06 |
| automation_control_score | 4 | 4 | Geprüft | S-P04-06 |
| scheduling_flex_score | 5 | 2 | Geprüft | S-P04-06 |
| thermal_storage_flex_score | 2 | UNKNOWN | Recherche nötig | S-P04-06 |
| incremental_load_score | 5 | 5 | Geprüft | S-P04-06 |
| power_quality_score | 1 | 1 | Geprüft | S-P04-06 |
| onsite_integration_score | 2 | 2 | Geprüft | S-P04-06 |
| measures_gap_score | 0 | 0 | Geprüft | S-P04-06 |
| management_gap_score | 2 | 2 | Geprüft | S-P04-03 | S-P04-04 | S-P04-05 | S-P04-06 |
| targets_gap_score | 0 | 0 | Geprüft | S-P04-06 |
| investment_gap_score | 0 | 2 | Geprüft | S-P04-06 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

- **scheduling_flex_score**: Discrete production stages or batch processing support only a weak sequencing hypothesis. The cited source does not establish spare capacity, safe interruption, dispatch permission or a usable shifting window.

- **thermal_storage_flex_score**: Central refrigeration and cooled beer storage do not establish an available thermal buffer for shifting electrical demand. Need a named usable heat/cold store, operating window and quality constraints.

- **investment_gap_score**: The 2023 report documents completed rooftop PV in 2023. Solar-thermal installation is beginning/planned; the malt-house energy upgrade is dated only 2021, without a commissioning month inside the strict 2021-10-07 to 2026-10-07 window. Count one safely dated completed project, not planned assets or an unbounded 2021 date.
