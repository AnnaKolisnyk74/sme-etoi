# Coding manual v0.2

## Core rule

Code only what a source supports. Use `unknown` rather than zero when a field
has not been researched. Every numeric score requires a concise justification
in `evidence_note` and supporting links in `source_urls`.

Never convert process descriptions into invented kW, MW, MWh, temperature,
connection voltage or savings values.

## Company identity and naming

The exact legal-entity name is the primary company identifier for all pilot and
main-sample records.

1. Copy the legal name, including its legal form, from the official company
   imprint (`Impressum`).
2. Verify it against an official company or commercial-register source whenever
   the imprint is ambiguous, outdated or inconsistent.
3. Store the legal name in `legal_entity` and the public brand or commonly used
   market name separately in `company_name`.
4. Treat plant names, shops, product brands and campaign names as site or brand
   attributes, not as separate companies, unless a distinct legal entity is
   documented.
5. Record the manufacturing site separately from the registered office when
   they differ.
6. Apply this rule consistently to all 20 pilot records and all 100 main-sample
   records.

Example: `Burgis GmbH` is the legal entity; `Burgis` or `Burgis Knödelliebe` is
the public brand; `Knödel-Retter Werksverkauf` is a shop/site designation.

## Search sequence

1. Resolve the legal entity, manufacturing location and group relationship.
2. Verify SME eligibility using employees plus turnover or balance-sheet data.
3. Identify actual production processes, equipment and operating pattern.
4. Record temperature information only where a source provides it; otherwise
   use a documented sector/process range and label it as secondary evidence.
5. Search for motors, pumps, fans, compressors, rectifiers, ovens, kilns,
   refrigeration, thermal storage, buffers and batch scheduling.
6. Search for PV, storage, heat recovery, heat pumps, electric process heat,
   energy management, demand response and power-quality measures.
7. Check ISO 50001 and EMAS evidence in appropriate sources.
8. Record dates, URLs, evidence excerpts and unresolved conflicts.

Suggested German search terms include `Prozesswärme`, `Temperatur`, `Ofen`,
`Brennofen`, `Sinter`, `Galvanik`, `Gleichrichter`, `Spritzguss`, `Extrusion`,
`Kälte`, `Dampf`, `Druckluft`, `Frequenzumrichter`, `Lastmanagement`,
`Blindleistung`, `Oberschwingungen`, `Photovoltaik`, `Abwärme`, `Wärmepumpe`,
`Elektrifizierung`, `Speicher`, `ISO 50001`, `EMAS` and `Investition`.

## Numeric anchors

Use integers. Intermediate values are permitted only when the evidence clearly
falls between anchors.

### Process-electrification potential

- `temperature_fit_score` (0/3/7/10): no fit known, difficult/uncertain,
  technically plausible, or strong established fit.
- `process_electrification_score` (0/3/7/10): no relevant process evidence,
  secondary-sector indication, one clear firm-specific use case, or multiple
  strongly supported use cases.
- `fossil_heat_displacement_score` (0/2/4/5): none known, possible, material,
  or central thermal service with substitution potential.

### Power-electronics relevance

- `motor_drive_score` (0/2/5/8): negligible, limited, material, or multiple
  intensive drive applications.
- `power_conversion_score` (0/2/5/8): no known case, limited, one material case,
  or several central rectifier/converter/controlled-heat applications.
- `automation_control_score` (0/1/3/4): negligible, limited, clear, or strong
  coordinated-control relevance.

### Load-flexibility potential

- `scheduling_flex_score` (0/2/5/8): continuous and inflexible, weak,
  schedulable/buffered, or several strong shifting options.
- `thermal_storage_flex_score` (0/2/5/7): none known, weak, clear cold/heat
  buffer, or substantial multi-use thermal flexibility.

### Grid and power-quality relevance

- `incremental_load_score` (0/2/5/8): negligible, limited, material, or major
  ordinal load-growth relevance if identified processes electrify.
- `power_quality_score` (0/1/3/4): negligible, possible, clear, or multiple
  strong harmonic/reactive-power/peak-load signals.
- `onsite_integration_score` (0/1/2/3): no fit known, possible, one clear use
  case, or coordinated PV/storage/microgrid/load-management fit.

### Publicly observed transition gap

Gap scores may be assigned only after the corresponding source checks.

- `measures_gap_score` (0/3/7/10): several measures, some measures,
  intentions/pilots only, or no concrete measure found after adequate search.
- `management_gap_score` (0/2/3/5): verified mature system, partial/other
  system, unverified claim, or no evidence after defined checks.
- `targets_gap_score` (0/2/3/5): dated target plus roadmap, dated target only,
  vague ambition, or no target found after adequate search.
- `investment_gap_score` (0/2/3/5): several recent investments, one,
  announcement/pilot only, or none found in the lookback period.

## Status fields

- `sme_status`: `confirmed`, `probable`, `uncertain`, `excluded`
- `group_check`: `independent`, `partner_or_linked_sme`, `large_group`, `unknown`
- source checks: `1` checked, `0` not checked
- `latest_evidence_date`: ISO date `YYYY-MM-DD`
- multiple URLs: separated by ` | `

## Conflict rule

Record both conflicting sources. Prefer the more authoritative, direct and
recent source and explain the choice. Do not average conflicting facts.
