# SME Energy Transition Opportunity Index (SME-ETOI)

**Industrial Electrification and Grid Readiness in German SMEs**

An open and reproducible research project examining whether public company and
process data can identify German industrial SMEs whose electrification could
create substantial decarbonisation potential, flexible electricity demand and
grid-integration requirements.

## Current checked state — 9 October 2026

All 100 provisional companies have all 15 fields assessed: **605 `CHECKED`
proposals (Geprüft), 895 blank `NEEDS_RESEARCH` fields and zero approved fields**.
The 554 original numeric proposals remain accounted for (507 confirmed,
42 corrected, five withdrawn); 56 formerly unknown fields now have new evidence.
Source/anchor checking remains separate from personal or final score approval.

Two decision-research blocks cover **20 technical companies, 12 SME/group cases
and two identity conflicts**. The latest ten firms follow the frozen decision
queue after previously profiled and gated firms are excluded. Their 96 open score
fields yield six new checked proposals; 90 remain unknown. Across both blocks,
146 selected gaps were investigated and eight closed. Previously checked proposals
are unchanged by this continuation.

[The latest report](evidence/decision_research_20261009.md),
[profiles](evidence/decision_research_profiles_20261009.json),
[26 source-body checks](evidence/decision_source_checks_20261009.csv) and
[96 field attempts](evidence/field_research_deep_20261009.csv) document dates,
attribution and limitations. A commissioned 2025 machine replacement, an own
management claim, laser marking and a manufacturer-linked machine family support
bounded anchors. Plans, other companies' measures, old network-use permissions,
redacted powers and adjacent timeline years do not become current deployment.

Langer's current ISO 50001 now supplies a sixth public YES fact in the research
ledger; four YES findings correspond to generated queue tasks. Canonical deployment
flags are not silently overwritten. All 12 SME gates stay open pending defensible
group/period decisions. The prior [decision report](evidence/decision_research_20261008.md)
and frozen ledgers remain available; the dashboard shows all 34 profiles and the
latest block separately.

## Research question

> Can publicly available company and process data identify German industrial
> SMEs whose electrification could create substantial decarbonisation potential,
> flexible electricity demand and grid-integration requirements?

The project develops and tests the **SME Energy Transition Opportunity Index
(SME-ETOI)**. It links observable industrial processes to five analytical
dimensions:

1. process-electrification potential;
2. power-electronics relevance;
3. load-flexibility potential;
4. grid and power-quality relevance; and
5. the publicly observed transition gap.

The index is an exploratory research and screening instrument. It does **not**
estimate a site's actual energy consumption, grid-connection capacity,
investment budget or probability of buying a solution.

## Why the project matters

Industrial electrification connects several parts of the energy-technology
ecosystem: customer energy solutions, automation and energy management, power
semiconductors and drives, transformers, voltage regulation, power quality and
distribution-grid planning. SME-ETOI creates a transparent public-data layer
between company-level process evidence and these technology questions.

## Study design

- **Initial pilot:** 20 selected companies, five per process stratum, plus a
  retained audit trail of excluded and unresolved candidates.
- **Current expansion:** 100 provisional companies, twenty-five per process stratum.
- **Final study:** 100 eligible companies in total, 25 per stratum. Following
  the project-owner decision, independent source review is performed after all
  100 provisional records have been assembled.
- **Unit of analysis:** one German operating company/legal entity.
- **Strata:** food and beverage; plastics processing; metal surface treatment
  and heat treatment; glass and technical ceramics.
- **Sampling:** stratified purposive sampling with documented candidates,
  exclusions and replacements.
- **SME eligibility:** fewer than 250 employees and either turnover up to EUR 50
  million or balance-sheet total up to EUR 43 million, including relevant group
  relationships where public evidence permits.

`data/pilot_candidates.csv` is a research queue, not a finished empirical
sample. A candidate moves from `TO_VERIFY` only after its legal entity, group
links and SME eligibility have been checked. Excluded records remain visible
and are replaced transparently.

## Index structure

| Dimension | Maximum |
| --- | ---: |
| Process-electrification potential | 25 |
| Power-electronics relevance | 20 |
| Load-flexibility potential | 15 |
| Grid and power-quality relevance | 15 |
| Publicly observed transition gap | 25 |
| **Total** | **100** |

A separate evidence-confidence grade prevents sparse public communication from
being misclassified as a large transition gap.

## Repository structure

```text
sme-etoi/
├── README.md
├── methodology.md
├── coding_manual.md
├── requirements.txt
├── .github/workflows/tests.yml
├── data/
│   ├── company_template.csv
│   ├── pilot_candidates.csv
│   ├── research_results.csv
│   ├── score_coding_proposals.csv
│   └── synthetic_demo.csv
├── evidence/
│   ├── README.md
│   ├── source_register.csv
│   └── companies/<candidate_id>_<legal_entity>/evidence.md
├── src/
│   ├── opportunity_engine.py
│   ├── research_queue.py
│   ├── validate_score_coding_proposals.py
│   ├── score_readiness.py
│   ├── score_work_queue.py
│   ├── company_work_priority.py
│   ├── run_pipeline.py
│   ├── validate_pilot.py
│   └── score_companies.py
├── outputs/
│   ├── opportunities.csv
│   ├── research_queue.csv
│   ├── score_readiness.csv
│   ├── score_work_queue.csv
│   ├── company_work_priority.csv
│   └── scored_demo.csv
├── web/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── data/sme_etoi.json
└── tests/
    ├── test_opportunity_engine.py
    ├── test_research_queue.py
    └── test_scoring.py
```

## Quick start

Run the current empirical pipeline with one command:

```bash
python src/run_pipeline.py
```

The integrated runner performs deterministic preflight QA, generates
`outputs/opportunities.csv` and `outputs/research_queue.csv`, checks
cross-output invariants and then refreshes the inter-rater reliability outputs.

To validate the full pipeline without writing generated files:

```bash
python src/run_pipeline.py --check-only
```

The individual components can still be run separately when developing or
debugging:

```bash
python src/score_companies.py data/synthetic_demo.csv outputs/scored_demo.csv --as-of 2026-09-12
python src/opportunity_engine.py
python src/research_queue.py
python src/validate_pilot.py
python -m unittest discover -s tests -v
```

The synthetic demo contains fictional records used only to test the pipeline.
It must never be reported as empirical evidence.

The integrated pipeline also refreshes the static web data snapshot at
`web/data/sme_etoi.json`.

The same run also refreshes `outputs/score_readiness.csv`, which records why
each canonical company is or is not ready for a final SME-ETOI score. It keeps
existing provisional scores visible without treating them as final when SME
eligibility, numeric coding or independent human review is still open.

It also refreshes `outputs/score_work_queue.csv`. The work queue keeps
upstream SME-eligibility gates ahead of scoring effort and groups the 15 numeric
anchors into five dimension-level work packages per scoreable company. This
makes the current 100-company workload operational without auto-filling any
numeric score field.

Numeric anchors proposed during AI-assisted or first-pass coding are stored
separately in `data/score_coding_proposals.csv`. They remain
`AWAITING_HUMAN_REVIEW` and do not change canonical scoring inputs or outputs.
The pipeline validates proposal anchors, source ownership and review-state
integrity. See `docs/score_coding_protocol.md`.

Current coding assessments (all numeric values remain non-canonical):

| Company | Numeric proposals | NEEDS_RESEARCH |
| --- | ---: | ---: |
| P04 Neumarkter Lammsbräu | 15 | 0 |
| P19 Glasfabrik Lamberts | 3 | 12 |
| P12 Richard Henkel | 14 | 1 |
| P16 Sembach | 4 | 11 |
| P05 Einbecker Brauhaus | 15 | 0 |
| P18 Glashütte Lamberts Waldsassen | 7 | 8 |
| P22 RIEDENBURGER BRAUHAUS | 15 | 0 |
| P24 H&K Müller | 2 | 13 |
| P23 FM-Plast | 7 | 8 |
| P11 B+T Oberflächentechnik | 5 | 10 |
| P53 Brauerei Rittmayer | 8 | 7 |
| P20 DERIX Glasstudios | 6 | 9 |
| P21 Moritz Fiege | 4 | 11 |
| P27 BCE Special Ceramics | 5 | 10 |
| P30 Privat-Brauerei Zötler | 7 | 8 |
| P31 Brauerei Clemens Härle | 7 | 8 |
| P43 WZR ceramic solutions | 6 | 9 |
| P13 Schmalriede-Zink | 6 | 9 |
| P25 Scheplast | 8 | 7 |
| P15 ELOXAL BARZ | 4 | 11 |
| P26 Barth Galvanik | 8 | 7 |
| P28 Berg Brauerei | 10 | 5 |
| P29 Meckatzer | 11 | 4 |
| P33 Gindele | 6 | 9 |

Current generated work queue: **12 OPEN_GATE, 140 READY_TO_CODE,
248 RESEARCH_NEEDED and 52 AWAITING_HUMAN_REVIEW**. These are task counts,
not proposal-field counts. All 88 companies with numeric-coding work still
await canonical coding and independent human review; no final score is ready.

`outputs/company_work_priority.csv` collapses work into company decisions:
28 `CODE_NOW`, 57 `RESEARCH_FIRST`, 3 `REVIEW_PROPOSALS`, and 12
`ELIGIBILITY_FIRST`. Failed or missing deterministic QA yields `QA_FIRST`;
partially covered coding stays `IN_PROGRESS` rather than claiming complete
review coverage.

The **Next Best Company to Code v2** ranking uses QA as a gate, both confidence
grades, a qualitative documentary information-gain proxy, verified process /
energy-transition / management coverage, unassessed fields and deduplicated
verified URLs. It never estimates numeric scores or assumes deployment.
See [the priority protocol](docs/next_best_company.md) for exact ordering,
limitations, source-type rules and the reproducible batch audit.

The v2 batches selected **P21/P27**, then **P30 Zötler/P31 Härle**, before
their source enrichment or coding. Both selections are frozen in
`data/coding_batch_selections.csv`; all four now require field-specific research.
The first pass is complete for **100/100 companies and 1,500/1,500 fields**.
The live queue has no remaining CODE_NOW company. The web scoring view shows
field coverage, review/research counts, the last frozen ranked batch and the
separate documentary cohort whose group-eligibility gates remain open.

For future sample extensions, freeze a batch from validated, freshly rebuilt
inputs before research. The selector currently fails closed because every
company is already assessed (choose a new batch ID and actual selection date):

```bash
python src/select_coding_batch.py --batch-id <new-batch-id> --selected-date YYYY-MM-DD --size 2
```

This command appends an immutable selection snapshot. It does not generate
proposals, approve reviews or publish scores.

### Web prototype

The [public-source audit](docs/public_source_audit_2026-10-06.md) covers all
100 companies, including coded and uncoded cases: **318 URLs checked, 304
retrievable**. Removed/blocked links, recovered sources and six limited or open
recovery cases remain visible in the **Quellenprüfung** view. Retrieval is an
AI check and never a human review or proof of current certificate/deployment
status. Offline pipeline QA requires complete retrieval coverage and a scoped
investigation for each failure. No new coding batch was started during this audit.

The first product-facing prototype is a dependency-free static web app with
three views:

- Overview
- Company Explorer
- Research Queue

Serve it locally from the repository root:

```bash
python -m http.server 8000 --directory web
```

Then open `http://localhost:8000`.

For an existing local checkout, run `git pull --ff-only` in the repository and
reload the browser with Ctrl+F5. The company table separates checked field
proposals from SME eligibility. Missing public ISO evidence is displayed as
"Kein öffentlicher Nachweis", never as a confirmed absence. Certificate details
include check dates, expiry dates, scope notes and links. Source details separate
URL retrieval from content rechecks; the overview counts follow the current filter.

The frontend reads only the generated public repository snapshot in
`web/data/sme_etoi.json`. It does not call employer systems, CRM data or
private APIs.


## Integrated pipeline

`src/run_pipeline.py` is the canonical orchestration entry point for the
current product prototype. It deliberately builds derived outputs in memory and
validates them before writing files. The pipeline stops if:

- the 100-company sample fails deterministic cross-file QA;
- a canonical company has no generated opportunity;
- unresolved group or ownership checks are missing their SME-eligibility gate;
- SME-eligibility gates are not ranked ahead of downstream deployment research;
- an eligibility-pending company appears actionable; or
- an unknown deployment state is converted into commercial white space.

This keeps product execution reproducible while preserving the project's
research safeguards.

## Research Queue

`src/research_queue.py` joins `data/company_intelligence.csv` to
`outputs/opportunities.csv`, annotates tasks with the latest auditable result
from `data/research_results.csv`, and writes the next unresolved research tasks
to `outputs/research_queue.csv`. It uses a first-match rule hierarchy, not an
aggregate or probabilistic score:

1. verify a dated announced or planned deployment whose commissioning remains
   unresolved;
2. define a missing deployment-evidence model;
3. verify unknown deployment for a HIGH technical opportunity with A/B
   confidence;
4. verify unknown deployment for another HIGH/MEDIUM technical opportunity;
5. defer provisional technical cases behind better-supported research.

`research_priority` controls ordering; `decision_impact` states how strongly a
resolved fact could alter commercial status or next action. The rule ID and
plain-language reasons are exported with every task. `UNKNOWN` and
`NOT_FOUND_AFTER_CHECK` remain uncertainty states: neither creates
`WHITE_SPACE_POSSIBLE`. A task moves to a different commercial status only
after direct positive or explicit negative evidence is coded in the company
fact layer and the opportunity engine is rerun.

### Research-result lifecycle

`data/research_results.csv` is an append-only research log. It records the
defined search scope, checked date, finding, evidence URLs, prior and resulting
values, reviewer and next review date. The queue selects the latest result for
the exact `(company_id, opportunity_type, missing_fact)` key and exposes:

- `OPEN` when no research result exists;
- `IN_PROGRESS` while a defined check is running;
- `RECHECK_DUE` when research produced only partial evidence or no public
  deployment evidence;
- `BLOCKED` when the result conflicts with the current company/opportunity
  state or an external blocker is recorded;
- `RESOLVED` only when the coded company fact and result agree.

Research results never overwrite company facts automatically. A reviewer must
code supported changes in `company_intelligence.csv`, rerun the Opportunity
Engine and then regenerate the queue. This prevents a search log from silently
becoming a factual claim.

## Research roadmap

1. Expand the balanced provisional sample to 100 companies, 25 per stratum.
2. Keep excluded and unresolved candidates visible without silently changing
   the sampling rule.
3. Build a neutral source manifest and independent-coding row for every record.
4. After assembly, independently review and double-code all 100 companies.
5. Test inter-rater reliability, adjudicate every conflict and freeze
   SME-ETOI v1.0.
6. Analyse process-stratum differences and evidence coverage in Python.
7. Build a Power BI dashboard and a 10–15 page research report.

Run the deterministic sample QA before reviewing or merging data changes:

```bash
python src/validate_pilot.py
```

The validator checks balanced expansion stages from 20 to 100 records,
legal-entity consistency, duplicate certificate rows, certificate validity
logic, process/source coverage and the second-pass QA matrix. It deliberately
does not label its own check as an independent human double-code.

## Independent sample validation

The independent reviewer works from the neutral source manifest rather than
the first coder's company facts or dossiers:

```bash
python src/build_double_code_package.py
# Fill data/pilot_double_code.csv independently.
python src/inter_rater_reliability.py
```

The comparison writes field-level agreement and Cohen's kappa to
`outputs/inter_rater_reliability.csv`. Every disagreement is written to
`outputs/double_code_conflicts.csv` for explicit adjudication. Until another
person completes the template, the output correctly reports zero completed
reviews and `UNKNOWN` reliability rather than manufacturing agreement.

See `docs/double_coding_protocol.md` for the blind-review rules and allowed
values.

## Research integrity

No internal employer, CRM, customer or non-public data may enter this project.
Absence of public evidence is never treated as proof that a company has taken no
action. No company-level score is published until the evidence threshold is met.

## Project status

**Current phase:** QA-checked provisional 100-company sample assembled. Company
Intelligence and process mappings contain twenty-five selected cases in each of
the four process strata. The candidate register retains exclusions and unresolved
linked-enterprise cases. Inclusion is not a final eligibility certification:
each record keeps its open financial or group checks, evidence confidence and
review status. A deterministic second-pass QA is recorded for all 100 cases;
independent human source review is deliberately pending until the 100-company
sample is assembled and must occur before SME-ETOI v1.0 is frozen.

## Licence

No licence has been selected yet. Until one is added, standard copyright rules
apply.


The ranked batch `NBCC-2026-10-06-03` assesses P43 WZR ceramic solutions and
P13 Schmalriede-Zink: six human-review-pending numeric proposals and nine research
gaps each. Source content inspection corrects WZR's generic VDI citation and
records Schmalriede's direct current ISO 14001 certificate and dated 2025 ambition,
without inferring an EnMS, target achievement or energy deployment. See
[the batch audit](docs/next_best_company.md#frozen-batch-nbcc-2026-10-06-03).


The ranked batch `NBCC-2026-10-07-01` assesses P25 Scheplast (eight numeric
proposals, seven research gaps) and P15 ELOXAL BARZ (four numeric proposals,
eleven gaps). All twelve new numeric fields await human review. Scheplast's
current direct ISO 14001 successor is recorded without inferring an EnMS;
Barz's historical 2016 supplier case and unverified public energy role do not
prove current technology deployment or a recent investment. After that batch,
twenty of the 100 sample companies had complete 15-field first-pass assessments:
148 numeric proposals were review-pending and 152 fields needed research.
All sample source URLs remain covered by the audit; this follow-up rechecks
ten selected-company URLs, including three newly added URLs (333 in total).
Barth Galvanik (P26) was next at that snapshot; that is a v2 documentary
priority result, not an opportunity score. See
[the frozen batch and evidence limits](docs/next_best_company.md#frozen-batch-nbcc-2026-10-07-01).


Batch `NBCC-2026-10-07-02` adds all 15 fields for **Barth Galvanik, Berg
Brauerei, Meckatzer and Gindele**: 35 numeric proposals awaiting independent
human review and 25 blank-valued research gaps. **24/100 companies** now have
complete fieldwise first-pass assessments (360 rows: 183 pending numeric
proposals, 177 explicit research fields). This is assessment coverage, not
approved scoring: **zero final-score-ready companies**. Four directly sourced
certificate statuses are corrected; canonical deployment UNKNOWNs, numeric
scoring and human review records are unchanged. The complete source inventory
is 352 URLs; all 100 sample companies remain covered. The selected-company
follow-up rechecked 29 URLs (19 new): 28 retrievable, one retained 404 with
its previously verified replacement. Live source counts are distinct from the
historical 318-URL audit snapshot. See
[batch evidence and limits](docs/next_best_company.md#frozen-batch-nbcc-2026-10-07-02).


Batch `NBCC-2026-10-07-03` assesses 12 more companies, all 180 fields:
67 numeric proposals await independent human review; 113 explicit fields need
research. **36/100 companies** now have a complete fieldwise first pass
(540 rows: 250 pending numeric proposals and 290 research gaps). No final score
is ready. Canonical deployment, staff, confidence and scoring inputs plus all
human review records remain unchanged. Six current certificate facts and one
historical claim are sourced separately from scoring.

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

MACK is corrected to actual vacuum thermoforming/CNC, with a separate provisional
process archetype. Unproven injection-moulding flexibility is removed. A firm
can remain fully covered in source/readiness/coding outputs without matching
a current opportunity rule; the pipeline no longer forces an unsupported
opportunity. Generated outputs contain 202 opportunities and 197 research tasks.
The live inventory has 357 registered sources and 387 audited URLs, 373 retrievable.
All 100 sample firms remain source-audited. The latest follow-up GET-checked
65 URLs (64 retrievable and the retained Alpirsbacher values-page 404 with
previous partial recovery). Generic portals and Ehingen TEST-SYSTEM content
remain explicitly blocked despite HTTP success. See
[batch methods and boundaries](docs/next_best_company.md#frozen-batch-nbcc-2026-10-07-03).


Batch `NBCC-2026-10-07-04` adds twelve complete fieldwise first passes,
180 fields: 55 numeric proposals awaiting independent human review and
125 precise research gaps. At the end of this batch, **48/100 companies** had all 15 fields assessed
(720 rows: 305 pending numeric proposals and 415 blank research fields).
No final score is ready. Actual human-review coverage remains unchanged;
AI first pass never becomes APPROVED automatically.

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

Dorn/Si-Tech ISO 14001 certificates and annex were visually inspected; ceram's
claim is corrected to CLAIM_ONLY, with a historical PDF404 retained explicitly.
Partner toolshops, stock imagery, theoretical SPC and customer energy products
do not count as owned equipment. Dorn's actual950kWh electrical battery feeds
site integration, never thermal storage or a fabricated commissioning date.
TechnoKer's biogas claim and Bio-LPG delivery remain distinct. Historical
heat export, test temperatures and 2024 cellar capacity retain their boundaries.

Live inventory: 394 registered sources, 424 audited URLs, 409 retrievable;
all 100 sample firms covered. The 67-URL follow-up found 66 retrievable URLs
and the new ceram404, with scope-limited claim recovery. Two reachable generic
sources remain content-blocked. Queue: 200 ready, 197 research, 43 review and
12 gates. Company queue: 40 code-now, 45 research-first, three review and
twelve eligibility-first. Canonical scores/deployment/staff/confidence and
prior proposals/human review records unchanged.
See [full batch boundaries](docs/next_best_company.md#frozen-batch-nbcc-2026-10-07-04).


## Continuous batch follow-up — 2026-10-07 (05)

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


## Continuous ranked batch 06 — 7 October 2026

Batch `NBCC-2026-10-07-06` completes the 15-field first pass for P95,
P97, P98, P100, P101, P105, P106, P108, P109, P110, P37 and P60. Selection
was frozen after PR #44 before source enrichment or process corrections.
It adds 68 numeric proposals awaiting independent human review and 112 blank
`NEEDS_RESEARCH` fields with UNKNOWN confidence. Assessment coverage at completion of that historical batch was
**72/100 companies and 1,080/1,500 fields**: 443 numeric proposals pending
review and 637 research gaps. No company has a final approved score.

Owner equipment/process PDFs establish Dornstetten's electric injection
machines and more than 20 sintering systems at about 1,400/1,650 C. The new
Kläger SPC machine is a different entity's investment and is excluded from
Dornstetten. Existing room heat pumps and 2010 PV are not recent process-heat
CAPEX. PECO's separately dated 2022/2024 efficient-machine investments are
within the five-year window; 24-hour operation is not load-shifting permission.

Metoba's image-only EMAS certificate was read visually: issued 15 January
2026, valid until 30 September 2029, despite the 2025 filename. An explicit
validity start is not stated. The active official register corroborates the
entity. Its historical brochure explicitly says the ISO-50001-based EnMS is
not certified. Environmental management and BHKW operation do not establish
current EnMS maturity or a BHKW commissioning date. Owner-linked DEKRA bodies
verify current ISO 14001 for atka (31 July 2025–28 July 2028) and Dresdner
Silber (23 December 2025–22 December 2028).

Vuckovic's owned route is CNC/ultrasound ceramic-component machining; no owned
kiln is established. Provisional `PR013` retains UNKNOWN heat/flex/storage
topology and has no supported opportunity rule. Triptis's current imprint
names Eschenbach Porzellan GmbH, not the sampled Neue Porzellanfabrik Triptis
GmbH. A historic FAQ and 2024 brand return cannot establish legal/operational
continuity. `PR012` prevents unsupported kiln opportunities; all its 15 fields
remain UNKNOWN and accessible imprint/FAQ sources remain content-blocked.
No unverified closure assertion or canonical eligibility change is made.
Both firms retain source, readiness and coding research coverage.

Nymphenburg's water power drives mechanical belts; it is not owned electric
generation or electric motor evidence. Its firing runs up to 36 hours, which
is not a shifting window. Reichenbach's firing temperatures are 950/1,380 C,
but the carrier remains unknown. atka's stated PV `630 kwP` is interpreted as
nameplate kWp, not generated kWh; waste heat warms offices/halls. Hartchrom
Beck's 60,000 A plating line cannot become kW without voltage. Generic
resource sustainability and quality-system claims do not fill energy gaps.

At completion of historical batch06, dimension-level work queue: 80 `READY_TO_CODE`, 299 `RESEARCH_NEEDED`,
61 `AWAITING_HUMAN_REVIEW`, 12 `OPEN_GATE`. Company actions: 16 `CODE_NOW`,
69 `RESEARCH_FIRST`, three `REVIEW_PROPOSALS`, 12 `ELIGIBILITY_FIRST`.
The next ranked company at that historical point was **P71 Flötzinger Brauerei**. Outputs then contained 198
opportunities and 192 research tasks. Source inventory: 463 registered
sources, 498 audited URLs and 483 retrievable URLs across all 100 sample firms.
The follow-up checked 62 batch URLs plus three new redirect destinations;
four retained retrieval failures are separate from content/holder blockers.
Prior proposals, canonical numeric/deployment/staff/confidence fields and
independent human-review records remain unchanged.


## Historical 100-company first pass before source recheck — 7 October 2026

**100/100 companies now have all 15 fields assessed: 1,500/1,500 unique
company-field entries.** There are 554 numeric proposals awaiting independent
human review and 946 blank `NEEDS_RESEARCH` fields with UNKNOWN confidence.
Coverage counts field assessment, not evidence sufficiency or approved scores.
No human approval, final score or deployment status is inferred.

The final eligible ranked cohort `NBCC-2026-10-07-07` freezes P71, P72, P73,
P74, P78, P82, P85, P86, P89, P96, P99, P102, P103, P107, P62 and P03 before
enrichment. The remaining 12 companies were separately frozen in
`data/eligibility_coding_selections.csv` as `GATE-ASSESS-2026-10-07`:
P07, P10, P104, P32, P34, P40, P42, P46, P47, P65, P67 and P88.
Their documentary assessment fulfils full sample coverage while their upstream
group checks remain OPEN_GATE and canonical scoring stays blocked. They never
enter the eligible CODE_NOW selection. The first twelve assessments predate the
ranked-batch manifest; their first-pass records are retained in the pre-recheck snapshot.

At that first-pass snapshot, company workflow was 85 `RESEARCH_FIRST`, three `REVIEW_PROPOSALS`,
12 `ELIGIBILITY_FIRST`, zero `CODE_NOW`. The dimension queue has 377
`RESEARCH_NEEDED`, 63 `AWAITING_HUMAN_REVIEW` and 12 `OPEN_GATE` tasks;
all 440 numeric dimension tasks remain separate from the 1,500 field entries.
There are 198 opportunities, 192 opportunity research tasks and no final-score-ready
companies. The web view reports complete documentary coverage and the open
review/research/eligibility work, with no empty next-company card.

Exact-holder certificate bodies confirm current ISO 50001 for Hermsdorf,
Hofmann, Kessel and Holder. Hofmann's ISO 50001 expires 4 June 2028 while its
ISO 14001 expires 14 March 2028. OT's linked ISO 14001 expired 27 July 2026;
accessible HTTP200 does not restore validity. Current ISO 14001 is also checked
for Varioplast, DOCERAM, PEKA and Wigl. Certificate filename years, first
registration dates and another group entity's certificates are not current
holder/period evidence.

Flötzinger's architect documents one completed October2024 Schechen building
project with PV/heat pump while the Rosenheim brewhouse remains separate.
Kundmüller's 2020 brewhouse and 2025 awards do not establish commissioning in the
five-year investment window. Hochdorfer explicitly documents all brewery heat
from woodchips, supporting zero fossil displacement from an affirmative baseline.
Green-gas procurement, purchased renewable electricity and a solar-beer label do
not independently establish a physical process heat-carrier balance.

Frömgen's recovered own machine-park page explicitly confirms several sintering
furnaces, CNC machines and automated finishing. Its furnace maximum1700C is
capability rather than an actual operating-temperature range; inert atmosphere
is not heating fuel. German Meissen sintering is confirmed separately, while
group1600–1800C temperatures and Swiss ISO14001 are not inherited. Ceramic
heat-exchanger products likewise do not prove owner heat recovery.

The completion adds 420 field entries: 111 pending numeric proposals and 309
explicit research gaps. Before-enrichment source/mapping fixtures reproduce the
last16 ranked selection. Existing proposal and selection prefixes, canonical
numeric/deployment/staff/confidence fields and actual human-review records are
preserved. Only bounded source links, process evidence and body-verified
certificate statuses are updated.

Before recheck, the source inventory had 516 source records, 551 audited URLs and
536 retrievable URLs across all100 firms. The completion checks121 URLs,
including new redirect endpoints and the recovered Frömgen machine park.
The three completion retrieval failures remain explicit: two Dibbern403 pages
and Erlemann/Huckenbeck502; alternative primary/company-authored evidence is
bounded rather than used to invent operating details.
