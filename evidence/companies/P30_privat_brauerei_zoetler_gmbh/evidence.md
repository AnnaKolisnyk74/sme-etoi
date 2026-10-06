# P30 — Privat-Brauerei Zötler GmbH

## Inclusion status

- Batch: 02 (companies 21-40 of the planned 100-company final study)
- Process stratum: `food_beverage`
- SME status: `probable`; final financial and linked-enterprise review remains open
- Independent human source review: `PENDING`

## Supported process relevance

The checked public evidence supports **brewing; boiling; fermentation; maturation and filling**. The company is mapped to `PR003` for technical screening. This mapping does not prove a specific energy technology is installed and does not imply buying intent.

## Certificates and deployments

- ISO 50001: `NOT_FOUND_AFTER_CHECK`
- ISO 14001: `NOT_FOUND_AFTER_CHECK`
- EMAS: `DOCUMENT_FOUND_VALIDITY_UNCLEAR`
- Unverified deployment fields remain `UNKNOWN`.
- `NOT_FOUND_AFTER_CHECK` means only that no public direct evidence was located in the defined check.

## Sources

- `S-P30-01` — [Privat-Brauerei Zötler: Impressum](https://www.familien-braukunst.de/impressum/) — Exact legal entity and production location.
- `S-P30-02` — [Privat-Brauerei Zötler: Quality and sustainability](https://www.zoetler.de/) — Brewing and EMAS company statement; registration validity open.

## AI first-pass coding — 2026-10-06

Frozen selection: `NBCC-2026-10-06-02`, rank 1, v2 policy, B/B confidence,
QA PASS, HIGH documentary gain. This is automated selection, not Anna's review.

- `S-P30-03` — [Quality and environment](https://www.zoetler.de/qualitaet-und-umwelt.html): company energy measures and EMAS claim. The linked 2023 report returned HTTP 404; current validity remains unresolved.
- `S-P30-04` — [Maturation cellar](https://www.zoetler.de/reifekeller.html): 2025 completion and individually controlled jacket cooling; no independently verified savings or usable load shifting.
- `S-P30-05` — [Brewing motivation](https://www.zoetler.de/motivation.html): individual brews and fermentation/maturation durations, not a proven thermal buffer.

Seven proposals cover control, weak scheduling, one onsite use case, observed
measures, unresolved management validity, vague targets and one dated investment.
All remain `AWAITING_HUMAN_REVIEW`; reviewer and review date are blank.
Eight fields remain `NEEDS_RESEARCH`: temperature fit, process electrification,
fossil-heat displacement, motors, power conversion, thermal storage,
incremental load and power quality. Their values remain blank, confidence UNKNOWN.
No canonical deployments, certification records or scores are changed.

## Remaining limitations after coding

The legal entity and process are supported, but complete financial aggregation, ownership links, certification validity and site-level energy deployments remain subject to Anna's final review after the 100-company sample is assembled.


## Public-source retrieval audit — 2026-10-06 (AI first pass)

- Original: https://www.zoetler.de/download/zoetler-nachhaltigkeitsbericht_emas2023.pdf — NO_EQUIVALENT_FOUND. Replacement/context IDs: `S-P30-03`. Reachable company sustainability page states that declaration is being revised; only company EMAS claim remains. Open: Direct current environmental statement and registration validity remain unresolved.

See `evidence/source_link_audit.csv` for GET status and `evidence/source_recovery.csv` for exact scope. Retrieval/recovery is not Anna's Human Review; scores, certificate validity and deployment UNKNOWNs are unchanged.
