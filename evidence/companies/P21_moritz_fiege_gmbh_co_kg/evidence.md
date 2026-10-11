# P21 — Privatbrauerei MORITZ FIEGE GmbH & Co. KG

- Public brand: Moritz Fiege
- Legal entity: Privatbrauerei MORITZ FIEGE GmbH & Co. KG
- Manufacturing location: Bochum
- Eligibility decision: INCLUDE (probable SME)
- Review state: RESEARCHED

## Evidence

- `S-P21-01` identifies the sixth-generation family brewery.
- `S-P21-03` reports approximately 90 employees and estimated turnover of EUR
  22.5 million. These figures support provisional SME eligibility.
- `S-P21-02`, an NRW public-agency case, documents an energy- and water-saving
  bottle washer operating in the filling line since 2020.
- The deployment does not prove thermal storage, flexibility or an EnMS.

## Open checks

- Verify the latest filing and ownership structure.
- Research refrigeration, heat supply, heat recovery and production scheduling.

## AI-assisted coding pass — 2026-10-06

The rechecked agency interview `S-P21-02` additionally supports compressors and
heat recovery. `S-P21-04` records carbon accounting; this is not an EnMS claim.
Sector-wide and other breweries' statements are excluded from P21 coding.
Four field-level numeric proposals await Human Review; eleven fields require
research. No deployment facts or canonical scores are auto-updated.


## Quellen- und Anker-Nachprüfung 2026-10-07

Prüfstatus: **Geprüft** für belegte Zahlenvorschläge. Fehlende Belege bleiben `NEEDS_RESEARCH`. Nachprüfer: Codex. Die ursprüngliche Erstbewertung bleibt historisch erhalten; eine persönliche Freigabe oder finale Score-Berechnung ist damit nicht erteilt.

| Feld | Vorher | Nachprüfung | Ergebnis | Quellen |
|---|---:|---:|---|---|
| motor_drive_score | 5 | 5 | Geprüft | S-P21-02 |
| measures_gap_score | 0 | 0 | Geprüft | S-P21-02 | S-P21-04 |
| management_gap_score | 2 | 2 | Geprüft | S-P21-04 |
| targets_gap_score | 3 | 3 | Geprüft | S-P21-02 | S-P21-04 |

Vollständige Entscheidungsspur: `evidence/score_proposal_checks.csv`; aktuelle Abruf-/Inhaltsgrenzen: `evidence/proposal_source_checks.csv`.

## Gesamtrecherche offener Felder – 2026-10-08

Codex: 11 zuvor offene Felder bearbeitet; 0 zusätzliche Felder quellen- und ankergeprüft; 11 weiterhin UNKNOWN. Rechercheumfang: bestehende Sachquellen, gezielte Firmenwebsuche und ausgewählte gefundene Seiten. Keine vollständige Anlageninventur und kein Nachweis fehlender Anlagen.

Multi-brewery research describes generic energy options, not this brewery current fuel balance or deployed thermal storage. Own process improvements lack attributable heat duties and dates.

| Feld | Ergebnis | Beleg / fehlender Nachweis |
|---|---|---|
| temperature_fit_score | Weiter offen / UNKNOWN | Source-linked operating temperatures and a firm-specific technology/temperature fit. |
| process_electrification_score | Weiter offen / UNKNOWN | Firm-specific electric-heat route beyond general process-steam transition intent. |
| fossil_heat_displacement_score | Weiter offen / UNKNOWN | Current fossil energy carrier and significance of fossil process heat at this site. |
| power_conversion_score | Weiter offen / UNKNOWN | Firm-specific rectifier/converter/controlled-electric-heat topology and its materiality. |
| automation_control_score | Weiter offen / UNKNOWN | Documented process controls beyond compact equipment design or carbon accounting. |
| scheduling_flex_score | Weiter offen / UNKNOWN | Current operating schedule, buffer constraints and usable load-shifting capability. |
| thermal_storage_flex_score | Weiter offen / UNKNOWN | Deployed thermal buffer/storage or documented usable thermal inertia, not an intention. |
| incremental_load_score | Weiter offen / UNKNOWN | A current additional electrification route and ordinal incremental-load relevance. |
| power_quality_score | Weiter offen / UNKNOWN | Site-specific harmonics, reactive-power or electrical peak-load evidence. |
| onsite_integration_score | Weiter offen / UNKNOWN | Site-specific PV, storage or load-management integration evidence. |
| investment_gap_score | Weiter offen / UNKNOWN | Dates and scope of qualifying investments within 2021-10-06 to 2026-10-06; historical projects do not close the lookback check. |

Feldspur: `evidence/field_research_all_open_20261008.csv`; Quellenabrufe: `evidence/research_source_attempts_20261008.csv`. Persönliche Freigabe bleibt separat.


## Continued open-field research —2026-10-11

Eigener UIP-Abschlussbericht und2026-Projektbericht verbinden fortbestehende Flaschenwaschmaschine mit historischen Temperatur-, Frequenzpumpen- und Steuerungsdaten. Fünf Felder neu geprüft. Präzises Inbetriebnahmedatum30.11.2018 widerspricht2023-Aussage2020; beide liegen außerhalb des Investitionsfensters.

Nächster Schritt: Heutige Temperaturen, Heizenergieträger und Pumpenkonfiguration, Speicher-/Schaltfenster sowie genaue Daten weiterer Energieinvestitionen verifizieren.

- S-P21-02 — https://www.efa.nrw/aktuell/details/foerderprogramme-belohnen-unternehmen-die-innovativ-sind-interview-mit-marc-zinkler-braumeister-und-betriebsleiter-der-privatbrauerei-moritz-fiege — Operator confirms installed bottle washer, air solar drying, air heat recovery and efficient compressors; recovery/storage transition planned.2020 commissioning statement conflicts with more precise final project report2018 date; both are outside lookback.
- S-P21-04 — https://www.efa.nrw/aktuell/details/projekt-brauerei-der-zukunft-das-rezept-fuer-klimaneutrales-bier — Current project account attributes continuing washer and emissions accounting to Fiege; solar, heat recovery/storage at other breweries are not Fiege deployments. Generic gas-dominant sector is not current Fiege fuel mix.
- S-P21-05 — https://www.umweltinnovationsprogramm.de/sites/default/files/2020-09/moritz_fiege_abschlussbericht_final_03072020.pdf — Exact Fiege project commissioned30November2018, with2019 trials: about83.4-83.5C caustic bath,138C steam, frequency-controlled pumps and implemented automatic pressure/drive reduction. Current2026 project account corroborates continuing washer, not current setpoints/configuration. Historic gas emission factor is not current fuel proof; five-stage recovery is not dispatchable storage.

| Feld | Ergebnis | Beleg / verbleibende Frage |
| --- | --- | --- |
| temperature_fit_score | NEW_EVIDENCE | Own project trial report records an approximately83.4-83.5C caustic bath and138C steam supply. Current project account corroborates continuing washer use. These historical duty temperatures support plausible thermal electrification fit; current setpoints, steam pressure and retrofit design require confirmation. |
| process_electrification_score | NEW_EVIDENCE | Implemented own steam-heated bottle-cleaning line, still attributed to Fiege in2026, supplies one clear conditional thermal electrification case. Heat recovery already reduces demand; no installed electric boiler/heat pump, current fuel mix or complete steam replacement is inferred. |
| fossil_heat_displacement_score | STILL_UNKNOWN | Current fossil energy carrier and significance of fossil process heat at this site. Continuation2026-10-08: Multi-brewery research describes generic energy options, not this brewery current fuel balance or deployed thermal storage. Own process improvements lack attributable heat duties and dates. Vertiefung2026-10-11: Heutige Temperaturen, Heizenergieträger und Pumpenkonfiguration, Speicher-/Schaltfenster sowie genaue Daten weiterer Energieinvestitionen verifizieren. |
| power_conversion_score | NEW_EVIDENCE | Exact own commissioned washer uses frequency-controlled pumps; trial conclusion confirms automatic pressure/drive reduction in reduced-output operation. This is one material converter case.2026 confirms the washer continues, not an unchanged detailed configuration or present ratings. |
| automation_control_score | NEW_EVIDENCE | Own final report confirms implemented automatic pump-pressure/drive reduction and machine measurements during2019 trials; continuing washer is corroborated in2026. Clear machine-control relevance, with current configuration and site-wide energy dispatch unverified. |
| scheduling_flex_score | STILL_UNKNOWN | Current operating schedule, buffer constraints and usable load-shifting capability. Continuation2026-10-08: Multi-brewery research describes generic energy options, not this brewery current fuel balance or deployed thermal storage. Own process improvements lack attributable heat duties and dates. Vertiefung2026-10-11: Heutige Temperaturen, Heizenergieträger und Pumpenkonfiguration, Speicher-/Schaltfenster sowie genaue Daten weiterer Energieinvestitionen verifizieren. |
| thermal_storage_flex_score | STILL_UNKNOWN | Deployed thermal buffer/storage or documented usable thermal inertia, not an intention. Continuation2026-10-08: Multi-brewery research describes generic energy options, not this brewery current fuel balance or deployed thermal storage. Own process improvements lack attributable heat duties and dates. Vertiefung2026-10-11: Heutige Temperaturen, Heizenergieträger und Pumpenkonfiguration, Speicher-/Schaltfenster sowie genaue Daten weiterer Energieinvestitionen verifizieren. |
| incremental_load_score | STILL_UNKNOWN | A current additional electrification route and ordinal incremental-load relevance. Continuation2026-10-08: Multi-brewery research describes generic energy options, not this brewery current fuel balance or deployed thermal storage. Own process improvements lack attributable heat duties and dates. Vertiefung2026-10-11: Heutige Temperaturen, Heizenergieträger und Pumpenkonfiguration, Speicher-/Schaltfenster sowie genaue Daten weiterer Energieinvestitionen verifizieren. |
| power_quality_score | NEW_EVIDENCE | Documented frequency-controlled pumps in the continuing own washer support possible converter-related effects. No present harmonic/reactive-power/voltage or electrical peak measurement supports a higher anchor. |
| onsite_integration_score | STILL_UNKNOWN | Site-specific PV, storage or load-management integration evidence. Continuation2026-10-08: Multi-brewery research describes generic energy options, not this brewery current fuel balance or deployed thermal storage. Own process improvements lack attributable heat duties and dates. Vertiefung2026-10-11: Heutige Temperaturen, Heizenergieträger und Pumpenkonfiguration, Speicher-/Schaltfenster sowie genaue Daten weiterer Energieinvestitionen verifizieren. |
| investment_gap_score | STILL_UNKNOWN | Dates and scope of qualifying investments within 2021-10-06 to 2026-10-06; historical projects do not close the lookback check. Continuation2026-10-08: Multi-brewery research describes generic energy options, not this brewery current fuel balance or deployed thermal storage. Own process improvements lack attributable heat duties and dates. Vertiefung2026-10-11: Heutige Temperaturen, Heizenergieträger und Pumpenkonfiguration, Speicher-/Schaltfenster sowie genaue Daten weiterer Energieinvestitionen verifizieren. |

Geprüft bezeichnet Quellen-/Ankerprüfung durch Codex; keine persönliche oder finale Score-Freigabe.
