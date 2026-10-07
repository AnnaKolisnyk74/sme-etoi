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
