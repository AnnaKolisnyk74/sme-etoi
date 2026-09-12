# Evidence archive

This directory is the audit trail for the SME-ETOI research dataset.

## Structure

- `source_register.csv`: one row per source document or webpage.
- `companies/<candidate_id>_<legal_entity>/evidence.md`: company-level identity,
  eligibility decision, evidence statements and unresolved questions.
- `documents/`: optional local copies only when redistribution is permitted.

## Evidence rules

1. The exact legal entity is anchored to the official company imprint and,
   where necessary, an official register.
2. Every decision and numeric field must point to a row in the source register.
3. Record the original URL, publisher, document title, publication/reporting
   period, access date and the page or section used.
4. Keep short evidence statements in the company file. Do not reproduce large
   copyrighted passages.
5. Do not upload third-party reports or webpages unless their licence permits
   redistribution. Use `LINK_ONLY` for externally hosted material.
6. If a source disappears, retain its metadata and mark it `UNAVAILABLE`; do
   not silently replace it with a weaker source.
7. Every company file must be reviewed before the record can enter the final
   100-company sample.

## Review states

- `NOT_REVIEWED`
- `RESEARCHED`
- `USER_REVIEWED`
- `REVISION_REQUIRED`
- `APPROVED`

