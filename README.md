# SME Energy Transition Opportunity Index (SME-ETOI)

**Mapping Industrial Energy-Transition Opportunity in German SMEs**

An open, reproducible research project examining whether public company and
process data can identify German industrial SMEs with substantial potential for
energy-transition solutions.

## Research question

**To what extent can publicly available company and process information support a transparent and reproducible classification of German industrial SMEs by energy-transition opportunity?**

The project develops and tests an **Energy Transition Opportunity Index (ETOI)**. It combines publicly observable indicators of:

1. energy-demand potential,
2. technical solution applicability, and
3. the observed transition gap.

The index is an exploratory decision-support instrument. It does **not** estimate actual energy consumption, prove that a company has taken no action, or predict sales conversion.

## Study design

- **Pilot:** 20 companies, five from each sector.
- **Main study:** 120 companies, 30 from each sector.
- **Unit of analysis:** one German operating company/legal entity.
- **Sectors:** food manufacturing (NACE C10), beverages (C11), rubber and plastics (C22), fabricated metal products (C25). For the 20-company pilot, C10 and C11 may be combined into one 10-company food-and-beverage stratum while retaining separate NACE codes.
- **Sampling:** transparent stratified purposive sample. Results describe the sample and are not nationally representative.
- **SME rule:** fewer than 250 employees and either turnover up to EUR 50 million or balance-sheet total up to EUR 43 million, including relevant group relationships where public information permits.
- **Evidence cut-off:** every source is recorded with URL, date, source type and quoted/paraphrased evidence.

The EU definition and its group caveat are documented by the [European Commission](https://single-market-economy.ec.europa.eu/smes/sme-fundamentals/sme-definition_en). The process-technology logic is anchored in the [German Environment Agency study on CO2-neutral industrial process heat](https://www.umweltbundesamt.de/themen/industrielle-prozesswaerme-kann-bis-2045-co2), which shows that electrification readiness differs substantially by application and industry. EMAS status can be checked in the [German EMAS register](https://www.emas-register.de/).

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

`synthetic_demo.csv` contains fictional records used only to test the pipeline. It must never be reported as empirical evidence.

## Milestones

1. Freeze research question, inclusion rules and ETOI v0.1.
2. Collect and double-code the 20-company pilot.
3. Test inter-rater reliability and weight sensitivity.
4. Revise the index once and document all changes.
5. Collect the 120-company main sample.
6. Analyse sector differences and evidence coverage in Python.
7. Build a Power BI dashboard and a 10–15 page research report.

## Planned outputs

- public-source dataset with an evidence trail,
- reproducible Python analysis,
- Power BI dashboard,
- methodology and limitations,
- research report,
- GitHub release and LinkedIn publication.

No internal employer, CRM, customer or non-public data may enter this project.

## Project status

**Current phase:** research design and synthetic pipeline validation. No real
company has yet been classified, and the scoring model remains subject to pilot
testing, inter-rater reliability assessment and sensitivity analysis.

## Licence

No licence has been selected yet. Until one is added, standard copyright rules
apply.
