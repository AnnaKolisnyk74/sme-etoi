# Methodology v0.2

## 1. Analytical claim

This study tests whether public information is sufficient for a reproducible
classification of industrial electrification and grid-readiness opportunities
in German SMEs. It does not predict purchases or infer actual energy use,
connection capacity or electrical demand from generic company characteristics.

The central output is SME-ETOI, ranging from 0 to 100. A separate
evidence-confidence grade prevents poorly documented companies from being
classified merely because few measures were found.

## 2. Sub-questions

1. How much of the process and energy information required by SME-ETOI is
   publicly observable?
2. Which process strata show the strongest observable electrification,
   power-electronics and flexibility relevance?
3. Which public process signals are useful proxies for grid and power-quality
   relevance without claiming actual load?
4. How strongly does the publicly observed transition gap affect the ranking?
5. Do classifications remain stable under alternative weights and thresholds?
6. Can a second reviewer reproduce the coding of a 20% subsample?

## 3. Pilot strata

| Stratum | Typical observable processes | Research relevance |
| --- | --- | --- |
| Food and beverage | refrigeration, hot water, steam, drying, cleaning | heat pumps, heat recovery, thermal storage, flexible cold loads |
| Plastics processing | injection moulding, extrusion, compounding, cooling | drives, electric heating, power conversion, process cooling |
| Metal surface/heat treatment | galvanising, anodising, coating, drying, furnaces | rectifiers, electric heat, harmonics, compressed air, power quality |
| Glass and technical ceramics | melting, reheating, firing, sintering | high-temperature electrification, continuous loads, grid reinforcement |

The study proceeds in two stages:

1. **Pilot sample:** 20 eligible companies, with five firms per process stratum.
   The pilot tests the coding manual, evidence availability, scoring anchors and
   reviewer agreement. Excluded candidates are replaced so that the completed
   pilot contains 20 eligible companies.
2. **Main sample:** 100 eligible companies in total. After the pilot has been
   reviewed and the scoring model frozen, the 20 eligible pilot records are
   rechecked under the frozen rules and 80 additional companies are added. The
   same identity, eligibility, evidence and scoring rules apply to every record.

Candidates are deliberately heterogeneous in region, scale, process and apparent
transition maturity. Pilot records are not presented as the final main sample.

## 4. Inclusion and exclusion

Company identity is anchored to the exact legal-entity name shown in the
company imprint and, where necessary, verified against an official register.
Brands, trading names, plants, shops and locations are recorded separately and
must not replace the legal entity name.

Include a company only when all conditions are met:

- it operates a manufacturing site in Germany;
- firm-specific public evidence identifies at least one relevant process;
- public evidence supports probable SME status;
- the legal entity and relevant group relationship can be identified;
- a company source and at least one official or credible independent source can
  be checked.

Exclude or hold as unresolved when the company belongs to a non-SME group, the
German site is not manufacturing, the legal entity cannot be resolved, or SME
eligibility cannot be supported. Record every replacement and exclusion.

## 5. Index definition

### A. Process-electrification potential: 0–25

| Component | Range | Meaning |
| --- | ---: | --- |
| Temperature/technology fit | 0–10 | Process fit with established electric-heat technologies |
| Process-electrification maturity | 0–10 | Technical maturity and applicability for the identified process |
| Fossil-heat displacement potential | 0–5 | Evidence that material thermal service could plausibly be displaced |

### B. Power-electronics relevance: 0–20

| Component | Range | Meaning |
| --- | ---: | --- |
| Motor and drive intensity | 0–8 | Relevance of pumps, compressors, fans, extruders or drives |
| Power-conversion intensity | 0–8 | Use cases for converters, rectifiers or controlled electric heat |
| Automation and control relevance | 0–4 | Potential value of sensing and coordinated control |

### C. Load-flexibility potential: 0–15

| Component | Range | Meaning |
| --- | ---: | --- |
| Production-scheduling flexibility | 0–8 | Batch, buffer or schedulable processes that may shift load |
| Thermal-storage flexibility | 0–7 | Cold stores, hot-water buffers or thermal inertia |

### D. Grid and power-quality relevance: 0–15

| Component | Range | Meaning |
| --- | ---: | --- |
| Incremental-load relevance | 0–8 | Plausible scale of new electrical demand from process conversion |
| Power-quality relevance | 0–4 | Potential relevance of harmonics, reactive power, peaks or voltage stability |
| Onsite-energy integration | 0–3 | Fit with PV, storage, microgrids or load management |

These are ordinal public-data proxies. They are not estimates of kW, MW, MWh,
grid voltage level or connection cost.

### E. Publicly observed transition gap: 0–25

| Component | Range | Meaning |
| --- | ---: | --- |
| Concrete-measures gap | 0–10 | Few documented implemented measures after adequate search |
| Management-system gap | 0–5 | No verified ISO 50001/EMAS evidence after defined checks |
| Target/roadmap gap | 0–5 | No specific dated target or implementation roadmap found |
| Recent-investment gap | 0–5 | No relevant investment found in the lookback period |

Higher gap values mean a larger **publicly observed** gap, not proof that no
internal action exists.

```text
SME-ETOI = Electrification + Power electronics + Flexibility + Grid relevance + Gap
```

Provisional bands: 0–39 Low, 40–69 Medium, 70–100 High. A band is assigned only
with evidence confidence A or B; confidence C produces `RESEARCH_REQUIRED`.

## 6. Evidence confidence

Each completed source family contributes 20 coverage points: company website;
annual, sustainability or environmental report; official company/register
information; certification source; credible independent source.

- **A:** coverage at least 80 and newest relevant evidence no older than 24 months;
- **B:** coverage at least 60 and newest relevant evidence no older than 48 months;
- **C:** otherwise.

## 7. Source hierarchy

1. Official registers, government sources and certification databases.
2. Company annual, sustainability and environmental reports.
3. Company process pages, press releases and technical descriptions.
4. Reputable trade press, public funding pages and provider case studies.
5. Search-result snippets only for discovery, never final coding.

Every numeric code requires a source URL and evidence note. A corporate claim
proves that the claim was published, not that the stated effect was achieved.

## 8. Validation

- independently double-code 20% of pilot records;
- calculate Cohen's kappa for categorical fields and agreement for numeric scores;
- reconcile disagreements and revise ambiguous anchors;
- vary each dimension weight by plus/minus 20%, re-normalise and report band stability;
- report missingness, exclusions, evidence coverage and classification rate;
- freeze the model before collecting the main sample.

## 9. Limitations

- Public disclosure differs by company size and communication capacity.
- Absence of public evidence is not absence of action.
- SME status and group links can remain uncertain.
- Process proxies may not reflect site-specific operating conditions.
- Grid relevance cannot be converted into actual load without site and network data.
- The purposive sample is not nationally representative.
- SME-ETOI is a transparent exploratory index, not a predictive model.
