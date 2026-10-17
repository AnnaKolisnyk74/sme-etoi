# Source-led field follow-up — 17 October 2026

Ten existing profiles were revisited after screening new primary and first-hand
sources: P74, P96, P107, P28, P54, P57, P72, P84, P85 and P04. The selection
prioritises attributable evidence capable of resolving particular gaps; it is
not represented as the next ten companies in the queue or as a random sample.
All **85 frozen open fields** for these firms were re-examined in the stated
source scope. **Ten additional proposals are CHECKED; 75 remain UNKNOWN.**

Current coverage is **664 / 1,500 checked proposals (44.3%), 836 unknown, zero
personal/final approvals**. All 654 previously checked rows remain unchanged.
The unchanged canonical company/process/deployment/certificate/score datasets
must not inherit these research proposals automatically. All twelve SME gates
remain open.

## Newly supported proposals

| Company | Field | Anchor / confidence | What the evidence supports |
| --- | --- | --- | --- |
| P74 Maisel | automation_control_score | 3 / B | Completed filling-hall ventilation with three-zone demand control and Siemens Simatic S7. Scope is this installation, not whole-company dispatch. |
| P96 PEKA | measures_gap_score | 3 / B | Named user testimony plus a first-hand site visit document an operating temperature-control/pump efficiency measure. |
| P107 Dibbern | fossil_heat_displacement_score | 4 / B | Management identifies gas-fired Hohenberg ceramic kilns. Material fossil thermal duty supports conditional substitution relevance, without establishing an electric route or measured present duty. |
| P107 Dibbern | investment_gap_score | 2 / B | Interview published 21 September 2026 confirms the kiln replacement already completed in 2026, inside the fixed 2021-10-07..2026-10-07 window. |
| P72 Hofbräuhaus Traunstein | management_gap_score | 2 / C | FfE explicitly names the brewery as an energy-audit reference. Date, exact report and current system maturity are not supplied. |
| P28 Berg; P54 Waldhaus; P57 Stocker; P84 Sauer; P85 Schweizer | management_gap_score | 5 / C each | Defined public-documentation checks find no verified formal energy/environmental system in the inspected scope. **Internal system reality remains UNKNOWN.** |

The last five values are public-documentation gap proposals, not positive
findings that systems or technologies are physically absent. Each has its own
[scope record](management_gap_checks_20261017e.csv), own-site bodies, recorded
ISO 50001 / ISO 14001 checks, executed name search, and an attributed copy of the
EMAS organisation-list check dated 1 October 2026. An absent exact-holder entry
there says nothing about ISO certification. Restaurant DEHOGA awards, ISO 9001,
funding consultation, efficiency claims and energy equipment do not authenticate
a formal brewery/site EnMS. No certificate-register status was overwritten.

## Source and interpretation boundaries

- The live airinotec homepage links its new `/projekte/brauerei-maisel` route.
  The old `/referenzen/` route now returns 404. The full current supplier body
  confirms successful completion; its reference to a 2023 article does not
  establish a commissioning day or prove completion after October 2021. No
  additional investment proposal is closed from this date alone. Steam does
  not identify fuel. A separate Bayreuther Brauhaus project is not inherited.
- The PEKA supplier catalogue and K-PROFI on-site interview (October 2022,
  printed pages 40–47) distinguish active tempering control from planned
  machine-level, cooling-network and compressed-air work. Page 45 was visually
  read: three 500 W constant-pump units were replaced by one 860 W unit.
  Catalogue ratings are not actual PEKA temperatures, grid demand or storage.
  The interview dates publication/site observation, not exact commissioning;
  the recent-investment field stays unknown.
- Jan and Ben Dibbern directly describe the already replaced Hohenberg kiln in
  their 21 September 2026 interview. The reported 30–35% reduction is per firing,
  not independently measured whole-site savings. EUR 1.1 million includes kiln
  **and logistics**, so it is not an energy-CAPEX amount. The 2027 decoration
  transfer remains planned. The state business profile independently identifies
  the sampled Hohenberg manufacturer; no other Dibbern production site is added.
- The freshly read Lammsbräu 2024 report states that the 105°C network, storage
  and heat pumps are planned as of April 2025, with expected August 2026 start.
  An elapsed expected date does not prove commissioning. Rainwater storage and
  carbon sequestration are not usable thermal storage; its final gap stays open.
- Waldhaus's advisor case dated 7 July 2026 describes completed filling-line
  modernisation and funding support since March 2023. The already checked
  investment row is preserved; the funding project does not verify an EnMS.
- Other discovery leads were rejected or unused, including another ceramics
  company's electric-kiln case, historical Barz pipe insulation, old Sembach gas
  data and inaccessible Dibbern/social/manufacturer pages. Failures and scoped
  alternatives are retained; search snippets never close fields.

## Audit trail and validation

- [Ten hash-linked profiles](decision_research_followups_20261017e.json) and
  [frozen predecessors](../data/history/decision_profiles_before_followup_20261017e.json).
- [85 exact-once field attempts](field_research_followup_20261017e.csv),
  [frozen 1,500-row baseline](../data/history/score_coding_proposals_before_followup_20261017e.csv)
  and [28 selected body checks](decision_source_checks_20261017e.csv).
- [54 direct retrieval attempts](research_source_attempts_followup_20261017e.csv)
  retain actual timestamps, response hashes and seven failures. Third-party raw
  bodies stay outside the repository. Two previously unavailable original
  Dibbern bodies are retained as dated failures in the proposal evidence trail;
  the new anchors cite accessible first-hand content instead.
- Thirteen new sources bring the assessed register to **655: 592 scoped
  RECHECKED, 53 CONTEXT_ONLY, 10 UNAVAILABLE, zero unclassified**. The separate
  retrieval inventory covers **939 URLs / 861 retrievable**, with 101 recovery
  investigations. A historical content check and a fresh GET have separate dates.
- Ten new check decisions give 669 proposal-check rows: 503 original confirmed,
  46 corrected, five withdrawn and 115 formerly unknown fields now supported.
  The body ledger contains 347 records, 340 retrievable. Four separate P11
  reassessments remain in history: 673 web check-history rows altogether.
- There remain 100 unique profiles, with 21 follow-up records across three
  follow-up blocks. Historical field work is **863 attempts / 67 closures /
  796 unknown at attempt date**; these are not the current 836 unknown fields.
  Public research-results history stays 105 observations / 16 YES; no new
  canonical deployment flag or human review is inferred from a field closure.

Validation covers 274 Python tests and the full Python suite, pipeline write/check-only, JavaScript
syntax, register rendering/navigation, unchanged checked baselines and private
publication of the exact green-CI merged assets. Browser visual QA is unavailable.
