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

- **Pilot:** 20 candidate companies, five per process stratum.
- **Main study:** 120 eligible companies, 30 per stratum.
- **Unit of analysis:** one German operating company/legal entity.
- **Strata:** food and beverage; plastics processing; metal surface treatment
  and heat treatment; glass and technical ceramics.
- **Sampling:** stratified purposive sampling with documented candidates,
  exclusions and replacements.
- **SME eligibility:** fewer than 250 employees and either turnover up to EUR 50
  million or balance-sheet total up to EUR 43 million, including relevant group
  relationships where public evidence permits.

`data/pilot_candidates.csv` is a research queue, not a finished empirical
sample. Every candidate remains `TO_VERIFY` until its legal entity, group links
and SME eligibility have been checked.

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
│   └── synthetic_demo.csv
├── src/
│   └── score_companies.py
├── outputs/
│   └── scored_demo.csv
└── tests/
    └── test_scoring.py
```

## Quick start

```bash
python src/score_companies.py data/synthetic_demo.csv outputs/scored_demo.csv --as-of 2026-09-12
python -m unittest discover -s tests -v
```

The synthetic demo contains fictional records used only to test the pipeline.
It must never be reported as empirical evidence.

## Research roadmap

1. Verify the legal entity, group relationship and SME eligibility of all pilot
   candidates.
2. Replace ineligible candidates without silently changing the sampling rule.
3. Collect and independently double-code the 20-company pilot.
4. Test inter-rater reliability and weight sensitivity.
5. Freeze SME-ETOI v1.0 before collecting the 120-company main sample.
6. Analyse process-stratum differences and evidence coverage in Python.
7. Build a Power BI dashboard and a 10–15 page research report.

## Research integrity

No internal employer, CRM, customer or non-public data may enter this project.
Absence of public evidence is never treated as proof that a company has taken no
action. No company-level score is published until the evidence threshold is met.

## Project status

**Current phase:** pilot-candidate verification and synthetic pipeline
validation. No real company has yet been scored.

## Licence

No licence has been selected yet. Until one is added, standard copyright rules
apply.
