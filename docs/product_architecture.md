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

Opportunity outputs also expose sample eligibility separately from technical and
commercial status:

- `sample_eligibility_status`: `ELIGIBILITY_PENDING`, `PROVISIONAL_PASS`,
  `CONFIRMED` or `EXCLUDED`;
- `actionability_status`: `ELIGIBILITY_BLOCKED`, `PROVISIONAL` or
  `ACTIONABLE`;
- `eligibility_next_action`: the explicit next step required before the case
  can be treated as an actionable SME opportunity.

An unresolved group or ownership check therefore does not erase technical
relevance or deployment evidence. It blocks actionability instead. This keeps
three distinct questions separate:

1. Is the technology technically relevant?
2. What is publicly known about deployment?
3. Is the company currently eligible and reviewed enough to be treated as an
   actionable SME-pilot case?

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

### 6. Score Readiness & SME-ETOI Scoring

The canonical 0–100 SME-ETOI methodology remains the model defined in
`methodology.md` and implemented by `src/score_companies.py`. The platform
must not create a second aggregate score from opportunity-engine outputs merely
because those signals are already available.

Before a company can receive a final SME-ETOI score, the Score Readiness layer
checks the prerequisites required by the existing methodology:

- SME / linked-enterprise eligibility is sufficiently resolved;
- at least one firm-specific process mapping exists;
- ISO 50001, ISO 14001 and EMAS checks each have a non-pending result;
- every numeric scoring anchor has been explicitly coded from evidence;
- independent human review has been completed.

The deterministic output is written to `outputs/score_readiness.csv`.

Possible score states include:

- `NOT_SCOREABLE_ELIGIBILITY`
- `NOT_SCOREABLE_PROCESS`
- `NOT_SCOREABLE_CERTIFICATES`
- `NEEDS_NUMERIC_CODING`
- `PROVISIONAL_SCORE_ONLY`
- `FINAL_SCORE_READY`
- `EXCLUDED`

Existing pilot scores remain visible for auditability, but if a gate is still
open they are labelled `LEGACY_PROVISIONAL_NOT_FINAL` rather than silently
presented as final results.

This layer deliberately separates **score existence** from **score validity**.

### 7. Scoring Work Queue

Score Readiness answers whether a company may be scored. The Scoring Work Queue
answers what should be worked on next.

The deterministic queue is produced by `src/score_work_queue.py` and written
to `outputs/score_work_queue.csv`.

Work is ordered in two stages:

1. unresolved SME / linked-enterprise eligibility gates first;
2. numeric coding only for companies whose eligibility, process-mapping and
   certificate-check prerequisites already pass.

Numeric work is grouped into the five SME-ETOI dimensions rather than split
into 15 disconnected field tasks:

- process-electrification potential;
- power-electronics relevance;
- load-flexibility potential;
- grid and power-quality relevance;
- publicly observed transition gap.

Every package exposes the exact `required_fields`, currently
`missing_fields`, evidence and process confidence, source count, queue reason
and the next coding instruction. Higher-evidence cases are queued before weaker
ones so the first coding passes are both efficient and methodologically
defensible.

The queue never assigns a numeric anchor. It only identifies explicit coding
work. Eligibility-blocked companies cannot receive numeric-coding tasks.

Coding proposals feed back into the work queue without mutating canonical
scores. A dimension can therefore move through:

- `READY_TO_CODE`;
- `IN_PROGRESS`;
- `RESEARCH_NEEDED`;
- `AWAITING_HUMAN_REVIEW`;
- `REWORK_REQUIRED`;
- `AWAITING_CANONICAL_UPDATE`.

`RESEARCH_NEEDED` is a first-class uncertainty state. It means the currently
stored evidence does not justify one or more numeric anchors. It must not be
collapsed into a zero score.

For the current 100-company snapshot this produces:

- 12 eligibility-gate work items;
- 440 numeric-coding packages;
- 452 work items in total;
- 5 P04 packages awaiting human review;
- 5 P19 packages requiring additional field-level research;
- 430 packages still ready for first-pass coding.

### 8. Research Queue

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
`IN_PROGRESS`, `RECHECK_DUE`, `AWAITING_REVIEW`,
`AWAITING_CANONICAL_UPDATE`, `BLOCKED` or `RESOLVED`.

SME and group eligibility is treated as an upstream gate. If `group_check`
is unresolved, the queue creates a high-priority `RQ00_SME_ELIGIBILITY_GATE`
task before downstream deployment research. A research result may propose
`CONFIRMED_SME` or `EXCLUDE`, but a provisional result is shown as
`AWAITING_REVIEW`. Only an explicitly approved result progresses to
`AWAITING_CANONICAL_UPDATE`.

The results log cannot mutate company intelligence. Positive deployment
evidence or an SME-eligibility decision must first be reviewed and coded in the
canonical company fact layer; the Opportunity Engine and Research Queue are
then rerun. Partial evidence and unsuccessful public searches remain visible
without being converted to negative deployment claims or sample decisions.

The intended eligibility feedback loop is:

```text
Research Queue
    -> research result
    -> AWAITING_REVIEW
    -> approved decision
    -> AWAITING_CANONICAL_UPDATE
    -> canonical company/sample update
    -> rerun engines and queue
```

This separation prevents the research automation from silently validating its
own assumptions.

### 9. Product Interface

The first user-facing prototype is a dependency-free static web application in
`web/`. It is intentionally read-only and consumes a generated public-data
snapshot rather than mutating canonical research files.

Current views:

- **Overview** — pilot size, opportunity mix, research backlog and eligibility
  gates;
- **Company Explorer** — searchable and filterable company intelligence with
  process mappings, confidence, opportunity signals and evidence links;
- **Research Queue** — ranked missing facts with priority, decision impact and
  lifecycle state.

Company detail panels keep technical relevance, commercial deployment status,
sample eligibility and evidence confidence visible as separate dimensions.

The browser payload is produced by `src/export_web_data.py` and written to
`web/data/sme_etoi.json`. The integrated pipeline refreshes this snapshot after
derived outputs pass QA.

### 10. Integrated Execution Pipeline

`src/run_pipeline.py` is the canonical orchestration entry point for the
current prototype. It turns the individual analytical components into one
deterministic workflow:

```text
canonical data + evidence
        |
        v
preflight sample QA
        |
        v
Opportunity Engine
        |
        v
Research Queue
        |
        v
Score Readiness
        |
        v
Scoring Work Queue
        |
        v
cross-output integrity checks
        |
        +----> STOP on invariant failure
        |
        v
write derived outputs
        |
        v
inter-rater reliability outputs
```

The pipeline builds opportunity and research-queue outputs in memory before
writing them. Cross-output checks require complete opportunity coverage,
correct SME-eligibility gates, eligibility-first research ranking, blocked
actionability for unresolved SME cases and preservation of uncertainty
(`UNKNOWN` may never become commercial white space).

A `--check-only` mode executes the same preflight and derived-output checks
without modifying generated files. This is intended for CI and reproducibility
checks.

### 11. Monitoring & Change Detection

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

- run deterministic cross-file QA at every balanced expansion stage;
- expand the provisional sample from 20 to 100 companies, 25 per stratum;
- independently human-review and double-code all 100 records before the v1.0 freeze;
- calculate field-level agreement and Cohen's kappa, then adjudicate every disagreement;
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

- complete and freeze the reviewed 100-company v1.0 dataset;
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
