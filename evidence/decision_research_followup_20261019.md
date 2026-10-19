# Plastics process follow-up — 19 October 2026

All **23 frozen open fields** at FM-Plast (P23, nine), H&K Müller (P24,
six) and Gindele (P33, eight) were revisited. **One new field proposal is
supported; 22 remain UNKNOWN.** All 670 previously CHECKED rows are unchanged.
Current coverage: **671/1,500 checked, 829 open, zero approved**.

## Supported change

Gindele's owner description and its named automation supplier attribute ultrasonic
joining to its actual secretion-bag production. Independent manufacturer
technology documentation explains electrical excitation and local joining heat.
This supports `process_electrification_score = 7`, confidence B: one existing
firm-specific electric process. The technology explanation does not identify
SONOTRONIC as Gindele's supplier or establish installed voltage, frequency or kW.
No new load, displaced fossil fuel, bulk operating temperature, safe interruption
window or recent energy investment is inferred. Supplier page metadata from
2025 is not an equipment commissioning date. Continuous assembly and avoiding
intermediate buffers are not permission to shift demand.

## Retained boundaries

FM-Plast's ARBURG customer report is explicitly issue 51/2013. Printed pages
22–23 were read and page 23 was rendered and visually inspected because text
extraction is partly corrupted. The report establishes historical automated
production and a then-planned host computer. It does not establish that plan's
completion, current equipment or investment within the frozen 2021-10-07 to
2026-10-07 lookback. Undated machine-age percentages on the own ECS page cannot
be anchored to the current retrieval date. Closed cooling and room heat recovery
do not establish a dispatchable thermal store. Nine fields remain open.

H&K Müller's own page retains gas pre-flaming with reduced consumption. It does
not quantify the remaining thermal duty or identify an electric replacement.
The announced additional 1.2 MWp PV and total 1.6 MWp remain planned with a
Q4/2025 commissioning target. Passing that date does not prove completion;
existing 420 kWp is a separate baseline. Generic moulding descriptions do not
identify actual installed heaters or temperatures. Six fields remain open.

The direct Gindele-hosted historical article returns HTTP 404, despite indexed
PDF text being discoverable. This failed retrieval is retained, with owner and
named supplier pages as partial alternative process evidence. The missing
article's exact dated content is not claimed recovered.

## Evidence and validation

- [Frozen predecessors](../data/history/decision_profiles_before_followup_20261019.json)
  and [all 23 field attempts](field_research_followup_20261019.csv).
- [11 scoped content checks](decision_source_checks_20261019.csv),
  [12 direct retrievals](research_source_attempts_followup_20261019.csv),
  and [nine executed discovery queries](research_queries_followup_20261019.csv).
  Eleven bodies retrieved successfully, one failed. Raw third-party bodies remain
  temporary inspection material outside Git.
- Four new registered sources: **677 assessed, 614 RECHECKED, 53 CONTEXT_ONLY,
  10 UNAVAILABLE, zero unclassified**. The newly failed unregistered discovery
  link is in the retrieval/recovery trail, separate from registered-source counts.
- Historical repeated field work: **956 attempts, 75 closures, 881 unresolved
  at their attempt date**. This is distinct from 829 current open fields.
- Canonical company, process, certificate, deployment, numeric scores and
  independent review inputs are unchanged. All twelve SME gates remain open.
  Source/anchor status “Geprüft” is separate from personal or final approval.

Validation: full Python suite, pipeline write and check-only, JavaScript syntax,
complete source rendering and all-company navigation. The repository web snapshot
includes the new profiles, scoped checks, field history and failed retrieval.
Online publication is verified separately after green CI and merge.
