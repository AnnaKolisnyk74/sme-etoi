# Technical research priority in the web interface

The chart/table priority is explicitly technical. It identifies which companies
have strong public technical signals worth investigating next. The engine's
commercial status and priority, deployment UNKNOWNs, score proposals, confidence
grades and final-score approval remain separate and unchanged.

Previously the UI selected `opportunity.priority` before `opportunity_level`.
Most opportunities had commercial priority RESEARCH. The UI then defaulted
that unrecognised value to C/Low, giving a misleading100-of100 Low chart.

## Display rule

1. Companies with unresolved/excluded SME eligibility are shown as `BLOCKED`
   (KMU-Prüfung offen); they receive no A/B/C research grade.
2. Consider explicit technical `opportunity_level` values with evidence
   confidence A or B. Confidence C and missing confidence do not qualify.
3. The strongest supported HIGH/MEDIUM/LOW level maps to A/B/C respectively.
4. If no supported level exists, show `UNKNOWN` (Belege offen). Missing,
   research-required or unmapped facts never default to Low/C.

The same rule is used in the chart, company list/detail, high-priority filter,
potential sorting and region/sector aggregates. CSV uses `technical_priority`
and retains UNKNOWN/BLOCKED as distinct machine-readable states.

On the current100-company dataset: **17A,62B,0C,9open,12SME-gated**.
These counts come from existing engine signals; no source fact, confidence,
score value or deployment claim was upgraded to obtain them. The652 checked
proposals and848 open field questions remain unchanged. An A company can still
have unresolved heat-carrier, storage or recent-project questions.

Validation exercises the original RESEARCH-versus-HIGH bug, confidence-C
rejection, genuine LOW, missing/unmapped levels, SME gates, mixed signals,
filtering, empty charts, CSV semantics and unchanged input data.
