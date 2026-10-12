# Registered-source content coverage — 12 October 2026

All 578 sources in the registered inventory now have a documented source-content
classification. This closes the missing-record pass over the existing inventory;
it does not establish that every original statement is correct, current or
usable for score coding.

| Content classification | Before this pass | After this pass |
| --- | ---: | ---: |
| Relevant body/section rechecked within the stated scope | 340 | 513 |
| Context only; original claim not confirmed for the sampled entity | 2 | 53 |
| Original body unavailable | 5 | 12 |
| No content record | 231 | 0 |
| Total registered sources, including excluded candidates | 578 | 578 |

The independent URL audit covers 831 URLs, of which 778 are retrievable.
Its denominator also includes redirect targets and research-attempt URLs.
URL availability is distinct from the 578 registered-source content decisions.

## Method and inspectable evidence

The [frozen selection](../data/source_content_review_selection_20261012.csv)
contains exactly the 231 source IDs without a content record at main commit
`efa7e85a210ccc49459f166a657c2d756375162f`. Sources previously checked in the
proposal and decision ledgers retain their dated decisions.

The [new ledger](source_content_checks_20261012.csv) records original URL,
company/source identity, UTC retrieval timestamp, final target, HTTP result,
content kind, full retrieved-body SHA-256, inspected location, finding and scope.
HTML was extracted for relevant-section inspection; PDF text was extracted,
and image-only certificate/report passages were visually inspected. Failed
network requests were retried. Third-party downloaded bodies remain temporary
inspection material, rather than redistributed repository artifacts.

RECHECKED means the relevant body or section supports the narrowly documented
finding. An imprint may support legal identification without supporting employee
count, ownership aggregation or any technical asset. This pass does not claim a
line-by-line audit of every page or linked document within every website.

CONTEXT_ONLY records generic portals, group/foreign-entity material, report
indexes, historical brand accounts and extracts that fail to reproduce the
registered company-specific claim. These are assessed boundaries, not confirmed
claims. UNAVAILABLE records inaccessible originals and preserves the limitation
even when a separately registered alternative supports a narrower statement.

The dashboard shows the new inspected finding alongside its scope; the original
register wording remains preserved separately in the export. This prevents a
retrievable generic portal from displaying its legacy company-specific statement
as though that statement had just been verified. The sources view exposes all
65 context/access boundaries as well as the separate retrieval/recovery table.

## Decisions and remaining work

Report indexes do not verify report contents. Group certificates do not become
German-entity certificates. Customer applications do not identify an owner's
energy equipment. Publication dates, upload paths, planned investments and first
registration dates do not replace commissioning dates or current validity.
Historical certificates remain historical even when their URLs are accessible.
Conflicting identity and group eligibility remain upstream gates.

All canonical score inputs, coding proposals, field-check decisions and personal
approval remain unchanged: **623 CHECKED proposals, 877 blank NEEDS_RESEARCH
fields, zero approved fields and 12 open SME gates**. The complete source pass
has documented the current public evidence and its limits. Closing the remaining
field questions requires targeted additional evidence, and some questions may
remain UNKNOWN after reasonable public research. Discovery of new sources can
extend the inventory and reopen its content coverage.

## Validation

The pipeline validates the frozen selection, source/URL ownership, UTC timestamps,
body fingerprints, content classifications and required context/access boundaries.
Regression tests reject dropped records, foreign entities/URLs, missing hashes,
invented human approval and unavailable bodies claimed as retrievable.

247 Python tests, the deterministic pipeline, JavaScript syntax checks and the
actual dashboard/detail renderer tests pass. Renderer tests cover the complete
578-source totals, all 65 boundary rows, aligned columns and escaped findings.
Canonical and numerical-coding files have no changes in this pass.
