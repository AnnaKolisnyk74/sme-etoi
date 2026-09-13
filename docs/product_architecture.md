# SME-ETOI Product Architecture

## Purpose

SME-ETOI is evolving from a research index into a reusable industrial-energy intelligence platform for German SMEs. The platform should reduce repetitive manual market-research work by turning public evidence into structured, auditable and updateable company, process, technology and opportunity intelligence.

The product must never imply knowledge of private customer intent, actual site load, grid capacity, budget or purchase probability when no public evidence exists.

## Product layers

### 1. Company Intelligence

Stores facts about the exact legal entity and relevant linked enterprises:

- company identity and manufacturing sites;
- NACE / process stratum;
- employees, turnover and balance-sheet total;
- SME and group status;
- ISO 50001, ISO 14001 and EMAS;
- energy and decarbonisation measures;
- targets, investments and public projects;
- evidence URLs, dates and confidence.

Primary principle: facts and claims remain traceable to source evidence.

### 2. Process Intelligence

Maps observable industrial processes to technical characteristics that matter for electrification and energy-system analysis.

Examples:

- injection moulding;
- extrusion;
- brewing and boiling;
- pasteurisation;
- refrigeration;
- electroplating;
- anodising;
- drying;
- firing and sintering;
- glass melting.

Each process record should eventually include:

- process family;
- typical temperature range;
- dominant energy service;
- electric-drive relevance;
- process-heat relevance;
- cooling relevance;
- batch / continuous character;
- schedulability;
- thermal inertia / storage potential;
- power-electronics relevance;
- power-quality relevance;
- suitable technologies;
- evidence basis for each generic process assumption.

### 3. Technology Intelligence

Defines technologies and the conditions under which they can be relevant.

Initial technology families:

- industrial heat pumps;
- electric boilers;
- resistance heating;
- induction heating;
- infrared / microwave where applicable;
- variable-frequency drives;
- rectifiers and converters;
- energy-management systems;
- thermal storage;
- battery storage;
- onsite PV integration;
- heat recovery;
- power-quality solutions;
- demand response / load management.

Technology records must distinguish:

- technical applicability;
- economic attractiveness;
- public evidence of existing deployment;
- unknown site-specific constraints.

### 4. Opportunity Engine

Transforms company facts + process facts + technology rules into transparent opportunity signals.

The engine should produce technology-specific outputs such as:

- electrification opportunity;
- industrial-heat opportunity;
- cooling optimisation opportunity;
- energy-management opportunity;
- flexibility opportunity;
- storage opportunity;
- power-electronics opportunity;
- grid / power-quality relevance.

Every result must expose the rule path that produced it.

Example:

```text
Company evidence: >100 injection-moulding machines, three-shift operation
Process model: injection moulding -> high drive relevance + cooling relevance
Technology rules: high drive relevance -> VFD/EMS relevance
Output: Energy-management opportunity = HIGH
Confidence: B
Reason: process evidence + operating-pattern evidence
```

This is not a sales-propensity score unless future validated data supports such a claim.

### 5. Evidence & Audit Layer

Every important fact or score should support:

- source URL;
- direct-document URL where available;
- source type;
- publication / validity date;
- checked date;
- exact claim or extracted fact;
- reviewer;
- confidence;
- change history.

No undocumented manual override should affect a published result.

### 6. Research Queue

The Research Queue converts unresolved opportunity outputs into ordered,
auditable research tasks. It joins the canonical company record to the
opportunity row, identifies the exact missing fact, proposes a focused research
question and records both research priority and decision impact.

Its deterministic first-match rules distinguish time-sensitive commissioning
checks, high-relevance deployment checks, standard deployment checks and gaps
in the evidence model. Each task exposes its rule ID and reasons. There is no
opaque aggregate score and no inference of buying intent.

Research priority answers *which fact should be checked first*. Decision impact
answers *how much resolving that fact can change the current commercial status
or next action*. A failed public search leaves the value `UNKNOWN` or may be
recorded as `NOT_FOUND_AFTER_CHECK`; it never creates commercial white space.

Completed checks are appended to `data/research_results.csv`. This log stores
the exact task key, search scope, finding, source IDs and URLs, prior and
resulting values, checked date, next review date and reviewer. The queue reads
the most recent result and assigns a visible lifecycle state: `OPEN`,
`IN_PROGRESS`, `RECHECK_DUE`, `BLOCKED` or `RESOLVED`.

The results log cannot mutate company intelligence. Positive deployment
evidence must first be reviewed and coded in the canonical company fact layer;
the Opportunity Engine is then rerun. Partial evidence and unsuccessful public
searches remain visible without being converted to negative deployment claims.

### 7. Monitoring & Change Detection

The platform should become longitudinal rather than static.

Track:

- newly published certificates;
- certificate expiry;
- new sustainability / annual reports;
- new energy projects;
- new targets;
- plant expansions;
- ownership changes;
- relevant public investment announcements.

Every company record should eventually expose:

- `last_verified_date`;
- `next_review_date`;
- `change_since_last_review`;
- `change_type`;
- `change_source_url`.

## Data architecture

The project should keep facts, generic process knowledge and derived outputs separate.

```text
raw public evidence
      |
      v
company_facts
      |
      +------------------+
      |                  |
      v                  v
process_mapping     certificate_register
      |
      v
process_library
      |
      v
technology_rules
      |
      v
opportunity_engine
      |
      +------------------+
      |                  |
      v                  v
SME-ETOI         technology opportunities
                          |
                          v
                   research_queue
      |
      v
Power BI / web / exports
```

## Product success criterion

The platform is useful only if it reduces real analytical work.

A future user should be able to answer questions such as:

> Which German industrial SMEs show strong public evidence of heat-pump, electrification, flexibility or energy-management relevance, and what evidence supports that classification?

without manually researching every company from scratch.

## Development sequence

### Phase A — research foundation

- run the deterministic cross-file QA for the complete provisional 20-company pilot;
- independently human-review and double-code the QA-checked pilot before the v1.0 freeze;
- validate inclusion / exclusion logic;
- complete evidence dossiers;
- double-code a subsample;
- freeze SME-ETOI v1.0.

### Phase B — reusable intelligence model

- build process library;
- build technology library;
- define transparent opportunity rules;
- connect companies to one or more processes;
- generate technology-specific opportunity outputs.

### Phase C — scalable dataset

- expand to 100 companies;
- measure missingness and evidence quality;
- automate validation and score generation;
- expose Power BI views and CSV exports.

### Phase D — longitudinal product

- expand to several hundred companies;
- implement scheduled re-check fields and change logs;
- track certificate and project changes over time;
- publish dated releases of the dataset and methodology.

## Guardrails

1. Public evidence is evidence of what is publicly observable, not proof of all activity inside a company.
2. Technical opportunity is not equivalent to buying intent.
3. Generic process assumptions must be documented separately from company-specific evidence.
4. All company-level scores must be reproducible from stored inputs.
5. The model must preserve uncertainty rather than silently filling unknown values.
6. Commercial usefulness must not weaken research traceability.
