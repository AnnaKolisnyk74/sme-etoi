# SME-ETOI Score Coding Proposal Protocol

## Purpose

`data/score_coding_proposals.csv` is a review layer between the scoring work
queue and the canonical numeric scoring input.

It exists so that a first coder or an AI-assisted research pass can propose
numeric anchors with evidence while preserving a strict human review gate.

A proposal is **not** a canonical score value.

## Required fields

Every proposal records:

- company and legal entity;
- SME-ETOI dimension;
- exact score field;
- proposed numeric anchor;
- maximum value;
- plain-language anchor interpretation;
- proposal confidence;
- evidence source IDs;
- evidence basis;
- missing fact when additional research is required;
- proposal status;
- coder;
- proposal date;
- reviewer and review date when applicable.

## Allowed lifecycle

```text
Scoring Work Queue
    -> coding assessment
        -> NEEDS_RESEARCH
        -> new evidence -> new coding assessment
        or
        -> AWAITING_HUMAN_REVIEW
        -> APPROVED or REJECTED
        -> separate canonical update
    -> rerun Score Readiness
    -> rerun scoring pipeline
```

An approved proposal still does not mutate canonical scoring data by itself.
The accepted values must be copied into the canonical scoring input in a
separate, reviewable change.

## Human-review rule

`AWAITING_HUMAN_REVIEW` proposals must have blank `reviewer` and
`review_date` fields.

`APPROVED` and `REJECTED` require:

- a real reviewer;
- a review date;
- preferably a short review note.

The automated validator may reject malformed proposals, but it must never mark
a proposal as human-reviewed.

## Evidence rule

Every numeric proposal must cite one or more source IDs from
`evidence/source_register.csv` that belong to the same company.

The proposal should explain why the selected coding-manual anchor fits the
stored evidence.

A source that merely identifies the company is not sufficient evidence for a
technical score field.

## Uncertainty rule

If evidence does not support an anchor, do not manufacture one from generic
sector assumptions.

Use `NEEDS_RESEARCH` when the current repository evidence is insufficient for
a field-level numeric anchor. Such a row must:

- leave `proposed_value` blank;
- use `proposal_confidence=UNKNOWN`;
- identify the exact `missing_fact`;
- cite the existing source IDs that establish the current evidence boundary.

This is intentionally different from a numeric zero. Zero is an allowed coding
anchor only when the stored evidence actually supports the zero anchor.

Where a conservative numeric anchor is proposed from weak but relevant
evidence, the proposal confidence should reflect that limitation and the
evidence basis must state it explicitly.

## P04 first-pass example

The first populated proposal set is P04 — Neumarkter Lammsbräu Gebr.
Ehrnsperger KG.

It contains all 15 SME-ETOI score fields and remains entirely
`AWAITING_HUMAN_REVIEW`.

If all proposed anchors were accepted unchanged, they would sum to 53/100.
This number is a proposal-derived arithmetic result, not a published SME-ETOI
score.

P04 must remain absent from canonical scored output until human review and a
separate canonical update are complete.

## P19 uncertainty example

P19 — Glasfabrik Lamberts GmbH & Co. KG demonstrates the field-level
uncertainty path.

The current repository evidence supports only three numeric first-pass
proposals:

- `measures_gap_score = 7`;
- `management_gap_score = 0`;
- `targets_gap_score = 5`.

The other twelve score fields remain `NEEDS_RESEARCH`. Examples include the
current furnace energy carrier, firm-specific electrification route, operating
pattern, power-quality evidence and onsite-integration evidence.

No total P19 score is calculated from these three fields. The twelve unresolved
fields stay explicitly unresolved.

## P12 mixed-state example

P12 — Richard Henkel GmbH demonstrates that one company can have different
proposal states across dimensions.

Four dimensions are fully covered by numeric proposals and therefore wait for
human review. Load-flexibility remains `RESEARCH_NEEDED` because the current
sources do not establish a thermal buffer, thermal store or sufficiently
documented usable thermal inertia.

Fourteen numeric proposals sum arithmetically to 50. This partial sum is not a
published SME-ETOI score because one required field remains unresolved.

## P16 high-confidence / incomplete-field example

P16 — Sembach GmbH & Co. KG has A-level company/process evidence and direct
current ISO 50001 / ISO 14001 certificates. That does not make all score fields
known.

The repository directly supports four numeric proposals:

- difficult/uncertain temperature fit from documented 1,100–1,750 °C processes;
- scheduling relevance from chamber-furnace / discrete thermal stages;
- mature management-system evidence;
- no dated public target after the defined checks.

Eleven remaining fields stay `NEEDS_RESEARCH`, including the furnace energy
carrier, firm-specific electrification route, motor/converter evidence,
thermal-buffer evidence, power-quality evidence and recent transition
investments.

This case prevents overall evidence confidence from being used as a shortcut
for score-field evidence.

## P05 fully covered proposal example

P05 — Einbecker Brauhaus AG has all 15 score fields covered by numeric
first-pass proposals.

The strongest direct evidence includes brewing and thermal-process operations,
refrigeration, PV, biogas CHP with absorption chilling, heat recovery, process
control renewal, dated climate targets and planned electric clean-steam
generation.

The proposed anchors sum arithmetically to 59/100. This value remains a
review artifact only. All five dimension packages stay
`AWAITING_HUMAN_REVIEW` until a real reviewer approves or rejects the field
proposals and a separate canonical update is performed.

## P18 known-fossil / partial-evidence example

P18 — Glashütte Lamberts Waldsassen GmbH documents natural-gas firing in glass
production and a current ISO 50001 system.

Seven score fields receive numeric first-pass proposals, including fossil-heat
displacement relevance, weak scheduling flexibility, ordinal incremental-load
relevance and transition-gap fields. Eight fields remain
`NEEDS_RESEARCH`.

The unresolved fields include the firm-specific electric-melting route,
motor/converter/control evidence, thermal storage, power quality, onsite
integration and recent transition investment evidence.

The seven numeric proposals sum to 22, but no aggregate score is calculated
while eight required fields remain unresolved.


## P22 full-coverage electrified-heat example

P22 — RIEDENBURGER BRAUHAUS Michael Krieger GmbH & Co. KG has all 15 score
fields covered by first-pass numeric proposals. Direct company evidence
documents heat pumps, vacuum vapour compression, own PV, waste-heat recovery,
three thermal stores and explicit peak reduction/time-shifted operation.

The proposed anchors sum to 74/100. This remains a review artifact only.

## P24 generic-process guardrail example

P24 — H&K Müller GmbH & Co. KG verifies a current ISO 50001 system and a
single-site injection-moulding operation. The generic PR001 process-library row
is still `TO_RESEARCH`, so it is not used as a substitute for company-level
technical evidence.

Only management-gap and target-gap fields receive numeric proposals. Thirteen
technical/investment fields remain `NEEDS_RESEARCH`.


## P23 automatic reprioritisation example

P23 — FM-Plast GmbH receives seven numeric first-pass proposals and eight
`NEEDS_RESEARCH` fields.

The unresolved facts include remaining fossil process heat, converter/control
topology, operating schedule, thermal buffering, additional electrification,
onsite integration and recent investment timing.

Because each of the five dimensions contains at least one unresolved field,
all five dimension packages are classified as `RESEARCH_NEEDED`. The company-level priority engine therefore removes P23 from `CODE_NOW` and
promotes P11 — B+T Oberflächentechnik GmbH — for the next coding pass.

## P11 next-best reprioritisation example

P11 — B+T Oberflächentechnik GmbH is the first company processed after the
company-level priority engine promoted it to coding rank 1.

The current repository evidence supports five numeric first-pass proposals:

- limited automation/control relevance from documented digital process-data work;
- an intentions/pilot transition-measures anchor;
- a verified mature ISO 50001 / ISO 14001 management-system anchor;
- a vague sustainability-target anchor;
- a pilot/research investment anchor.

Ten technical fields remain `NEEDS_RESEARCH`, including process
temperatures, fossil-heat carrier, rectifier/converter evidence, operating
schedule, thermal buffering, power-quality evidence and onsite integration.

The five numeric proposals sum to 14, but no total score is calculated.

Because four of the five dimension packages now contain research gaps, P11
moves from `CODE_NOW` to `RESEARCH_FIRST`. The dynamic priority engine
automatically promotes P53 — Brauerei Rittmayer Hallerndorf GmbH & Co. KG —
to coding rank 1.

## P53 biomass-heat / storage example

P53 — Brauerei Rittmayer Hallerndorf GmbH & Co. KG documents biomass heat,
process-heat recovery, a heat store and photovoltaic generation.

Eight fields receive numeric first-pass proposals, including clear thermal
buffering, onsite integration and several observed transition measures.
Seven fields remain `NEEDS_RESEARCH`, including the firm-specific
electrification route, remaining fossil heat, motor/control evidence,
incremental load and investment timing.

The numeric proposals sum to 25, but no aggregate score is calculated while
required fields remain unresolved. P53 therefore moves from `CODE_NOW` to
`RESEARCH_FIRST`, and P20 DERIX Glasstudios becomes the next company to code.

## P21/P27 documentary-priority batch

The v2 priority mechanism selected P21 and P27 before their assessments were
written. P21 has four numeric proposals and eleven research gaps; P27 has five
numeric proposals and ten research gaps. Both move to `RESEARCH_FIRST`.

The carbon-accounting interpretation for P21 and historical electric-oven route
for P27 are explicitly provisional at confidence C. They do not establish an
EnMS or current furnace deployment. All numeric proposals await real human
review; no canonical values or score totals are published. See
[`next_best_company.md`](next_best_company.md) and the frozen
`data/coding_batch_selections.csv` for selection provenance.

## P30/P31 reusable-selector batch

The selector froze batch NBCC-2026-10-06-02 from rebuilt QA-passing v2 priorities
before new source checks. Both companies have seven numeric proposals awaiting
human review and eight explicit research gaps; neither has a complete score.

P30's individually controlled cellar cooling and dated investment do not prove
process electrification or thermal-storage flexibility. Its EMAS statement
has unresolved validity; the linked report returned 404. P31's agency-documented
renewable heat baseline supports a zero fossil-displacement anchor for that
baseline, not a universal no-fossil deployment claim. Its electric trucks qualify
as recent energy-transition investment evidence, not electric process heat.
Scheduling interpretations remain weak at confidence C for both companies.

The selector appends selection provenance without changing evidence, scores
or review states. Both assessments move to `RESEARCH_FIRST`; P43 becomes the
next company to code. The web batch card reports live field counts and retains
the original selection rank. All canonical coding and human-review gates remain.


## P43 / P13: scope inspection after retrieval

The third ranked batch adds six numeric proposals and nine blank-valued research
gaps per company. Own-site scope is required: customer product savings are not
site measures; a generic whitepaper is not installed AI/IoT or converter control;
a product's temperature resistance or a curing lower bound is not a complete
process temperature range. An offered service does not establish onsite furnace
ownership. Research equipment and wastewater chemical savings are not automatically
energy-transition investments.

P13's direct current ISO 14001 certificate is factual research evidence, not a
human approval. The proposal uses the partial/other-system anchor because EnMS
maturity is unresolved. A climate-neutrality target dated 2025 supports only the
published dated ambition; its achieved status remains UNKNOWN. P43's ISO 9001
quality claim does not substitute for energy/environmental management evidence.


## P25 / P15: validity, historical continuity and public role claims

The frozen 2026-10-07 batch adds eight numeric proposals and seven research
fields for Scheplast, and four numeric proposals plus eleven research fields
for ELOXAL BARZ. All numeric proposals await human review; no score total is
published. Unknown deployment facts stay UNKNOWN.

A direct current ISO 14001 successor can correct a factual certificate status
without becoming a mature EnMS or approving a numeric score. An undated company
statement of PV and waste-heat utilisation supports some concrete measures but
does not date recent investments. An own-site robotics claim supports only
limited drive/control relevance until ratings and architecture are established.
Old numeric source extracts that are no longer reproducible remain visible
with CONTENT_REVIEW_REQUIRED rather than being silently treated as current.

A named supplier case from 2016 establishes historical context only. Coolant
temperature, generic pipe temperature limits, insulation and old flow sensing
cannot substitute for actual current process heat, storage or control evidence.
A public self-reported energy role uses the unverified-claim management anchor,
not verified certification. No login-only profile data is used. This batch's
five-year investment lookback is 2021-10-07 through 2026-10-07; publication/crawl
dates, certificate renewals and role duties are not commissioning dates.


## P26 / P28 / P29 / P33: attribution and temporal precision

The 2026-10-07 second batch assesses every field for four ranked companies:
35 numeric proposals await human review, 25 fields remain NEEDS_RESEARCH.
This raises full fieldwise first-pass coverage to 24/100, not human-reviewed
coverage or published scores. Review metadata and deployment UNKNOWNs stay
unchanged. Four directly sourced current certificate facts are corrected.

Certificate body, holder and dates govern validity, not a legacy download URL.
A current signed EMAS statement can establish validation without inventing an
expiry from planned future updates. Mixed-period reports must distinguish old
prose, current tables, validated dates and completed/partial/planned status;
status-colour tables need visual inspection. A defective legacy installation
is not assumed repaired. Dated emissions roadmaps are not achieved reductions.

Actual night/day cold buffering can support scheduling and thermal-storage
anchors; a suspect temperature in the same source remains unresolved and
cannot be silently corrected, used as heat fit or converted to energy capacity.
Local heat for auxiliary buildings does not establish the factory process fuel
mix. A hospitality award is not a manufacturing-site management system.

A generic municipal homepage cannot substantiate a company profile merely
because it returns HTTP 200. Retain and block the old attribution, register
an exact named replacement and correct the process-map URL. Issuer tables
require exact row attribution; adjacent firms' ISO 50001 cannot become the
selected company's certification. Animated zero counters, closing force and
hardness are not energy facts. Resource policy and old automation are not a
recent energy-investment inventory. These evidence boundaries apply per field,
without imputing sector averages, missing numeric values or human approval.


## Continuous batch follow-up — 2026-10-07 (03)

Batch NBCC-2026-10-07-03 adds twelve complete 15-field first passes: 67 numeric
proposals awaiting independent human review and 113 blank UNKNOWN research
fields. Current assessment coverage36/100, 540 fields: 250 pending numeric and
290 research gaps. Human approval/canonical score coverage remains unchanged.
Live queue260 ready/142 research/38 review/12 gate; company queue52 code-now/
33 research-first/3 review/12 eligibility-first. Next P56. Canonical deployment,
staff, confidence and numeric inputs plus human-review records are unchanged.

357 sources/387 audited URLs, 373 retrievable; all100 companies covered. The
65-URL follow-up has64 retrieval successes and one old retained404 with partial
recovery. HTTP success does not clear five generic/staging content blockers.
MACK's actual thermoforming replaces unsupported injection mapping. The new
provisional archetype does not invent storage/scheduling; zero matched
opportunity rules is valid while source/readiness/coding coverage remains
complete. Current outputs202 opportunities/197 research tasks. Six certification
facts and one historical claim are corrected by actual holder/date/body/register,
with no automatic score approval. Certificate expiry, reporting dates, expired
goals and planned measures remain separate.
See [full batch boundaries](next_best_company.md#frozen-batch-nbcc-2026-10-07-03).
