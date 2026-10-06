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
