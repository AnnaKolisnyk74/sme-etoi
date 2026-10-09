# Decision research — 8 October 2026

This block examines 12 unresolved SME/group cases, two legal-entity conflicts and
ten technical companies. It records public-source findings, not personal approval
or final canonical scores. The actual checker is Codex; the dashboard label is
**Geprüft**. Missing evidence remains unknown.

## Results and scope

- The frozen baseline had 597 checked proposals and 903 unknown fields. Of the
  50 unknown score fields in the ten selected firms, two have new direct evidence
  and 48 remain unknown. The live total is **599 checked / 901 unknown / zero
  approved**. Previously checked proposals are unchanged.
- Lamberts' own electrician vacancy supports motor/drives = 5 and automation/
  control = 3 with confidence B. Electric drives and controls do not establish
  an electrically heated glass-melting furnace.
- Five research-ledger findings have public YES evidence: heat recovery at
  Kläger, Scheplast, Meckatzer and metak, plus metak's current ISO 50001 energy
  management certificate. Three correspond to currently generated queue tasks;
  those show **EVIDENCE_FOUND**, rather than a canonical value being silently
  overwritten. The other two remain visible in the ledger and company profiles.
- All 12 SME eligibility gates remain unresolved. Two group-scale exclusion
  signals require a final group/AWU/period decision. Neither source checking nor
  an individual entity's small size is a group eligibility approval.

## Reproducible selection and evidence

The first ten distinct firms by frozen Research Queue rank were selected after
excluding SME gates and the two identity conflicts: P04, P05, P100, P12, P18, P25,
P29, P76, P77 and P78. The selection is preserved in
[the selection ledger](../data/decision_research_selections_20261008.csv) and
[the pre-research queue](../data/history/research_queue_before_deep_20261008.csv).

[The 24 profiles](decision_research_profiles_20261008.json) give attributable
source IDs, periods, findings and next missing facts. The
[50 field attempts](field_research_deep_20261008.csv) cover each selected unknown
field once. [The 29 selected source checks](decision_source_checks_20261008.csv)
record primary-body hashes, document locations and bounded scope. The
[151 distinct URL retrieval records](research_source_attempts_deep_20261008.csv)
include 26 access failures; search discovery and unselected readable pages do not
substitute for reviewed evidence. Queries are preserved separately in
[the discovery ledger](research_queries_deep_20261008.csv).

## SME and identity decisions still needed

| Company | Finding | Remaining decision |
| --- | --- | --- |
| P07 Varioplast | Own Hong Kong subsidiary documented | Full ownership chain and aggregated group thresholds |
| P10 Oskar Lehmann | KG and liable partner identified; old staffing figure | Current ownership, group staffing and finances |
| P32 Kronenbrauerei | Brewing process verified | Current finances and ownership |
| P34 KTS | Losse Holding portfolio link; standalone staffing context | Stake, linked entities and group thresholds |
| P40 Oftech | Source access and financial gap remain | Obtain a attributable current ownership/financial source |
| P42 OT | Liable participation company identified | Ownership and group aggregation |
| P46 Hermsdorf | Current group confirmation access-limited | Verify current CERAM chain and group figures |
| P47 Hofmann | IFGL report establishes full control and group-scale staffing | AWU, relevant periods and final eligibility decision |
| P65 Fürstenberg | State ownership chain and entity finances documented | Exact public-control exception and aggregation analysis |
| P67 DOCERAM | MOESCHTER's three-unit structure documented | Current group staffing and financial thresholds |
| P88 Ceramaret Meissen | Own group page reports more than 300 employees | Current ultimate chain, AWU, periods and group finances |
| P104 Holder | Correct metal-coating legal entity identified | Full ownership and current financial thresholds |
| P109 Nymphenburg | Imprint includes “Königliche” and München HRA 48197 | Match stored record to register identity before canonical rename |
| P110 Triptis / Eschenbach | Current brand imprint names Eschenbach; old shop terms conflict | Verify operator/succession rather than transfer claims across entities |

Each row's source and exact boundary are in its profile and company dossier.
P47's 1,180 permanent group employees and P88's undated “more than 300” are
exclusion signals, not calculated EU annual work units. Fürstenberg's individual
entity figures cannot resolve its public group control by themselves.

## Technical follow-up

The company profiles distinguish commissioned measures from planned measures,
historical events and reports covering multiple periods. The 48 remaining fields
need specific facts such as the heat carrier and process temperature, machine or
storage capacity, operating hours, dispatchability, commissioning date, or dated
management/investment evidence. Heat recovery alone does not establish controllable
thermal storage. An electrical vacancy does not identify the production shift
pattern. Access failures do not establish non-deployment or commercial white space.

## Validation

Pipeline preflight verifies selection, exact frozen gap coverage, attributable
reviewed source bodies and absence of personal approval. Regression tests verify
the preserved checked baseline, source ownership, SME gates, identity conflicts,
deployment ledger and dashboard rendering. The canonical master, coded pilot,
process map and QA approvals are unchanged.
