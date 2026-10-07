# Public-source retrieval audit — 2026-10-06

## Scope and result

Starting `main`: `0f8ac45deac222c07f8f1166531844629f02e56b` (PR #37).
All 100 sample companies were checked, including companies with coding
assessments and companies not yet coded. The audit also includes the public
sources of nine excluded candidates. No next coding batch or new proposals were
created during this work.

The initial inventory contained 297 distinct URLs across all 271 source-register
records, company websites, certificate links, process mappings, review-source
manifests, research-result citations and company dossiers. The final checked
inventory contains **318 URLs**, including accepted replacement/context links,
the previously mentioned Zötler PDF, and current redirect targets. Eleven new
source records bring the register to **282 entries**.

| Retrieval outcome | URLs |
| --- | ---: |
| HTTP_OK | 290 |
| REDIRECT_OK | 14 |
| NOT_FOUND (404/410) | 8 |
| ACCESS_BLOCKED (403) | 2 |
| HTTP_ERROR (502 after retry) | 4 |
| Total | 318 |

**304 URLs were retrievable.** Fourteen were not retrievable in this check;
two of those are trailing-slash variants of already investigated removed
imprint paths. The first pass had eleven problematic URLs; the explicit Zötler
PDF and two final-path variants account for the increase. Failed requests remain
in the audit and old source records remain in the register.

This is an AI retrieval and source-recovery check, **not Anna's Human Review**.
An HTTP success establishes only retrieval of response bytes. It does not
validate every historical claim, exact company attribution, current operation,
certificate validity, deployment, or SME eligibility. Search-index snippets
were used to locate candidates, not treated as live retrieved documents.
All canonical deployment facts, score inputs, numeric proposals, certificate
records and human-review records are unchanged. UNKNOWN stays UNKNOWN.

## Retrieval method and reproducibility

`src/audit_source_links.py` deduplicates public URLs while preserving company,
source-ID and repository-reference provenance. Synthetic demo URLs are excluded.
It performs GET rather than HEAD, follows redirects, stores HTTP status, final
URL, UTC time, content type, title, attempt count and a SHA-256 digest of the
sampled response (up to 512 KiB). This is not a full-document archival hash.
Timeouts, selected server failures and throttling receive one retry. Obvious
soft-404 titles, access challenges, parked-page titles and PDF-to-HTML responses
do not pass merely because their status is 200. Detection is heuristic, not an
exhaustive authenticity or content-quality assessment.

Full response samples were used temporarily for inspection; downloaded page
bodies and PDFs are not committed. Recovery searches checked current company
navigation, exact-company public directories, official fair profiles and
issuer-labelled company releases. Rejected alternative URLs and their retrieval
results remain in `evidence/source_recovery_attempts.csv`.

```bash
python src/audit_source_links.py --workers 12 --timeout 15 --sync-register
# Inspect failures and update scoped recovery records before completing QA.
python src/run_pipeline.py
python src/run_pipeline.py --check-only
python -m unittest discover -s tests
node --check web/app.js
node tests/test_web_priority.cjs
```

Network checks are explicit work; CI and the pipeline never contact company
websites. The offline pipeline rejects missing URL coverage, uninvestigated
retrieval failures, foreign recovery source IDs, an AI recovery claiming human
review, and failed source retrievals still marked VERIFIED. A newly added source
must receive a retrieval check before pipeline preflight can pass.

`--sync-register` updates retrieval metadata only. It preserves content-scope
blockers even through later retrieval failures and successes. An accessible
expired certificate remains marked expired; certificate validity is not updated
by this command. Process references were re-anchored only to supported process
descriptions, with historical and attribution limitations in their notes.
Confidence grades and scoring fields were not upgraded.

The 100-row `outputs/source_audit_by_company.csv` distinguishes companies with
coding assessments from uncoded companies, reports retrieval issues, and counts
open recovery-scope gaps. The web's **Quellenprüfung** view shows the same
coverage and recovery records. Individual source panels distinguish retrieval
status from evidence status and check date.

## Recovery decisions and exact boundaries

Fourteen recovery investigations have these outcomes: eight REPLACEMENT_FOUND,
three PARTIAL_REPLACEMENT, one HISTORICAL_REPLACEMENT, one
REDIRECT_SCOPE_UNRESOLVED and one NO_EQUIVALENT_FOUND. General financial,
operational or certification questions remain separate from recovery of a
specific source claim.

| Company | Replacement/context | Decision and remaining scope |
| --- | --- | --- |
| P26 Barth Galvanik | S-P26-03, current official SurfaceTechnology profile | Same March 2024 staff/revenue bands recovered; no new independent eligibility approval. |
| P49 SAXONIA (excluded candidate) | S-P49-03, company training site | 300 employees recovered; plastic coating supported, metal-coating claim only partially recovered. |
| P52 Glauner / Alpirsbacher | S-P52-03, company raw-material/process page | Brewing and ingredients supported; old across-process resource-use claim remains open. |
| P60 HARTCHROM Beck | S-P60-03, company homepage with explicit service description | Industrial hard-chromium scope recovered; no energy-deployment claim. |
| P78 Erlemann & Huckenbeck | S-P78-03, 2023 issuer-labelled company release | Historical entity/address and pressing/injection processes recovered; current legal/site continuity remains open. |
| P93 Brauerei Schimpfle | S-P93-03, current company imprint | Exact entity, Gessertshausen address and register recovered. |
| P95 Winkler-Bräu | S-P95-03, named Key to Bavaria record | Brewery entity/address recovered; hotel imprint was rejected as an equivalent brewery identity proof. |
| P107 Dibbern Porzellanmanufaktur | S-P107-03, exact-company Key to Bavaria record; S-P107-04, brand context | Candidate identity and hand forming recovered; separate DIBBERN GmbH brand furnace/glaze claims are not assigned to the candidate. |
| P110 Neue Porzellanfabrik Triptis | S-P110-03, company production FAQ | Triptis hard porcelain, glazing/firing and decoration supported; no electric-heat route inferred. |
| P76 Si-Tech Singer | S-P76-03, current company imprint | Original imprint redirects to homepage; correct named imprint recovered. |
| P17 QSIL (excluded candidate) | S-P17-02, existing 2020 acquisition release | Group redirect is retrievable but does not establish current candidate attribution. |
| P30 Zötler | S-P30-03, existing company sustainability page | Old PDF returns 404; page says declaration is being revised. Direct current statement and EMAS validity remain open. |

The six non-equivalent or limited cases remain explicit research gaps. No
unretrievable evidence is rewritten as evidence of non-deployment, absence of
certification or commercial white space. The full request/source-ID relationships,
search scope, supported facts and missing facts are in
`evidence/source_recovery.csv`.

## Frozen decisions and live queues

Link health and source recovery alter documentary counts and company ordering.
They do not rewrite the frozen NBCC batch manifests. Reconstruction tests now
use pinned source-register and process-map fixtures from the PR #37 baseline;
later retrieval failures cannot falsify a historical selection decision.

The current work queue remains **12 OPEN_GATE, 360 READY_TO_CODE,
57 RESEARCH_NEEDED and 23 AWAITING_HUMAN_REVIEW**. No proposals were approved,
no missing field was filled and no total score was published. P43 remains the
live next coding company, but coding stayed paused during this audit.


## Subsequent coding follow-up

The counts above describe the PR #38 audit snapshot. Batch NBCC-2026-10-06-03
subsequently adds company-specific evidence and retrieval checks. P43's generic
VDI homepage was available but failed the content attribution check; it remains
visible with CONTENT_REVIEW_REQUIRED beside its located company-specific profile.
This illustrates the stated distinction between retrieval and claim validation.
The live audit CSV/web view includes later checks; frozen audit counts do not
claim that every historical factual assertion has passed human review.


On 2026-10-07, NBCC-2026-10-07-01 rechecked ten URLs for P25/P15, including
three new URLs, all with HTTP 200. The live inventory now contains 333 URLs.
The current Scheplast certificate replaces the expired document for current
validity only; the expired PDF remains retained. The old homepage extraction
of staffing/recycling/annual generation failed current content reproduction,
so its source is blocked with CONTENT_REVIEW_REQUIRED and a partial-recovery
record. This content limitation is retained despite successful HTTP retrieval.
The historical counts above remain the original full-audit snapshot.


On 2026-10-07, NBCC-2026-10-07-02 rechecked 29 URLs for P26/P28/P29/P33,
including 19 new URLs: 28 retrievable, one historical fair-link 404 with an
existing verified replacement. The complete live inventory now has 352 URLs;
all 100 sample companies remain covered. Current exact-holder certificates
and signed EMAS validation were inspected separately from HTTP retrieval.
Gindele's generic municipality URL remains retrievable but cannot reproduce
its attributed company profile: CONTENT_REVIEW_REQUIRED retains that history,
and a named municipal profile provides a scoped replacement. Neither this
AI source correction nor successful GET constitutes Anna's human review.
The original full-audit counts above remain historical snapshots.


## Continuous batch follow-up — 2026-10-07 (03)

Batch NBCC-2026-10-07-03 adds twelve complete 15-field first passes: 67 numeric
proposals awaiting independent human review and 113 blank UNKNOWN research
fields. Current assessment coverage36/100, 540 fields: 250 pending numeric and
290 research gaps. Human approval/canonical score coverage remains unchanged.
Live queue260 ready/142 research/38 review/12 gate; company queue52 code-now/
33 research-first/3 review/12 eligibility-first. Next P56. Canonical deployment,
staff, confidence and numeric inputs plus human-review records are unchanged.

357 sources/387 audited URLs, 373 retrievable; all100 companies covered. The
65-URL follow-up has64 retrieval successes and one old retained404 with partial
recovery. HTTP success does not clear five generic/staging content blockers.
MACK's actual thermoforming replaces unsupported injection mapping. The new
provisional archetype does not invent storage/scheduling; zero matched
opportunity rules is valid while source/readiness/coding coverage remains
complete. Current outputs202 opportunities/197 research tasks. Six certification
facts and one historical claim are corrected by actual holder/date/body/register,
with no automatic score approval. Certificate expiry, reporting dates, expired
goals and planned measures remain separate.
See [full batch boundaries](next_best_company.md#frozen-batch-nbcc-2026-10-07-03).


## Continuous batch follow-up — 2026-10-07 (04)

NBCC-2026-10-07-04 adds twelve full15-field first passes:55 numeric proposals
pending independent human review,125 blank UNKNOWN research fields. Current
coverage48/100,720 rows:305 numeric pending,415 research. No new canonical
score or human approval; no prior proposal/score/deployment/staff/confidence/
review mutation. Live queue200 ready/197 research/43 review/12 gate; company
queue40 code-now/45 research-first/3 review/12 eligibility-first. Next P77.

All100 firms source-audited;394 sources/424 URLs,409 retrievable. Follow-up67
URLs:66 retrievable plus ceram404 with claim-only partial recovery. Actual
Dorn/Si-Tech cert bodies/annex support current ISO14001; ceram's current claim
is not verified current validity. Partner machines/theoretical SPC/stock photos
and customer energy assets stay outside own-plant inference. Electrical
storage not thermal storage; biogas not Bio-LPG; test/recovery temperatures not
production temperatures; old/planned/capacity projects not recent energy CAPEX.
See [full batch boundaries](next_best_company.md#frozen-batch-nbcc-2026-10-07-04).


## Continuous batch follow-up — 2026-10-07 (05)

Batch `NBCC-2026-10-07-05` completes 15-field first passes for P77, P79,
P80, P81, P83, P84, P87, P90, P91, P92, P93 and P94: 70 numeric proposals
await independent human review; 110 fields remain blank `NEEDS_RESEARCH`
with `UNKNOWN` confidence and an exact missing fact. Current coverage is
**60/100 companies and 900/1,500 fields**: 375 numeric proposals pending
review and 525 research gaps. This is assessment coverage, not resolved or
human-reviewed coverage. No new canonical score or automatic approval.

Six certificate facts are corrected using actual document holders, validity
and issuer: Metak ISO 50001/14001, Langer ISO 50001/14001, MKT ISO 14001 and
Riegele EMAS. Riegele's signed 2025 statement and current official register
are distinct from reporting years, registration-since dates and expiry.

German Ceramany manufacturing attribution is unresolved; foreign ISO 9001
holders and cross-site staff cannot establish German owned assets. All its
15 fields remain researched gaps. InnoKeramik operates plate finishing;
KITO's firing and machinery sold to partners are not owned kiln equipment.
Both mappings use explicit provisional archetypes without supported
opportunity-rule matches; source, readiness and coding coverage remain.

Planned Langer PV/storage cannot be considered commissioned because September
2026 has passed. Actual 2024 efficient-machine, extraction-converter and
cooling work is dated separately. MKT's purchased hydro is not owned generation
or renewable process heat. ELB's coating resistance is not bath temperature.
A GRW capacity grant is not completed energy CAPEX. Riegele's inconsistent
boiler unit is retained, not silently changed from MWh to MW. Future controls,
CIP and logistics PV remain planned until completion is established.
Ketterer's explicit owner statement of exclusively woodchip operating heat
supports a bounded thermal-fuel anchor, not whole-company fossil-free status;
2021/2023 nitrogen dates conflict and are not averaged. Schimpfle's completed
PV and transformer projects retain separate dates. Kuchlbauer's room heat
pump and electrical battery are not brewery process heat or thermal storage;
its 2024 integrated logistics project counts once for investment coding.

Current work queue: 140 `READY_TO_CODE`, 248 `RESEARCH_NEEDED`,
52 `AWAITING_HUMAN_REVIEW`, 12 `OPEN_GATE`. Company actions: 28 `CODE_NOW`,
57 `RESEARCH_FIRST`, three `REVIEW_PROPOSALS`, 12 `ELIGIBILITY_FIRST`.
Next ranked company: **P95 Winkler-Bräu**. Outputs contain 200 opportunities
and 195 research tasks. The source inventory has 430 registered sources,
460 audited URLs and 445 retrievable URLs, covering all 100 sample firms.
The 65-URL batch follow-up confirms 63 retrievable URLs and two retained
404s; replacement/scope notes remain separate from successful retrieval.
Prior proposals, canonical numeric/deployment/staff/confidence fields and
independent human-review records remain unchanged.
