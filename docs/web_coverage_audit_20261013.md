# Web coverage audit — 2026-10-13

This audit compares the current repository data with the private hosted interface
at https://sme-etoi.fairorbit8.chatgpt.site. It checks display coverage, not new
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
