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
The current queue has **360 ready, 57 research-needed, 23 review-pending and
12 gate tasks**. Both companies are `RESEARCH_FIRST`; **P43 WZR ceramic
solutions GmbH** is the next coding company. The company queue contains
72 CODE_NOW, 13 RESEARCH_FIRST, 3 REVIEW_PROPOSALS and 12 ELIGIBILITY_FIRST.

## Automated selection and history

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
