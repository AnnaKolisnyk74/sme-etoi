# Final six-company field-work continuation — 17 October 2026

All **100 current-sample companies now have a dedicated decision profile**:
86 technical,12 eligibility and two dedicated identity profiles across nine dated
blocks. This completes profile coverage, not all factual research or approval.
The final six have60 frozen open fields. **No new numeric anchor is supported;
all60 stay blank UNKNOWN.** Totals remain652 CHECKED /848 NEEDS_RESEARCH /
0 approved. All earlier checked proposals remain byte-identical.

## Selection and provenance

The generated opportunity-research queue has no remaining unprofiled, non-gated
company. It omits six companies that still have open numeric field work. The
continuation therefore uses the first unique unprofiled company by ascending
**field-work rank**, retaining upstream gates and skipping ready/checked rows:
P24(33),P23(58),P35(218),P87(333),P90(403),P106(418).

The [selection](../data/decision_research_selections_20261017b.csv) explicitly
labels SCORE_WORK_QUEUE. Its legacy research_rank column contains work_rank,
not a fabricated opportunity rank. The web labels it Feldarbeitsrang and shows
selection1–6 of6. The validator rejects this fallback while any company remains
in the ordinary opportunity selection and rejects hidden rank provenance.
Both [opportunity](../data/history/research_queue_before_deep_20261017b.csv) and
[field-work](../data/history/score_work_queue_before_deep_20261017b.csv) queues,
[proposals](../data/history/score_coding_proposals_before_deep_20261017b.csv) and
[checks](../data/history/score_proposal_checks_before_deep_20261017b.csv) are frozen.

## Findings and remaining requirements

| Company | Open fields attempted | Finding and remaining requirement |
| --- | ---: | --- |
| P24 H&K Müller | 6 | Own PV, electric drives and recovered heat for rooms remain separate from process heating. Own text still describes reduced gas consumption in flame pretreatment. Generic screw friction/external heating does not identify actual heaters or setpoints. Obtain the site's thermal carrier/duty, substitution route, useful storage and operating freedom. |
| P23 FM-Plast | 9 | Own electric/hybrid machines, hot runners, closed tool-water cooling and hall heat recovery are documented. Undated machine-age shares, short cycles and colour changes do not establish coordinated energy control, commissioning in the fixed window or a thermal replacement route. Obtain actual thermal equipment, control coordination, storage and dated projects. |
| P35 Mack | 6 | Six thermoforming machines, CNC and2023 PV expansion remain supported. Sheet dimensions and material ratings are not plant setpoints;3000m² is not installed kWp. Identify heaters/fuels, temperatures, storage and authorised operating windows. |
| P87 Ceramany | 15 | German imprint and Chinese/German contact locations are separate. Group brochure forming/sintering/CNC claims do not allocate each asset to the German entity. Visually read ISO9001 body names Yixing Ceramany and Yixing Doprecision, cycle27May2026–26May2029 despite the older URL filename. Resolve exact legal holder/site attribution before scoring owned German assets; quality certification is not EnMS. |
| P90 InnoKeramik | 13 | Own finishing of purchased KLAX slabs is distinct from KITO/KLAX firing above1200°C,15000t pressing and energy recovery. Machinery sales, leasing and partner digitalisation are not owned Düren kilns, controls or investments. Establish the actual own equipment and energy boundary. |
| P106 Felix Vuckovic | 11 | Own CNC grinding, honing, lapping, polishing, ultrasound and CAD/CAM remain supported. Annual unspecified machine investment and ISO9001 do not identify an energy investment date, process-heating route, EnMS or quantified energy goal. Obtain owned energy duties and dated project/system evidence. |

Ceramany's ENTITY_CONFLICT outcome refers to unresolved attribution between the
German record and foreign manufacturing/certificate holders. The canonical
German name is preserved. Its next-action link opens entity clarification first.
All100 exported profiles retain final_score_approval=NOT_GRANTED.

## Source trail and limits

- [Six profiles](decision_research_profiles_20261017b.json),
  [60 exact-once field attempts](field_research_deep_20261017b.csv),
  [20 scoped body checks](decision_source_checks_20261017b.csv),
  [seven executed discovery queries](research_queries_deep_20261017b.csv) and
  [32 direct retrieval attempts](research_source_attempts_deep_20261017b.csv).
- Direct responses retain time, status, final URL and complete raw-body SHA256.
 31 bodies were retrievable; the discovered H&K certification-index URL returned
 404. The existing direct certificate and sustainability body remain readable;
 a search extract does not erase that404. The recovery ledger now has93 cases.
- Ceramany's image-only certificate and brochure pages3/5 were visually inspected.
 They retain CONTEXT_ONLY status for German-asset attribution. Foreign quality
 holders and group-process scope are not upgraded to German energy certification.
 Full third-party bodies remain temporary inspection material outside the repo.
- Two newly registered primary pages bring the source inventory to **626/626
 assessed:562 scoped RECHECKED,52 CONTEXT_ONLY,12 UNAVAILABLE,0 missing**.
 Separate URL inventory: **900 audited /825 retrievable**. Content provenance
 and retrieval availability remain distinct.
- Fixed investment window:2021-10-07 through2026-10-07. Undated machine age,
 certificate issuance, website copyright and public-search silence establish
 neither commissioning nor non-deployment.

Cumulative dated field attempts total756:55 new-evidence closures and701 still
unknown at their attempt date. These are historical attempts, distinct from the
current848 open fields and the prior103 newly supported fields overall. Twelve
SME gates, final canonical scores and independent review remain open. Public
findings stay96 observations/15 YES; no commercial or internal CRM facts appear.

Validation:263 Python tests, JavaScript syntax, complete source/profile renderers,
field-rank/batch-size display and navigation pass. New regressions enforce
exhausted-queue fallback, gates/prior/duplicates, exact sample coverage,60 frozen
gaps and retained foreign-holder scope. Pipeline write/check and whitespace
checks pass. Canonical company, process, certificate, QA, coding, independent
review and score files, earlier public findings and score-check decisions remain
byte-identical to the preceding main. Browser visual QA is unavailable here.
The tested green-CI merge is published to the existing owner-private Site.
