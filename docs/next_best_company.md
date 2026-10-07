# Next Best Company to Code — protocol v2.0.0

## Purpose and exact policy

The priority engine chooses an untouched company for AI-assisted first-pass
coding. It reduces manual queue inspection; it never predicts a company score,
probability of buying, deployment absence or number of codable numeric fields.

1. Collapse the dimension queue to one company decision. Eligibility gates,
   research gaps, review and unfinished coding remain separate workflows.
2. Only `CODE_NOW` companies with deterministic QA `PASS` can receive a coding
   rank. QA is automated consistency checking, not independent human review.
3. Sort eligible companies lexicographically by:
   - worst of Evidence and Process Confidence (A, B, C, UNKNOWN);
   - Evidence Confidence, then Process Confidence;
   - expected information gain: HIGH, MEDIUM, LOW, UNKNOWN;
   - number of covered documentary domains, descending;
   - distinct still-unassessed score fields, descending;
   - distinct verified final source URLs, descending, capped at four;
   - natural company ID solely as the final deterministic tie breaker.
4. Assign dense coding ranks and one `is_next_to_code=YES`. All components,
   coverage source IDs, the policy version and a plain-language reason are
   exported. The task queue keeps upstream eligibility gates first.

No weighted aggregate or numeric opportunity score is introduced. Confidence
is inherited from canonical research metadata; the engine does not upgrade it.
A partial mix of ready and review-pending packages is `IN_PROGRESS`, never a
claim that all numeric work is waiting for review. QA blockers use `QA_FIRST`.

## Source coverage and qualitative information gain

Only registered same-company sources with `VERIFIED` or `REDIRECT_VERIFIED`
links contribute. Final URLs are deduplicated, so several register records or
copies of a single page cannot buy a higher rank. Link verification dates stay
visible in the source register and do not establish factual freshness.

- **PROCESS:** a verified registered URL matches a company process mapping with
  a nonempty evidence note and known A/B/C confidence. Generic process-library
  rows, identity pages without such a mapping, and another company's sources
  cannot create this coverage.
- **ENERGY_TRANSITION:** a verified source with an evidence fact has an explicit
  energy, sustainability, environmental-statement, government/public-agency
  case, supplier case, technical report, research-project, investment/project,
  or regional-transformation source type. The exact allowlist is
  `TRANSITION_SOURCE_TYPES` in `src/company_work_priority.py`.
- **MANAGEMENT:** explicit direct ISO/combined-ISO/EMAS, energy/environmental
  certificate or EMAS-document source types, as listed in
  `MANAGEMENT_SOURCE_TYPES`. Coverage alone does not establish current validity.

HIGH means both PROCESS and ENERGY_TRANSITION documents are available;
MEDIUM means PROCESS only; LOW means verified documents exist but lack a
matched process source; UNKNOWN means no usable verified source is available.
Management coverage further differentiates otherwise similar cases.

This is a **documentary decision-value proxy**: assessable evidence can move
uncoded fields toward either a justified proposal or a precise research gap.
It is not statistical entropy reduction, a calibrated expected numeric yield,
independent corroboration or proof that every field in a dimension is covered.
One source can cover several domains without becoming several independent
sources. Historical projects can support route relevance while current plant
configuration remains UNKNOWN. Domain coverage does not override field-level
coding rules, certificate validity or adequate-search requirements for gap
anchors. The four-URL cap is a workflow heuristic, not an empirically validated
threshold. Future validation can compare predicted tiers with observed coding
yield; this version does not claim that validation has happened.

## Frozen batch NBCC-2026-10-06-01

`main` was checked at `b2564383385234915341f478e0f08a2bd57bd0eb`, after the
P23/P11/P53/P20 assessments. The starting work queue contained 380 ready,
39 research-needed, 21 review-pending and 12 eligibility-gate tasks.

Selection was saved **before source enrichment and new coding** in
`data/coding_batch_selections.csv`:

| Rank | Company | Evidence / Process | QA | Gain | Verified URLs | Coverage source IDs |
| --- | --- | --- | --- | --- | ---: | --- |
| 1 | P21 Moritz Fiege | B / B | PASS | HIGH | 3 | S-P21-02 |
| 2 | P27 BCE Special Ceramics | B / B | PASS | HIGH | 2 | S-P27-02, S-P27-03 |

Both have source-linked process and energy evidence, unlike the former
source-count leader P25's narrower documentary coverage. P21 wins the remaining
URL tie breaker. No sector-diversity quota is silently added: the two selected
companies happen to span food/beverage and ceramics.

The reconstruction test removes the new P21/P27 assessments and sources
S-P21-04/S-P27-04, regenerates task inputs, and checks each frozen component
against the v2 ranking. Updated descriptive facts and access dates in older
sources do not affect that selection. The manifest is an automated workflow
decision, not Anna's Human Review.

## Assessment results and evidence boundaries

P21: four numeric proposals (drive relevance, observed measures, partial
management and vague target) and eleven `NEEDS_RESEARCH` fields. The rechecked
2023 agency interview supports compressors and multiple measures; the 2026
agency report supports carbon accounting. Carbon accounting is proposed only
as a partial-system interpretation with confidence C, never as an EnMS or
ISO 50001 claim. The article's general industry heat statements and other
breweries' measures are not assigned to P21. Dates of further investments and
usable storage, electrical topology and process-heat route remain open.

P27: five numeric proposals and ten `NEEDS_RESEARCH` fields. The official
technical-equipment page supports multiple machining drives and CNC control.
The electric-oven route is a historical first-pass proposal at confidence C;
no current deployment claim follows. ISO 9001 is a quality claim and does not
prove ISO 50001. Current thermal service, additional electrification,
flexibility, power quality and recent investments remain unresolved.

All numeric proposals remain `AWAITING_HUMAN_REVIEW`, with blank reviewer/date.
No canonical score input, scored output, company deployment fact or human-review
record is changed by this batch. Uncertainty rows have blank numeric values,
UNKNOWN confidence and exact missing facts. No aggregate company score is
published. After this first batch the queue had 370 ready, 49 research-needed,
21 review-pending and 12 gate tasks. Both selected firms became `RESEARCH_FIRST`;
P30 Zötler became coding rank 1 automatically.

## Frozen batch NBCC-2026-10-06-02

`main` was checked at `6a39490ebf5d0bc35c4ae08eacda66a0e5ba230e` (merged
PR #36). The selector rebuilt validated inputs and froze these companies before
source enrichment or proposals:

| Rank | Company | Evidence / Process | QA | Gain | Verified URLs | Coverage source IDs |
| --- | --- | --- | --- | --- | ---: | --- |
| 1 | P30 Privat-Brauerei Zötler | B / B | PASS | HIGH | 2 | S-P30-02 |
| 2 | P31 Brauerei Clemens Härle | B / B | PASS | HIGH | 2 | S-P31-02 |

Both covered PROCESS and ENERGY_TRANSITION, with 15 unassessed fields. All
substantive components tied, so natural ID resolved their ordering; ID did not
create eligibility or documentary coverage. No sector quota was applied.
The reconstruction test excludes five newly registered sources and both
companies' proposals, then reproduces the frozen manifest exactly.

P30 has seven numeric proposals and eight research gaps. The company describes
a completed 2025 cellar investment and individually controlled tank cooling.
Its energy/EMAS claims support only limited first-pass anchors: the linked
2023 environmental report returned HTTP 404 on recheck, leaving validity open.
Fermentation and maturation durations support a weak scheduling interpretation
at confidence C, not a thermal-buffer or usable load-shifting claim.

P31 also has seven numeric proposals and eight research gaps. The 2024 state
agency case documents a renewable heat baseline, supporting a zero fossil-heat
displacement proposal for that documented baseline rather than from missing
evidence. Wood/biogas heat does not prove process electrification. Company
evidence of PV and dated electric delivery-truck investments supports measures
and investment anchors; vehicle electrification is not process-heat deployment.
KLIMAWIN is a partial management framework, not a verified EnMS. The 2028
electricity self-sufficiency target is not a detailed roadmap.

All fourteen numeric proposals remain `AWAITING_HUMAN_REVIEW`, with blank
reviewer/date. The sixteen gaps retain blank values and UNKNOWN confidence.
No canonical coding, deployment/certificate record or human approval changes.
After batch 02 the queue had **360 ready, 57 research-needed, 23 review-pending and
12 gate tasks**. Both companies became `RESEARCH_FIRST`; **P43 WZR ceramic
solutions GmbH** was the next coding company. The company queue contained
72 CODE_NOW, 13 RESEARCH_FIRST, 3 REVIEW_PROPOSALS and 12 ELIGIBILITY_FIRST.

## Automated selection and history

The subsequent [public-source audit](public_source_audit_2026-10-06.md) rechecked
all 100 companies and updated live link health. Frozen selections retain their
original inputs: reconstruction tests use pinned pre-audit register/process-map
fixtures rather than substituting current link status into historical decisions.
The selector now also runs offline audit-completeness preflight. Audit recovery
does not approve a score or start a coding batch.

`src/select_coding_batch.py` runs deterministic preflight and rebuilds priorities
in memory; it does not rely on a potentially stale output CSV. Only QA-passing
CODE_NOW candidates with dense unique ranks and no open eligibility gate may
be selected. A small remaining queue yields a smaller batch; an empty queue
fails without writing a selection.

Selection is appended atomically to `data/coding_batch_selections.csv`.
An identical snapshot retry preserves bytes; a different snapshot using the
same batch ID fails instead of replacing history. After a batch is assessed,
use a new ID for the next selection. The web export retains frozen selection
components alongside live field counts/workflow, without publishing sums.

## Reproduction

```bash
python src/run_pipeline.py
python src/run_pipeline.py --check-only
python src/select_coding_batch.py --batch-id <new-batch-id> --selected-date YYYY-MM-DD --size 2
python -m unittest discover -s tests -v
node --check web/app.js
node tests/test_web_priority.cjs
```

Outputs and the web snapshot share the same v2 metadata. Behavioral tests cover
source deduplication and ownership, unverified links, QA gating, confidence
ordering, independence from inherited task ranks, incomplete review coverage,
no numeric score mutation and the frozen selection audit.


## Frozen batch NBCC-2026-10-06-03

Starting main: `5fe71bedd651de2d3e0c5843d41f2eb24c1bb482` (PR #38).
Selection was frozen before enrichment: P43 WZR ceramic solutions (B/B,
HIGH, PROCESS and ENERGY_TRANSITION, two verified URLs) and P13 Schmalriede-Zink
(B/B, MEDIUM, PROCESS, three verified URLs), both QA PASS and 15 unassessed fields.

Content inspection exposed a limitation of documentary ranking: P43's old VDI
homepage was retrievable but did not substantiate its company claim. It is now
CONTENT_REVIEW_REQUIRED. A concrete named profile was found and registered,
and the process map now cites the company's own extrusion page. The original
selection is retained as history; it is not rewritten to hide this limitation.
Retrieval metadata plus an old evidence fact is not a content-validation guarantee.
Pinned pre-batch source/process fixtures reproduce this selection.

Each company has six numeric proposals and nine research gaps. P43 documents
its own extruder and control plus limited stage scheduling; own electricity
reduction remains an intention. Customer savings, coating lower bounds and
research equipment are not treated as site heat electrification or storage.
P13 supports limited drives, DC conversion, weak scheduling and possible power
quality, with explicit engineering-inference confidence. A direct current ISO
14001 document supports a conservative partial/other management anchor, not an
EnMS; the expired 2025 target deadline does not prove achievement.

The direct certificate and target evidence correct P13's factual records.
Deployment UNKNOWNs, canonical numeric scoring, previous proposals and all
human-review records remain unchanged. All new numeric proposals remain
AWAITING_HUMAN_REVIEW with blank reviewer/date; no aggregate score is published.

After batch 03 the work queue has **350 READY_TO_CODE, 67 RESEARCH_NEEDED,
23 AWAITING_HUMAN_REVIEW and 12 OPEN_GATE**. There are 70 CODE_NOW,
15 RESEARCH_FIRST, three REVIEW_PROPOSALS and 12 ELIGIBILITY_FIRST companies.
P25 Scheplast GmbH is next automatically; no additional batch is frozen here.


## Frozen batch NBCC-2026-10-07-01

Connected GitHub comparison confirmed main at
`b254e94080ec8b7df668b51075aa4375e6872d7b` (merged PR #39).
The selector froze this batch before new sources, certificate correction or
coding proposals. Source-register/process-map fixtures preserve that state.

| Rank | Company | Evidence / Process | QA | Gain | Verified URLs | Coverage |
| --- | --- | --- | --- | --- | ---: | --- |
| 1 | P25 Scheplast GmbH | B / B | PASS | MEDIUM | 3 | PROCESS (S-P25-03) |
| 2 | P15 ELOXAL BARZ GmbH & Co KG | B / B | PASS | MEDIUM | 2 | PROCESS (S-P15-01) |

Both had 15 unassessed fields. Confidence, QA, documentary gain, coverage and
unassessed-field count tied; verified distinct URLs put P25 first. ID was only
the final tie-breaker among otherwise equal remaining companies. No prediction
of numeric yield and no company score influenced this decision.

| Company | Numeric fields awaiting human review | Blank-valued research gaps |
| --- | ---: | ---: |
| P25 Scheplast | 8 | 7 |
| P15 ELOXAL BARZ | 4 | 11 |

Scheplast's own PV/self-consumption and waste-heat statements support some
concrete energy measures and one onsite integration use case. Robotics supports
limited drive/control interpretations only. The exact-holder ISO 14001 successor
is valid through 2027-02-26; the old certificate remains VERIFIED_EXPIRED.
This is environmental management, not ISO 50001 or verified EnMS maturity.
Old staff/recycling/annual-solar figures cannot be reproduced on the current
homepage and now have CONTENT_REVIEW_REQUIRED plus a scoped recovery entry;
legacy staff data is not freshly confirmed. Conflicting undated counts are not
averaged. Bioenergy concepts do not prove deployed CHP. Closing force in tonnes
does not establish temperature, power or an electric thermal route.

ELOXAL BARZ's own anodising and supplier-authored electrical-oxidation evidence
support conservative conversion/power-quality inferences. The supplier case
is explicitly historical (2016); coolant temperature and pipe material ranges
are not process-heat temperatures, and insulation is not thermal storage.
Current continuity and measured energy effects remain open. A public self-reported
energy-management role supports the unverified-claim anchor only. Its role duties
are neither a verified EnMS nor a deployed technology inventory. The public
profile excerpt was retrieved without accessing login-only content.

Company/process/energy sections, direct certification and exact-name public
energy, certification, CO2 and target searches were inspected on 2026-10-07.
Public gap interpretations do not assert absence of internal targets. The
investment window is 2021-10-07 to 2026-10-07; a 2016 project, undated measures,
certificate dates and crawl dates do not establish investments in that window.
Ten selected-company URLs were rechecked by GET; all returned HTTP 200, including
three new URLs. The complete inventory now has 333 URLs across all 100 sample
companies and retained excluded candidates. Availability is separate from claim
attribution, currency and human source review.

The live queue is **340 READY_TO_CODE, 76 RESEARCH_NEEDED,
24 AWAITING_HUMAN_REVIEW and 12 OPEN_GATE**. Both selected firms move to
RESEARCH_FIRST; the company queue has 68 CODE_NOW, 17 RESEARCH_FIRST,
three REVIEW_PROPOSALS and 12 ELIGIBILITY_FIRST. P26 Barth Galvanik is next.
There are 20 assessed companies, 148 review-pending numeric proposals and
152 explicit research fields. No prior proposal, canonical numeric input,
deployment column, confidence grade or human review record is changed; only
the sourced ISO 14001 fact and public-evidence summaries are corrected.
No proposal total or published SME-ETOI score is produced.


## Frozen batch NBCC-2026-10-07-02

Connected GitHub comparison confirmed main at
`32efc59290f4bac3e2a818926de56d0ff777c41e` (merged PR #40).
The existing v2 selector froze four companies before source enrichment,
certificate correction, process-attribution correction or coding. Fixtures
`source_register_before_nbcc040702.csv` and
`company_process_map_before_nbcc040702.csv` preserve the selection state.

| Rank | Company | Evidence / Process | QA | Gain | Verified distinct URLs | Coverage |
| --- | --- | --- | --- | --- | ---: | --- |
| 1 | P26 Barth Galvanik | B / B | PASS | MEDIUM | 2 | PROCESS |
| 2 | P28 Berg Brauerei | B / B | PASS | MEDIUM | 2 | PROCESS |
| 3 | P29 Meckatzer | B / B | PASS | MEDIUM | 2 | PROCESS |
| 4 | P33 Gindele | B / B | PASS | MEDIUM | 2 | PROCESS |

Each had 15 unassessed fields. All ranking factors tied; ID was only the
final deterministic tie-breaker. P26's retained broken fair link is excluded
from verified URL count. Four cases share the same QA/confidence documentary
readiness, allowing a larger batch without changing the priority rules.
The documentary gain proxy does not predict numeric yield or an opportunity
score; the generic Gindele municipality source was corrected after freezing,
not silently substituted into the historical ranking.

| Company | Numeric proposals pending real human review | Blank-valued research fields |
| --- | ---: | ---: |
| P26 Barth Galvanik | 8 | 7 |
| P28 Berg Brauerei | 10 | 5 |
| P29 Meckatzer | 11 | 4 |
| P33 Gindele | 6 | 9 |

Barth's owned induction hardening and individual quality controls establish
one thermal use case and clear control relevance. Actual furnace fuels,
temperatures, load-shifting windows, new load and investment dates remain
open; 600 HV is hardness, not temperature. Direct ISO 50001 and ISO 14001
certificates establish current exact-holder validity. A misleading old 2024
URL does not supersede the ISO 14001 PDF's actual 2027 validity.

Berg's roughly 90 m3 ice-water buffer is explicitly produced at night for
daytime cooling with peak relief. This supports one cold-buffer use case.
The same article's suspect 90-deg-C ice-water statement is retained as an
unresolved inconsistency: no silent correction to 9 deg C, invented capacity,
process-heat fit or hot-store use. The dated April 2025 warehouse/PV opening
supports one recent site investment. Local heat for associated buildings does
not prove fossil-free brewery steam; the DEHOGA award is for hospitality,
not a manufacturing-site EnMS. Five fields remain research gaps.

Meckatzer's full 48-page report has a 2026 cover/validation, older 2024 prose
and 2025 tables. The visually inspected status colours on printed p22 distinguish
completed 2024 PV/NH3 replacement and 2025 KEG automation from partial/future
fleet steps. Printed p41 is signed by the registered validator on 2026-06-19
for DE-147-00005. Planned nonvalidated July 2027 and consolidated July 2028
updates are due dates, not an asserted expiry. The signed registration number
is used; a shortened later header is not substituted. Natural-gas steam/CHP,
multiple motor applications, central control/166 meters and peak regulation
are directly documented. Legacy vapour-compressor defect/repair is unresolved;
no current operational heat-electrification route or thermal store is invented.
The dated 2030 roadmap supports target coding, not target achievement.

Gindele's own process and automation pages establish computer-controlled
moulding, handling, camera inspection and ultrasonic welding. Closing force,
animated zero counters and a sequence of assembly steps are not power,
temperature, operating hours or load flexibility. ISO 14001 is direct and
current through 2027-07-09; the SKZ issuer table's neighbouring ISO 50001 rows
belong to other companies. The generic municipality URL is retained with
CONTENT_REVIEW_REQUIRED; a named municipal profile corroborates the entity
and process, and the process map now points to the own injection-moulding page.
Environmental policy and historical 2017 automation do not establish concrete
recent energy investments or an absent energy-technology portfolio.

The actual investment window is 2021-10-07 through 2026-10-07. Official company,
process, energy, report, download and certification sections plus exact-name
public energy/target/certification searches were inspected. Full certificate
PDFs and relevant report/table pages were rendered and visually checked.
29 selected-company URLs were rechecked by GET, including 19 new URLs:
28 retrievable and one retained fair-link 404 with its verified replacement.
Complete inventory: 352 URLs across all 100 companies and excluded candidates.
Availability remains separate from attribution, currency and human review.

After this batch, the live queue is **320 READY_TO_CODE, 90 RESEARCH_NEEDED,
30 AWAITING_HUMAN_REVIEW and 12 OPEN_GATE**. All four selected companies move
to RESEARCH_FIRST. Company queue: 64 CODE_NOW, 21 RESEARCH_FIRST,
three REVIEW_PROPOSALS and 12 ELIGIBILITY_FIRST. P35 MACK KUNSTSTOFFTECHNIK
is next. **24/100** companies now have complete 15-field first-pass assessments:
183 numeric fields await review, 177 fields need research. Coverage is distinct
from completion of human review or canonical scoring. No prior proposal,
canonical numeric input, deployment field, confidence grade or human review
record changes; four directly sourced certificate statuses and evidence
summaries are corrected. No aggregate proposal or published score is produced.


## Frozen batch NBCC-2026-10-07-03

Connected GitHub tools confirmed main at `79b84144d50f13e5b7f5b6516c19d92adf093d9a`
(merged PR #41). The user authorises continuous work across company boundaries.
The existing v2 selector froze twelve candidates before enrichment: P35, P36,
P38, P39, P41, P44, P45, P50, P51, P52, P54 and P55. Each tied on B/B
evidence/process confidence, QA PASS, PROCESS-only coverage, MEDIUM documentary
gain, 15 unassessed fields and two verified distinct URLs. ID was only the final
deterministic tie-breaker. Fixtures `source_register_before_nbcc040703.csv` and
`company_process_map_before_nbcc040703.csv` preserve the original selection.
The proxy predicts documentary research gain, never numeric yield or SME-ETOI.
Generic source and process errors found afterwards are not retroactively erased
from the frozen ranking.

| Company | Numeric proposals pending real human review | Blank-valued research fields |
| --- | ---: | ---: |
| P35 MACK Kunststofftechnik | 9 | 6 |
| P36 Kunststofftechnik Borgmann | 8 | 7 |
| P38 Krämer + Eckert | 2 | 13 |
| P39 Eloxal Höfler | 6 | 9 |
| P41 Galvano Weis | 4 | 11 |
| P44 OXIDKERAMIK J. Cardenas | 2 | 13 |
| P45 HARZKRISTALL | 8 | 7 |
| P50 Brauerei Aying | 9 | 6 |
| P51 Distelhäuser | 4 | 11 |
| P52 Glauner / Alpirsbacher | 1 | 14 |
| P54 Waldhaus | 5 | 10 |
| P55 Merschbrock | 9 | 6 |

MACK owns vacuum thermoforming and CNC, not established own injection moulding.
The source-linked PR010 archetype keeps temperature, cooling, schedule, storage
and power-quality assumptions UNKNOWN. The existing opportunity rules match
none of its currently supported signals. Output QA checks that opportunities
belong to the sample and that process mappings resolve; it does not force every
company to acquire a technical opportunity. Source, readiness and scoring work
outputs still cover all 100 firms. Its 2023 PV expansion is dated, whereas
2019 servo conversion is outside the lookback and 2025 general CNC capacity/
efficiency is not a separate confirmed energy project. Square metres are not kWp.

Borgmann's current solar-energy use is not proof of owned PV. Limited conversion
is supported by actual ultrasonic welding; onsite fit is only possible EMS
consumption steering. Regional biogas use is not own CHP. Current ISO 14001:2015
PDF dates govern over the website's erroneous 2025 norm label. Its generic job
portal does not substantiate legacy staff counts; current 110 and historical
130-plus figures remain separated without a canonical staff/eligibility update.

Ehingen's own reachable websites expose a TEST-SYSTEM banner. They remain
CONTENT_REVIEW_REQUIRED. The actual association profile establishes the exact
entity and anodising/powder coating only. Combined group 280 staff, 30000 m2
and heat-treatment capabilities are not assigned to the entity. Höfler's two
automated lines and bath quality control are owned process evidence; wastewater
2022 and capacity 2023 do not by themselves prove energy-transition investment.

Galvano Weis's exact-site current certificate uses an abbreviated holder name
linked on its own legal imprint to the unchanged canonical entity. The generic
directory source is blocked. 2013 pulse-plating research's future-tense heat pump
is not a confirmed current plant; 2023 carbon offsets are not plant heat savings.
OXIDKERAMIK's product operating temperatures and customer PV/wind/hydro
applications do not establish its own kiln temperature, carrier or generation.

Harzkristall directly identifies two owned electric thermal applications: melt
furnace and reheating drum. Programmable cooling and named cold machining are
actual control/drive evidence. 130 kg is glass capacity, not temperature, kW
or validated thermal storage. Furnace recipe control is not dispatch permission.

Ayinger's primary public case establishes an 83 C washer heat-pump application
with 150 kW thermal output. That is not electrical input; the historical 135 C
gas boiler does not establish the current whole-site fossil mix. The Bavarian
11/2018 washer date and report's 05/2019 heat-pump date are distinct stages;
dena's 06/2019 heat-pump date remains differing precise evidence. All are outside
the investment window. The scanned 28-page statement has 2022 data and signed
2023-06-28 validation for DE-155-00168. The exact official active EMAS register
on 2026-09-01 establishes current registration. Its registered-since date 2000
and future May 2025/2027 submissions are not invented validity/expiry dates.
Visual inspection of report pp12, 23, 24 and 27 separates completed, in-planning
and in-implementation measures. Expired 2020-2024 goals, planned 2023-2030
energy storage and planned 2023-2026 logistics do not become completed current
targets/storage/investments merely because it is now 2026. Savings 81%/87%
have different accounts/scopes and are not averaged. Current targets, current
remaining fossil mix, storage and completed recent investments remain research.

Distelhäuser's 2022 ISO 14001 renewal is CLAIM_ONLY without current direct
validity. Actual wort-cooling heat recovery is not itself a store or heat pump;
0 C maturation is not heating fit or a free load-shifting window. Glauner/
Alpirsbacher's recovered raw-material scope does not restore the broken values
page's environmental claims; 1893/1895/1925 assets are not current steam/ice
installations. Waldhaus's 75% denominator is own PV generation self-consumed,
not total site demand. Its 2017 PV falls outside the investment window.

Merschbrock's two PV commissions 2022/2025, charging transformer 2025 and
charging 2026 are several actual recent energy projects. Current 1200 kWp is
PV nameplate, not annual generation. Over 90% own electricity includes PV/CHP,
not all renewable PV or total energy. CHP waste heat used for building heating
and absorption cooling is not a heat pump or thermal store. Actual EDM/PV/
charging are distinct conversion applications; the transformer alone is not
a power-quality issue. ISO 14001 expires 2026-10-15: current on the research
date but close to expiry, with no unstated validity start invented.

Lookback: 2021-10-07 to 2026-10-07. Official company/process/energy/documents,
certifier/EMAS and exact-name public certification/energy/target searches checked.
Relevant PDFs rendered and visually inspected; scanned report OCR never alone
sets validity or status. 65 company URLs rechecked by GET: 64 retrievable, one
retained 404 with prior partial recovery. Complete live inventory 387 URLs
(35 new), 373 retrievable, 357 registered sources; all 100 firms audited.
Five generic/staging sources remain CONTENT_REVIEW_REQUIRED despite success.

36/100 complete fieldwise first passes (540 fields: 250 numeric pending human
review, 290 blank research gaps). This is assessment coverage, not human-reviewed
or canonical scoring. No prior proposals, canonical numeric/deployment/staff/
confidence fields or human review records changed. No aggregate score published.
Six current certification facts and one historical claim corrected. Live work
queue: 260 READY_TO_CODE, 142 RESEARCH_NEEDED, 38 AWAITING_HUMAN_REVIEW and
12 OPEN_GATE. Company queue: 52 CODE_NOW, 33 RESEARCH_FIRST, three
REVIEW_PROPOSALS and twelve ELIGIBILITY_FIRST. All twelve selected companies
move to RESEARCH_FIRST. Next live candidate: P56 Spritzguß Müller GmbH.


## Frozen batch NBCC-2026-10-07-04

Connected GitHub tools verified main at `00bf4390b2018bb8f3026c14f5adf1d530d47d43`
(merged PR #42). Continuous company work is authorised by the user. Before
enrichment, the v2 selector froze P56, P57, P58, P59, P61, P63, P64, P66,
P68, P70, P75 and P76. Each tied on evidence/process B/B, QA PASS, PROCESS-only
coverage, MEDIUM documentary gain, 15 unassessed fields and two verified
distinct URLs. Final ID tie-breaker is deterministic, never predicted numeric
yield or SME-ETOI. Fixtures `source_register_before_nbcc040704.csv` and
`company_process_map_before_nbcc040704.csv` reproduce selection before later
source/mapping corrections. P76's existing exact legal imprint recovery
remains intact, while the old imprint URL's scope blocker remains explicit.

| Company | Numeric proposals pending independent human review | Blank-valued research fields |
| --- | ---: | ---: |
| P56 Spritzguß Müller | 5 | 10 |
| P57 Stocker | 1 | 14 |
| P58 Dorn | 9 | 6 |
| P59 AK Kunststoffspritzguss | 4 | 11 |
| P61 Galvanik-Horstmann | 4 | 11 |
| P63 OTK Kaltenkirchen | 4 | 11 |
| P64 Wieland Metalloberflächentechnik | 5 | 10 |
| P66 KPM Berlin | 3 | 12 |
| P68 TechnoKer | 6 | 9 |
| P70 ceram | 4 | 11 |
| P75 Falter | 2 | 13 |
| P76 Si-Tech Singer | 8 | 7 |

P56 Spritzguß Müller owns CNC/mills/lathes/grinder, EDM/TIG, SPS and automatic
assembly. Machine closing force/shot weight and photographed heated mould
titles do not establish load, process heat carrier or temperatures.
P57 Stocker's actual nine moulding machines differ from external AB-FormTECH
toolmaking, generic CNC explanations and stock photos. Its quality page's
theoretical SPC/regression discussion is not evidence of named installed
control. Accordingly motor/control remain UNKNOWN instead of inherited
maximum values. The process mapping now states external tool manufacture.

P58 Dorn's actual2022 PV supplies self-reported500000-600000kWh/yr and50-60%
of electricity demand, not all energy. Own950kWh electrical battery stores PV
surplus: clear linked integration, not a thermal store or converter rating.
Battery acquisition is undated; only2022 PV safely counts as a recent energy
investment. New1500m2 hall is not a second proven energy technology. Own
CNC/HSC milling, turning/grinding, EDM and laser welding are documented actual
capabilities. Series QA has predefined control/measurement cycles without
energy dispatch. DEKRA certificate171116123/3, ISO14001:2015, exact company/site,
valid2025-11-28 to2028-11-27, issued2025-11-25: PDF body governs, including
uppercase file extension.

P59 AK owns picker/robot-equipped machines and QS/ERP; new tools made by external
shops. Actual cooling/exhaust recovery heats the complete building through
underfloor heating. This supports some measures, not a defined process-fuel
displacement, slab thermal storage/dispatch or a dated recent investment.

P61 Galvanik-Horstmann's own services/measurements replace generic old sector
text. 250C is solderability-test temperature, not core bath heating. A rendered
undated brochure uploaded2020 states KWKK and PV together cover50-55%
electricity: not PV alone or total energy, with2026 continuity/fuel/date
unconfirmed. Current policy supports vague improvement ambition. Historical
portfolio does not automatically close current onsite/deployment fields.

P63 OTK Kaltenkirchen's terse actual production-automaton/bath-line caption
supports limited control. Adviser contact hours7-16 are not factory shifts or
flexible windows. Generic association directory lacks exact company entry in
retrieved content; its source stays CONTENT_REVIEW_REQUIRED with own
entity/process recovery only. Other OTK entities' certificates/energy assets
are excluded. P64 Wieland Schwetzingen owns rack/drum/manual galvanic plants
and checks bath parameters; customer PV/wind applications are not owned
renewables and unrelated Wieland Group targets are not inherited.

P66 KPM's actual980C biscuit/1420C high firing support difficult high-temperature
fit. Project provider2023 describes own kiln waste-heat export, public VDI case
anchors2017;110C recovery outlet and1000kW THERMAL do not become kiln heat
carrier or electric input.2017 outside recent lookback. Adjacent Siemens
heat-pump pilot/provider decarbonisation goals are another actor/site, not KPM.
Current remaining fuel, heat-electrification route, storage, dispatch and recent
completed energy investments remain researched gaps.

P68 TechnoKer owns2022 PV205kWp and describes regional biogas in thermal
afterburning. Visually inspected supplier proof537 records4436litres BIO-LPG/
biogenic propane delivered2023-12-04, confirmed2024-01-25 to exact site. This
is a different fuel product/scope from biogas, not ISO evidence or whole-plant
fossil-free proof. Customer electric-heater ceramics are not own electric kilns.
2018 recovery outside window;2021 kiln year lacks month and might precede
2021-10-07. Only2022 PV safely counts as dated recent physical energy CAPEX;
gas-supply switch/delivery not automatically additional capital project.
Planned digitalisation by end2023 is not verified complete just because now2026.

P70 ceram owns grinding/milling/air classification and XRF/laser measurement,
melting/sintering without stated thermal carrier/temperature. Customer material
ratings are excluded. Current ISO14001 claim has no current direct body. Old
PDF returned404: filename/cached snippet cannot authenticate holder/dates or
prove expiry. Corrected CLAIM_ONLY with blank direct URL/current validity,
never VALID/VERIFIED_EXPIRED or inferred discontinued certification. Scope-
limited recovery preserves own claim and the missing current certificate.

P75 Falter actually pumps beer into lager tanks, heats mash at unspecified
temperatures and makes vague resource-saving bottling claims. Product
maturation4-6weeks/3-4months is not thermal-buffer/dispatch permission.2018
cellar and2024 capacity extension do not establish recent energy CAPEX. Alcohol
responsibility is not an energy target. P76 Si-Tech owns PV and robots/automatic
handling/packaging plus production planning; specialised tool manufacture is
outsourced, no owned CNC/EDM inherited. Three shifts not flexible window. SKZ
certificate001048.U current2025-11-29 to2028-11-28 issued2025-11-29; rendered
annex explicitly includes Siemens15 assembly alongside Siemens26-28. EcoVadis
and integrated-system claims are not mature certified EnMS. PV commissioning
undated;2018/2020 projects outside window.

Lookback2021-10-07 to2026-10-07. Own primary production/energy/documents and
exact-name public certificate/energy/target checks completed; relevant PDF
bodies and annex rendered/visually inspected. Certificate and report periods,
claim attribution and current continuity remain separate from HTTP200.
67 URLs GET-rechecked:66 retrievable, one ceram404 with explicit partial claim
recovery. Live inventory424 URLs,409 retrievable,394 registered sources, all
100 sample companies audited. Two generic reachable sources are explicitly
blocked; all prior content blockers remain in place.

48/100 complete15-field first passes:720 rows,305 numeric proposals pending
independent human review and415 blank UNKNOWN research fields. Assessment
coverage not reviewed/canonical score coverage; no final score published.
All prior proposals, canonical numeric/deployment/staff/confidence fields and
human-review records unchanged. Two verified ISO14001 facts and one
unverified claim corrected independently from scoring. Live queue200 ready/
197 research/43 review/12 gate; company queue40 CODE_NOW/45 RESEARCH_FIRST/
3 REVIEW_PROPOSALS/12 ELIGIBILITY_FIRST. All12 selected firms RESEARCH_FIRST.
Next live candidate P77 metak GmbH & Co. KG.


## Frozen batch NBCC-2026-10-07-05

Batch `NBCC-2026-10-07-05` completes 15-field first passes for P77, P79,
P80, P81, P83, P84, P87, P90, P91, P92, P93 and P94: 70 numeric proposals
await independent human review; 110 fields remain blank `NEEDS_RESEARCH`
with `UNKNOWN` confidence and an exact missing fact. Current coverage is
**60/100 companies and 900/1,500 fields**: 375 numeric proposals pending
review and 525 research gaps. This is assessment coverage, not resolved or
human-reviewed coverage. No new canonical score or automatic approval.

Six certificate facts are corrected using actual document holders, validity
and issuer: Metak ISO 50001/14001, Langer ISO 50001/14001, MKT ISO 14001 and
Riegele EMAS. Riegele's signed 2025 statement and current official register
are distinct from reporting years, registration-since dates and expiry.

German Ceramany manufacturing attribution is unresolved; foreign ISO 9001
holders and cross-site staff cannot establish German owned assets. All its
15 fields remain researched gaps. InnoKeramik operates plate finishing;
KITO's firing and machinery sold to partners are not owned kiln equipment.
Both mappings use explicit provisional archetypes without supported
opportunity-rule matches; source, readiness and coding coverage remain.

Planned Langer PV/storage cannot be considered commissioned because September
2026 has passed. Actual 2024 efficient-machine, extraction-converter and
cooling work is dated separately. MKT's purchased hydro is not owned generation
or renewable process heat. ELB's coating resistance is not bath temperature.
A GRW capacity grant is not completed energy CAPEX. Riegele's inconsistent
boiler unit is retained, not silently changed from MWh to MW. Future controls,
CIP and logistics PV remain planned until completion is established.
Ketterer's explicit owner statement of exclusively woodchip operating heat
supports a bounded thermal-fuel anchor, not whole-company fossil-free status;
2021/2023 nitrogen dates conflict and are not averaged. Schimpfle's completed
PV and transformer projects retain separate dates. Kuchlbauer's room heat
pump and electrical battery are not brewery process heat or thermal storage;
its 2024 integrated logistics project counts once for investment coding.

Current work queue: 140 `READY_TO_CODE`, 248 `RESEARCH_NEEDED`,
52 `AWAITING_HUMAN_REVIEW`, 12 `OPEN_GATE`. Company actions: 28 `CODE_NOW`,
57 `RESEARCH_FIRST`, three `REVIEW_PROPOSALS`, 12 `ELIGIBILITY_FIRST`.
Next ranked company: **P95 Winkler-Bräu**. Outputs contain 200 opportunities
and 195 research tasks. The source inventory has 430 registered sources,
460 audited URLs and 445 retrievable URLs, covering all 100 sample firms.
The 65-URL batch follow-up confirms 63 retrievable URLs and two retained
404s; replacement/scope notes remain separate from successful retrieval.
Prior proposals, canonical numeric/deployment/staff/confidence fields and
independent human-review records remain unchanged.


The selection was frozen from main at `8acdeb2ee6408f23ece54aea583e53a217c2a853`
before enrichment. Each selected company had B/B confidence, QA PASS, MEDIUM
documentary gain, PROCESS coverage, 15 unassessed fields and two verified
distinct URLs. The company ID broke the final tie. Historical source/process
fixtures reproduce the exact manifest, independently of later scope corrections.

| Company | Numeric proposals pending review | Blank research fields |
| --- | ---: | ---: |
| P77 metak | 8 | 7 |
| P79 Langer | 9 | 6 |
| P80 MKT | 7 | 8 |
| P81 Eloxalwerk Ludwigsburg | 5 | 10 |
| P83 Gerbracht & Mönch | 5 | 10 |
| P84 Sauer Oberflächentechnik | 1 | 14 |
| P87 Ceramany | 0 | 15 |
| P90 InnoKeramik | 2 | 13 |
| P91 Riegele | 10 | 5 |
| P92 Ketterer | 8 | 7 |
| P93 Schimpfle | 8 | 7 |
| P94 Kuchlbauer | 7 | 8 |

All twelve companies now require field-specific research; a first pass with
zero numeric proposals remains an honest assessment. This preserves the
separation between missing evidence, technical relevance and commercial
white space. All retained unreachable sources and content blockers remain
visible; successful retrieval never proves the claim or human approval.


## Complete first pass: 100/100 — 2026-10-07

The final eligible selection `NBCC-2026-10-07-07` contains the remaining16
CODE_NOW companies in deterministic v2 rank order. Pre-enrichment sources and
process mapping are frozen in the completion100 fixtures. The selector's QA and
eligibility requirements remain intact.

To satisfy the entire100-company documentary sample, `GATE-ASSESS-2026-10-07`
separately freezes the12 upstream group-gated firms. Documentary coverage does
not resolve their validity gates or approve canonical scoring. They have15
field assessments each and retain ELIGIBILITY_FIRST / OPEN_GATE.

All100 companies now have all15 fields assessed. The exporter counts unique
expected company-field keys and excludes duplicate or unknown fields from
coverage; it reports554 pending numeric proposals and946 UNKNOWN research gaps.
None has actual human approval. The live queue has no CODE_NOW candidate;
selection fails closed rather than recycling a previously assessed company.
The web view shows complete coverage, current research/review states and the
separate gated cohort without aggregate proposal scores.

Owner equipment evidence distinguishes actual manufacture, equipment maximum,
product capability, other group sites and building heat. Frömgen's recovered
machine park confirms own sintering; maximum1700C and inert-gas atmosphere are
not actual operating temperature or heating fuel. Hermsdorf/Hofmann/Kessel/Holder
current ISO50001 bodies are holder/date checked. OT's linked environmental
certificate is expired, and Swiss Ceramaret environmental certification is not
inherited by German Meissen. No absent public evidence becomes non-deployment.

See the latest README section for current queue totals and all company dossiers
for source IDs, exact field decisions and missing-fact questions.
