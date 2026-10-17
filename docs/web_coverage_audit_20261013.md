# Web coverage audit — 2026-10-13

This audit compares the current repository data with the private hosted interface
at https://sme-etoi.fairorbit8.chatgpt.site. The table below records the 13October2026 baseline; dated follow-ups describe later changes. It checks display coverage, not new
scientific evidence or independent human approval. The deployed snapshot is
updated from the tested, merged repository web export.

| Repository area | Current coverage | Web location |
| --- | --- | --- |
| Current company sample | 100 companies | Target companies, filters, details, CSV |
| Technical priority | 17 A, 62 B, 0 C, 9 UNKNOWN, 12 BLOCKED | Chart, company list, details, regional and sector tables, CSV |
| Score proposals | 1,500 fields: 652 CHECKED, 848 NEEDS_RESEARCH | Analysis overview and company analysis; missing facts and clickable evidence IDs |
| Field check history | 657 proposal checks plus 4 reassessments = 661 records | Expandable history beside each proposal, with before/after values, dates and evidence |
| Source register | All 617: 591 in the current sample and 26 outside | Sources, complete register with membership labels and scoped findings |
| Source content classification | 552 RECHECKED, 53 CONTEXT_ONLY, 12 UNAVAILABLE | Sources overview and register; retrieval and content review remain separate |
| Source recovery | 80 dated cases | Sources overview plus affected company source details |
| Certificate register | All 321: 300 in sample and 21 outside | Sources, full certificate register; company certificate details |
| Public research results | All 96, including 15 YES observations | Research history and company research details; scope and dates preserved |
| Generated research queue | 192 tasks; only 6 EVIDENCE_FOUND tasks match the generated queue | Research task table; recorded findings are shown separately |
| Decision profiles | 84 profiles: 70 technical, 12 eligibility, 2 identity | Sources/research summaries and company details |
| Opportunities | 198 rows | Opportunities, company details and technology aggregates; rule and next action included |
| Score work | 452 tasks: 440 numerical and 12 eligibility gates | Analysis and company scoring work queue |
| Company QA | 100 dated protocols | Quality assurance; company QA summary in analysis details |
| Independent double coding | 100 status records, no completed independent reviews | Quality assurance status totals |
| Inter-rater reliability | 16 rows; zero completed pairs; agreement UNKNOWN; field-level kappa UNKNOWN, overall kappa not applicable | Quality assurance; empty conflicts never imply agreement |
| Process library | 13 generic profiles | Methodology; all reference temperature ranges, relevance and review status |
| Technology library | 8 generic profiles | Technologies; constraints, economic inputs, signals and reference status |
| Opportunity rules | 9 rules | Methodology; required signals, blockers, confidence caps and output levels |
| Scoring methodology | 5 dimensions, 15 fields, maximum 100 points | Methodology with per-field and dimension maxima |
| Public signals and deployment flags | Existing company facts, targets, investments and process evidence | Company overview, dated independently of later research |
| Project documentation | 9 project links | Documentation including access instructions and this coverage audit |

## Boundaries and deliberate exclusions

Technical A/B/C prioritization is not source confidence A/B/C and is not a final
ETOI score. Checked proposals do not change canonical company scores or constitute
independent human approval. The 12 unresolved eligibility gates remain blocked;
no company has final-score approval. The 848 unknown proposal fields remain open.

The 96 historical findings are not identical to the current generated queue.
Dates and observation scope are preserved rather than converting every YES into
an implemented-technology flag. Company facts retain their own last-verified date;
later field checks and source reviews have separate timestamps. Retrieval success
does not prove company identity, certificate validity or a source's original claim.

The investment window remains 2021-10-07 through 2026-10-07. Generic process
ranges and technology fit rules do not establish company operating temperatures,
installed equipment, savings or economic feasibility.

Historical CSV snapshots, research batches, developer tests and synthetic scoring
demos remain repository audit/development artifacts. They are not added as extra
current companies or observations. The project documentation links provide the
repository entry point; underlying histories used for current field decisions
are exposed directly in the web interface. Personal notes and pinned/recent lists
are stored in the user's browser and are not shared repository facts.

## Validation

The export is compared against complete CSV register keys and original finding
and check rows. Renderer tests exercise all navigation areas, register row counts,
company histories, missing-fact display and unsafe-link/HTML escaping. The Python
suite, JavaScript suite and pipeline consistency check must pass before merging
and updating the existing private Site. This environment does not provide browser
visual QA; rendering checks here validate generated HTML and data coverage.

## Navigation follow-up — 2026-10-16

Cross-area company links now open the requested company and its actual table
page. Incompatible previous company filters are cleared, while compatible
filters stay active; the controls, counters and page heading follow the visible
view. Company IDs can be searched directly. Paging updates the selected row and
detail together, and closing the detail leaves it closed until another selection.

The personal company tab now contains only locally pinned companies and is
labelled accordingly. Removing a pin updates that subset and its counts
immediately, including its empty state. Pins and notes remain browser-local.

Both research tasks and historical findings open the corresponding company's
research detail. Research search covers IDs, missing facts, source IDs and status
as well as names and questions; no-match states are explicit. Evidence links
retain their own navigation. Table-only mode persists across company links;
opening the dashboard or the chart command deliberately enables charts. The
sidebar toggle and the reset/search commands keep navigation chrome consistent.

A separate JavaScript navigation suite exercises the actual handlers against the
100-company export and runs in CI alongside the existing rendering suite. These
changes do not alter source facts, proposals, scores or canonical company data.
Visual browser QA remains unavailable in this managed environment.

## Signal and next-action follow-up — 2026-10-16

Company technical signals are qualitative HIGH/MEDIUM/LOW categories, with missing
or research-required technical levels explicitly open. Fixed 92/68/42/25-percent
bar lengths have been removed: they were display constants, not derived scores.
Commercial priority is never used as a fallback technical level. Signal confidence
and commercial status are displayed alongside each category; missing confidence
has neutral styling rather than the styling of confidence C. All company signals
are retained in both overview and analysis, without a six-row truncation.

The company list and overview now use the same next-action selection. Eligibility
and certificate gates, entity-attribution conflicts, open generated research,
unresolved field evidence and separate proposal approval are considered in that
order. A company with no generated opportunity can still have missing field
facts; it no longer appears to have no work solely because its opportunity queue
is empty. All 100 current companies retain a next step, and the detail action opens
the matching analysis, research or source tab. This display selection does not
write proposal statuses, canonical scores or human-review decisions. A genuine
final-score-ready state is not reopened just because it retains checked history.

Renderer and actual-handler tests cover commercial-versus-technical fallbacks,
missing confidence, HTML escaping, the 12 open eligibility gates, identity cases,
companies without opportunities, the next-action link and unchanged input data.
The remaining view-help button opens documentation. The browser-back control is
explicitly labelled as browser navigation.


## Research follow-up — 2026-10-17

The next frozen decision block covers ten further firms and all75 of their
previously open fields. None supports a new numeric anchor; the global652
CHECKED /848 UNKNOWN proposals remain unchanged. There are now94 profiles
(80 technical,12 eligibility,2 identity), with696 historical field attempts.

The full register contains624 records:560 scoped rechecks,52 context-only and12
unavailable. The change from53 to52 context records is the recovered exact
Heilbronn operator/imprint scope for S-P85-01; it is not an upgrade of energy
certification or of a score. The separate URL audit has897 rows,823 retrievable.
Failed fresh retrievals preserve the date and scope of earlier content records.

The new Winkler website-operator conflict is displayed separately from the
canonical brewery entity and now takes precedence in its next review action.
See the [complete research record](../evidence/decision_research_20261017.md).

## 17 October follow-up update

The current web export contains all100 dedicated company profiles,632 sources,
321 certificate records,100 public-research observations and100 QA protocols.
Five follow-ups are shown separately from the nine initial decision blocks and
756 historical field attempts. The recovered Winkler imprint supersedes the
footer-based operator conflict without transferring hotel energy assets to the
brewery. The latest gate-specific next action uses the attributed profile finding.
652 checked field proposals,848 unknowns,12 SME gates and zero final-score-ready
companies remain. See the [follow-up report](../evidence/decision_research_followup_20261017c.md).

## Further 17 October field follow-up

The current export contains642 assessed sources,321 certificate records,105
research observations(16 YES) and100 unique company profiles. Eleven follow-ups
are separate from original profile coverage. The latest six-company follow-up
has22 attributed field attempts, two new checked proposals and20 remaining gaps.
Total field history778 attempts/57 closures; current654 checked/846 unknown.
Hochdorfer's implemented2023 PV is separated from planned2026/2027 projects,
expired compensation labels and the cooperative-owned2020 array. OFTECH/OT
ownership gaps remain separate from primary legal/site facts. See the
[latest follow-up report](../evidence/decision_research_followup_20261017d.md).


## 17 October 2026 — source-led follow-up

The new ten-company block retains 100 unique profiles and exposes 85 repeat field
attempts, ten new checks and 75 retained unknowns. All 654 earlier checked rows
remain unchanged. Current totals: 664 checked / 836 unknown / 0 approved; 655
classified sources (592 scoped rechecked, 53 context-only, ten unavailable).
Five new management anchors describe bounded public-documentation gaps; one
other describes a named partial audit. Neither claims current ISO certification
or internal system absence. Historical attempts are 863 / 67 closures; 21
follow-up records remain separate from unique-company coverage. The new report
and all source/field provenance are linked in the web export.
