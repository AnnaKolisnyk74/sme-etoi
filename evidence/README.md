# Evidence archive

This directory is the audit trail for the SME-ETOI research dataset.

## Structure

- `source_register.csv`: one row per source document or webpage.
- `certificate_register.csv`: mandatory ISO 50001, ISO 14001 and EMAS check for
  every eligible or scored company, including direct document links.
- `qa_review.csv`: one second-pass cross-file review row per selected pilot
  company, with unresolved eligibility limits and the independent-human-review
  state kept separate.
- `companies/<candidate_id>_<legal_entity>/evidence.md`: company-level identity,
  eligibility decision, evidence statements and unresolved questions.
- `documents/`: optional local copies only when redistribution is permitted.

## Evidence rules

1. The exact legal entity is anchored to the official company imprint and,
   where necessary, an official register.
2. Every decision and numeric field must point to a row in the source register.
3. Record the original URL in `source_link`, plus publisher, document title,
   publication/reporting period, access date and the page or section used.
4. Record the separately verifiable fact in `evidence_fact`. A document title or
   link alone is never treated as evidence.
5. Keep short evidence statements in the company file. Do not reproduce large
   copyrighted passages.
6. Do not upload third-party reports or webpages unless their licence permits
   redistribution. Use `LINK_ONLY` for externally hosted material.
7. Validate every URL before accepting the source. Record the result,
   validation date and resolved destination in `link_check_status`,
   `link_check_date` and `final_url`.
8. If a source disappears, retain its metadata and mark it `UNAVAILABLE`; do
   not silently replace it with a weaker source.
9. Every company file must be reviewed before the record can enter the final
   100-company sample.

## Link-check states

- `VERIFIED`: the page or document opens and supports the recorded fact.
- `VERIFIED_INDEX`: a stable index opens and provides the named report.
- `REDIRECT_VERIFIED`: the URL redirects to a relevant current page; the
  destination is recorded in `final_url`.
- `VERIFIED_EXPIRED`: the certificate or time-limited document opens and is
  authentic/relevant, but its stated validity ended before the access date.
  It is retained as historical evidence and must not prove current status.
- `EXISTS_ACCESS_CHALLENGE`: the URL resolves, but automated access is blocked
  (for example by Cloudflare); content was cross-checked in a search index and
  still requires manual review.
- `UNAVAILABLE`: the source no longer resolves or no longer contains the
  recorded evidence.

## Certificate-review states

Every included or still-eligible researched company must have one reviewed row
for each of `ISO 50001`, `ISO 14001` and `EMAS` in
`certificate_register.csv`. No final opportunity classification is allowed
while any of these rows remains `PENDING_CHECK`.

- `VALID`: a direct document or authoritative register entry proves current
  validity on the research date.
- `EXPIRED`: the document is authentic and relevant, but validity ended
  before the research date and no current successor was located.
- `DOCUMENT_FOUND_VALIDITY_UNCLEAR`: a direct relevant document exists, but
  current validity cannot be established from the accessible metadata.
- `CLAIM_ONLY`: a public claim exists, but no direct certificate or
  authoritative register evidence was located.
- `NOT_FOUND_AFTER_CHECK`: no public evidence was located in the defined
  official-site and exact-legal-name checks. This is not proof that the company
  has no certification.
- `PENDING_CHECK`: research is incomplete.
- `NOT_REQUIRED_EXCLUDED`: the candidate was excluded at the SME eligibility
  gate, so certificate research is not used for scoring.

## Review states

- `NOT_REVIEWED`
- `RESEARCHED`
- `USER_REVIEWED`
- `REVISION_REQUIRED`
- `APPROVED`

The automated/Codex second pass is a consistency and evidence QA, not an
independent human double-code. `qa_review.csv` therefore keeps
`independent_human_review_status=PENDING` until a different human reviewer has
checked the record.
