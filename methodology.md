# Methodology v0.1

## 1. Analytical claim

This study tests whether public information is sufficient for a **reproducible opportunity classification**. It does not test whether a company will buy a solution, and it does not infer actual consumption from silence on a website.

The central output is the Energy Transition Opportunity Index (ETOI), ranging from 0 to 100. A separate evidence-confidence grade prevents poorly researched companies from being classified merely because few measures were found.

## 2. Sub-questions

1. How much of the information needed for the ETOI is publicly observable?
2. Which sectors show the highest median demand potential and solution applicability?
3. How strongly does the observed transition gap change the overall ranking?
4. Do classifications remain stable under plausible alternative weights and thresholds?
5. Can a second reviewer reproduce the coding of a 20% subsample?

## 3. Hypotheses

- **H1:** At least 70% of sampled firms can be assigned an A or B evidence-confidence grade.
- **H2:** The distribution of demand-potential scores differs across the four sector strata.
- **H3:** ISO 50001 or EMAS evidence is positively associated with visible concrete transition measures, but does not perfectly predict them.
- **H4:** At least 80% of classified firms retain their Low/Medium/High band when each dimension weight is varied by plus or minus 20% and weights are re-normalised.

H1 and H4 are provisional feasibility thresholds, not findings.

## 4. Inclusion and exclusion

Include a company when all conditions are met:

- it has a manufacturing site in Germany;
- its main activity fits one of the selected NACE divisions;
- public evidence supports probable SME status;
- the legal entity and relevant group relationship can be identified;
- at least a company website and one independent or official source can be checked.

Exclude or hold as unresolved when:

- it is clearly controlled by a non-SME group;
- the German site is only sales, administration or logistics;
- company identity cannot be resolved;
- evidence is too sparse to assess SME eligibility.

Record every exclusion and reason. Never silently replace difficult cases.

## 5. Sampling

### Pilot

Select 20 firms across the four strata, with variation in region and apparent company size. The pilot is deliberately heterogeneous to reveal coding failures.

### Main study

Select 30 eligible firms per stratum. Within each stratum, document the candidate list, ordering rule, replacements and exclusions. Because no complete open national sampling frame is assumed, the design is stratified purposive rather than probabilistic. No prevalence claim for all German SMEs is permitted.

## 6. Index definition

### A. Demand potential: 0–40

| Component | Range | Meaning |
| --- | ---: | --- |
| Sector energy profile | 0–15 | Typical heat, cold, compressed-air or electricity intensity of the activity |
| Process evidence | 0–15 | Firm-specific evidence of relevant production processes or equipment |
| Site scale | 0–10 | Observable indicators of production scale, not assumed energy use |

### B. Solution applicability: 0–30

| Component | Range | Meaning |
| --- | ---: | --- |
| Low/medium-temperature fit | 0–10 | Potential for heat pumps, heat recovery or related solutions |
| Electrification fit | 0–10 | Technical maturity of electrification for the observed process |
| Flexibility/onsite fit | 0–10 | Observable fit for PV, storage, load management or cold-storage flexibility |

### C. Observed transition gap: 0–30

| Component | Range | Meaning |
| --- | ---: | --- |
| Concrete-measures gap | 0–12 | Few or no publicly documented implemented measures after adequate search |
| Management-system gap | 0–6 | No verified ISO 50001/EMAS evidence after registry and website checks |
| Target/roadmap gap | 0–6 | No specific dated target or implementation roadmap found |
| Recent-investment gap | 0–6 | No relevant investment announced in the defined lookback period |

Higher values indicate a larger *publicly observed* gap. They never establish that no internal action exists.

### Overall score

```text
ETOI = Demand potential + Solution applicability + Observed transition gap
```

Provisional bands:

- 0–39: Low
- 40–69: Medium
- 70–100: High

Bands are assigned only for confidence A or B. Confidence C produces `RESEARCH_REQUIRED`.

## 7. Evidence confidence

Coverage weights:

- company website checked: 20 points;
- annual, sustainability or environmental report checked: 20 points;
- official company/register information checked: 20 points;
- ISO/EMAS or equivalent certification source checked: 20 points;
- credible independent source checked: 20 points.

Confidence additionally depends on the most recent relevant evidence:

- **A:** coverage at least 80 and newest evidence no older than 24 months;
- **B:** coverage at least 60 and newest evidence no older than 48 months;
- **C:** otherwise.

The rules distinguish `not found after a defined search` from `not researched`.

## 8. Source hierarchy

1. Official registers, government sources and certification databases.
2. Company annual, sustainability and environmental reports.
3. Company website, press releases and technical project descriptions.
4. Reputable trade press, funding-project pages and technology-provider case studies.
5. Search-result snippets are discovery aids only and cannot support a final code.

For every scored claim, store at least one source URL and an evidence note. A company statement proves that the statement was made, not that the measure achieved the claimed effect.

## 9. Validation plan

- Independently double-code 20% of the pilot records.
- Calculate Cohen's kappa for categorical fields and intraclass correlation or absolute score differences for numeric components.
- Manually reconcile disagreements and revise ambiguous coding instructions.
- Vary each dimension weight by plus/minus 20%, re-normalise to 100 and report band stability.
- Compare companies with verified ISO 50001/EMAS evidence against those without verified evidence, while avoiding causal language.
- Report missingness, excluded firms, source coverage and classification rate by sector.

## 10. Main limitations

- Public communication differs by firm size and marketing sophistication.
- Absence of public evidence is not absence of action.
- SME status and corporate links may be uncertain.
- Sector-level process assumptions can misclassify unusual firms.
- The sample is not representative of all German industrial SMEs.
- The ETOI is a transparent index, not a validated predictive model.
