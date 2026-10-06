# SME-ETOI Score Coding Proposal Protocol

## Purpose

`data/score_coding_proposals.csv` is a review layer between the scoring work
queue and the canonical numeric scoring input.

It exists so that a first coder or an AI-assisted research pass can propose
numeric anchors with evidence while preserving a strict human review gate.

A proposal is **not** a canonical score value.

## Required fields

Every proposal records:

- company and legal entity;
- SME-ETOI dimension;
- exact score field;
- proposed numeric anchor;
- maximum value;
- plain-language anchor interpretation;
- proposal confidence;
- evidence source IDs;
- evidence basis;
- missing fact when additional research is required;
- proposal status;
- coder;
- proposal date;
- reviewer and review date when applicable.

## Allowed lifecycle

```text
Scoring Work Queue
    -> coding assessment
        -> NEEDS_RESEARCH
        -> new evidence -> new coding assessment
        or
        -> AWAITING_HUMAN_REVIEW
        -> APPROVED or REJECTED
        -> separate canonical update
    -> rerun Score Readiness
    -> rerun scoring pipeline
```

An approved proposal still does not mutate canonical scoring data by itself.
The accepted values must be copied into the canonical scoring input in a
separate, reviewable change.

## Human-review rule

`AWAITING_HUMAN_REVIEW` proposals must have blank `reviewer` and
`review_date` fields.

`APPROVED` and `REJECTED` require:

- a real reviewer;
- a review date;
- preferably a short review note.

The automated validator may reject malformed proposals, but it must never mark
a proposal as human-reviewed.

## Evidence rule

Every numeric proposal must cite one or more source IDs from
`evidence/source_register.csv` that belong to the same company.

The proposal should explain why the selected coding-manual anchor fits the
stored evidence.

A source that merely identifies the company is not sufficient evidence for a
technical score field.

## Uncertainty rule

If evidence does not support an anchor, do not manufacture one from generic
sector assumptions.

Use `NEEDS_RESEARCH` when the current repository evidence is insufficient for
a field-level numeric anchor. Such a row must:

- leave `proposed_value` blank;
- use `proposal_confidence=UNKNOWN`;
- identify the exact `missing_fact`;
- cite the existing source IDs that establish the current evidence boundary.

This is intentionally different from a numeric zero. Zero is an allowed coding
anchor only when the stored evidence actually supports the zero anchor.

Where a conservative numeric anchor is proposed from weak but relevant
evidence, the proposal confidence should reflect that limitation and the
evidence basis must state it explicitly.

## P04 first-pass example

The first populated proposal set is P04 — Neumarkter Lammsbräu Gebr.
Ehrnsperger KG.

It contains all 15 SME-ETOI score fields and remains entirely
`AWAITING_HUMAN_REVIEW`.

If all proposed anchors were accepted unchanged, they would sum to 53/100.
This number is a proposal-derived arithmetic result, not a published SME-ETOI
score.

P04 must remain absent from canonical scored output until human review and a
separate canonical update are complete.

## P19 uncertainty example

P19 — Glasfabrik Lamberts GmbH & Co. KG demonstrates the field-level
uncertainty path.

The current repository evidence supports only three numeric first-pass
proposals:

- `measures_gap_score = 7`;
- `management_gap_score = 0`;
- `targets_gap_score = 5`.

The other twelve score fields remain `NEEDS_RESEARCH`. Examples include the
current furnace energy carrier, firm-specific electrification route, operating
pattern, power-quality evidence and onsite-integration evidence.

No total P19 score is calculated from these three fields. The twelve unresolved
fields stay explicitly unresolved.

## P12 mixed-state example

P12 — Richard Henkel GmbH demonstrates that one company can have different
proposal states across dimensions.

Four dimensions are fully covered by numeric proposals and therefore wait for
human review. Load-flexibility remains `RESEARCH_NEEDED` because the current
sources do not establish a thermal buffer, thermal store or sufficiently
documented usable thermal inertia.

Fourteen numeric proposals sum arithmetically to 50. This partial sum is not a
published SME-ETOI score because one required field remains unresolved.

## P16 high-confidence / incomplete-field example

P16 — Sembach GmbH & Co. KG has A-level company/process evidence and direct
current ISO 50001 / ISO 14001 certificates. That does not make all score fields
known.

The repository directly supports four numeric proposals:

- difficult/uncertain temperature fit from documented 1,100–1,750 °C processes;
- scheduling relevance from chamber-furnace / discrete thermal stages;
- mature management-system evidence;
- no dated public target after the defined checks.

Eleven remaining fields stay `NEEDS_RESEARCH`, including the furnace energy
carrier, firm-specific electrification route, motor/converter evidence,
thermal-buffer evidence, power-quality evidence and recent transition
investments.

This case prevents overall evidence confidence from being used as a shortcut
for score-field evidence.

## P05 fully covered proposal example

P05 — Einbecker Brauhaus AG has all 15 score fields covered by numeric
first-pass proposals.

The strongest direct evidence includes brewing and thermal-process operations,
refrigeration, PV, biogas CHP with absorption chilling, heat recovery, process
control renewal, dated climate targets and planned electric clean-steam
generation.

The proposed anchors sum arithmetically to 59/100. This value remains a
review artifact only. All five dimension packages stay
`AWAITING_HUMAN_REVIEW` until a real reviewer approves or rejects the field
proposals and a separate canonical update is performed.

## P18 known-fossil / partial-evidence example

P18 — Glashütte Lamberts Waldsassen GmbH documents natural-gas firing in glass
production and a current ISO 50001 system.

Seven score fields receive numeric first-pass proposals, including fossil-heat
displacement relevance, weak scheduling flexibility, ordinal incremental-load
relevance and transition-gap fields. Eight fields remain
`NEEDS_RESEARCH`.

The unresolved fields include the firm-specific electric-melting route,
motor/converter/control evidence, thermal storage, power quality, onsite
integration and recent transition investment evidence.

The seven numeric proposals sum to 22, but no aggregate score is calculated
while eight required fields remain unresolved.
