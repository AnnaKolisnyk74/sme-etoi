# SME Energy Transition Opportunity Index (SME-ETOI)

**Industrial Electrification and Grid Readiness in German SMEs**

An open and reproducible research project examining whether public company and
process data can identify German industrial SMEs whose electrification could
create substantial decarbonisation potential, flexible electricity demand and
grid-integration requirements.

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

## Pilot design

- **Pilot:** 20 selected companies, five per process stratum, plus a retained
  audit trail of excluded and unresolved candidates.
- **Final study:** 100 eligible companies in total, 25 per stratum (the 20 validated pilot records plus 80 additional records).
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
│   └── synthetic_demo.csv
├── evidence/
│   ├── README.md
│   ├── source_register.csv
│   └── companies/<candidate_id>_<legal_entity>/evidence.md
├── src/
│   ├── opportunity_engine.py
│   ├── research_queue.py
│   └── score_companies.py
├── outputs/
│   ├── opportunities.csv
│   ├── research_queue.csv
│   └── scored_demo.csv
└── tests/
    ├── test_opportunity_engine.py
    ├── test_research_queue.py
    └── test_scoring.py
```

## Quick start

```bash
python src/score_companies.py data/synthetic_demo.csv outputs/scored_demo.csv --as-of 2026-09-12
python src/opportunity_engine.py
python src/research_queue.py
python -m unittest discover -s tests -v
```

The synthetic demo contains fictional records used only to test the pipeline.
It must never be reported as empirical evidence.

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

1. Independently review the provisional legal-entity, group and SME decisions
   for the complete 20-company pilot.
2. Keep excluded and unresolved candidates visible without silently changing
   the sampling rule.
3. Independently double-code the 20-company pilot.
4. Test inter-rater reliability and weight sensitivity.
5. Freeze SME-ETOI v1.0 before expanding the validated pilot to the 100-company final sample.
6. Analyse process-stratum differences and evidence coverage in Python.
7. Build a Power BI dashboard and a 10–15 page research report.

## Research integrity

No internal employer, CRM, customer or non-public data may enter this project.
Absence of public evidence is never treated as proof that a company has taken no
action. No company-level score is published until the evidence threshold is met.

## Project status

**Current phase:** complete provisional 20-company pilot. Company Intelligence
and process mappings contain five selected cases in each of the four process
strata. The candidate register retains three exclusions and four unresolved
linked-enterprise cases. Inclusion is not a final eligibility certification:
each record keeps its open financial or group checks, evidence confidence and
review status. All pilot records remain subject to independent user review and
double-coding before SME-ETOI v1.0 is frozen.

## Licence

No licence has been selected yet. Until one is added, standard copyright rules
apply.
