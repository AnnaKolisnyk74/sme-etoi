# Coding manual v0.1

## Core rule

Code only what a source supports. Use `unknown` rather than zero when a field has not been researched. Numeric score fields must include a short justification in `evidence_note` and supporting links in `source_urls`.

## Search sequence per company

1. Resolve legal entity, location, activity and group relationship.
2. Check probable SME status using employees plus turnover or balance-sheet evidence.
3. Identify manufacturing processes and scale indicators.
4. Search the company website and reports for energy, heat, cold, compressed air, PV, storage, heat recovery, electrification and emissions measures.
5. Check ISO 50001 and EMAS evidence in appropriate databases and company documents.
6. Check credible independent reports for recent projects or investments.
7. Record the search date, evidence date, URLs and any unresolved conflict.

Suggested German search terms include `Energie`, `Wärme`, `Kälte`, `Dampf`, `Druckluft`, `Photovoltaik`, `Abwärme`, `Wärmepumpe`, `Elektrifizierung`, `Speicher`, `ISO 50001`, `EMAS`, `Klimaziel`, `Dekarbonisierung` and `Investition`.

## Anchors for numeric scoring

Use integer values. Intermediate values are allowed only when the evidence clearly falls between anchors.

### Demand components

- `sector_energy_profile_score` (0/5/10/15): negligible, limited, material, or typically intensive energy-service needs for the coded activity.
- `process_evidence_score` (0/5/10/15): no firm-specific evidence, weak/indirect, one clear relevant process, or multiple strongly relevant processes.
- `site_scale_score` (0/3/6/10): little evidence of manufacturing scale, small site, material production site, or large/multi-line site while still SME-eligible.

### Applicability components

- `low_temp_fit_score` (0/3/7/10): no fit known, possible, clear, or strong multi-use fit.
- `electrification_fit_score` (0/3/7/10): low maturity/unclear, possible, technically established for a main process, or established across several material processes.
- `flexibility_fit_score` (0/3/7/10): no evidence, weak site fit, one clear use case, or several clear onsite/flexibility use cases.

### Gap components

Gap scores may be assigned only after the corresponding source checks are complete.

- `measures_gap_score` (0/4/8/12): several concrete implemented measures, some measures, intentions/pilots only, or no concrete measure found after adequate search.
- `management_gap_score` (0/2/4/6): verified mature system, partial/other system, unverified claim, or no evidence after both website and certification-source checks.
- `targets_gap_score` (0/2/4/6): dated target plus roadmap, dated target only, vague ambition, or no target found after adequate search.
- `investment_gap_score` (0/2/4/6): several recent relevant investments, one, announcement/pilot only, or none found within the lookback period.

## Status fields

- `sme_status`: `confirmed`, `probable`, `uncertain`, `excluded`
- `group_check`: `independent`, `partner_or_linked_sme`, `large_group`, `unknown`
- source checks: `1` checked, `0` not checked
- `latest_evidence_date`: ISO date `YYYY-MM-DD`
- multiple URLs: separated by ` | `

## Conflict rule

When sources disagree, record both. Prefer the more authoritative, direct and recent source, and explain the choice. Do not average conflicting facts.
