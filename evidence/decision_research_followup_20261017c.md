# Priority ownership and operator follow-up — 17 October 2026

Five existing profiles were revisited: first three SME-gate ranks P07,P10,P104,
then P47's previously identified group exclusion signal, plus the recently found
P95 operator boundary. **One operator conflict is corrected with newly recovered
primary content. No additional numeric field closes.** The100-company sample,
652 CHECKED proposals,848 UNKNOWN fields and12 unresolved SME gates remain.

## Findings and consequence

| Company | New checked scope | Remaining requirement |
| --- | --- | --- |
| P07 VARIOPLAST | Current own legal/footer content separately names the operating GmbH, Holding GmbH and Hongkong company. The2015 item calls the latter a subsidiary; the mould-making page uses branch language. | Names, family leadership and public descriptions do not establish current control percentages or complete same-period annual-work-unit and financial aggregation. Obtain the actual holding/HK chain. |
| P10 Oskar Lehmann | Own company page calls it a second-generation family company and places production, tooling and logistics together. Own imprint identifies KG and general-partner GmbH. | Executive representation and family-business wording do not determine shareholder/voting quotas or all linked same/adjacent-market businesses. Obtain partner and group statements. |
| P104 Holder | Current direct imprint names exact HRB230335 operator and Jochen/Henri Holder as executives. | Directors are not automatically shareholders. Secondary register summaries suggest holding/property links but are discovery only. Obtain primary current control and group accounts; exclude unrelated vehicle/motor namesakes. |
| P47 hofmann CERAMiC | IFGL's own2024/25 and2025/26 reports identify100percent German subsidiary interest. Printed staff tables show1181 permanent parent employees at31March2025 and1180 at31March2026. | Stronger two-date non-SME signal. The figures are point-in-time headcounts, not an explicit EU annual-work-unit calculation or final legal/sample ruling. Retain the gate and complete period/unit-based decision provenance. |
| P95 Winkler | **Complete own embedded imprint separately identifies** hotel Winkler Bräustüberl GmbH, Nürnberg HRB8374, and brewery Winkler Bräu GmbH&Co.KG, Nürnberg HRA13022, with Winkler Bräu Verwaltungs GmbH as general partner. | The earlier footer-based conflict was too broad and is superseded. Brewery legal identity is established within this source scope; current CHP operator, commissioning and hotel/brewery energy ownership still need attribution. No hotel asset or canonical name is automatically transferred. |

## How the Winkler correction was checked

The [own imprint page](https://www.winkler-braeu.de/credits/impressum) returns a
static shell containing a hotel footer and a loading placeholder. That footer
alone was incorrectly treated as the entire imprint in the earlier profile.
The own brewery landing page uses the brewery-KG footer.

The shell exposes an exact public text-block ID. The actual public frontend code
maps that ID and the observed German language to its content endpoint. A direct
GET of the **[embedded imprint body](https://api.text.bnamic.com/render/channels/de/4ae1122d-c1c8-11ea-8e3c-96000009c248/textblockshtml)**
returns both legal-entity sections, separate register numbers, contact/VAT data
and the brewery's general partner. This is content embedded by the company,
not a third-party directory inference. The HTML shell, discovery code and complete
body each have their own response/fingerprint records. No login or browser
session was used. S-P95-07's scope is corrected to static footer/placeholder;
new S-P95-09 records the complete content. Earlier dated evidence is retained.

The current profile outcome is ENTITY_IDENTIFIED_ASSET_SCOPE_OPEN. Its next
action now opens technical/source research instead of repeating the superseded
identity conflict. Existing true conflicts such as Ceramany remain separate.

## Provenance and limits

- [Five current follow-up profiles](decision_research_followups_20261017c.json)
  retain the SHA256 of the exact previous profile. The validator rejects missing
  predecessors, altered predecessor hashes, changed workstreams/legal entities
  and fabricated personal/final approval. The
  [frozen predecessor profiles](../data/history/decision_profiles_before_followup_20261017c.json)
  preserve the reviewable before/after record.
- [14 scoped body checks](decision_source_checks_20261017c.csv),
  [19 actual retrieval/code records](research_source_attempts_followup_20261017c.csv)
  and [20 executed queries](research_queries_followup_20261017c.csv) retain scope.
  Public discovery results include irrelevant or gated secondary pages; these
  are not used for shareholder percentages, numeric anchors or legal conclusions.
- IFGL PDF ownership tables were visually read at viewer52/printed50 for both
  years; staff tables at viewer57/printed55 and viewer58/printed56. Reports and
  German subsidiary bodies remain separate from UK/Czech namesakes. Full third-
  party bodies are temporary inspection files, not copied into the repository.
- The direct EUR-Lex PDF request delivered HTTP202 HTML challenge content. It is
  recorded as ACCESS_CHALLENGE and has no selected company-evidence source ID.
  Indexed official definition excerpts were available separately; no directly
  inspected legal PDF or final SME ruling is claimed. Recovery cases total94.
- Four new partial-eligibility records append to the
  [research-results ledger](../data/research_results.csv); its
  [prior96 rows](../data/history/research_results_before_followup_20261017c.csv)
  are frozen and preserved. Current ledger100 observations,15 YES. The four gates
  remain UNRESOLVED/RECHECK_DUE, separate from approval and canonical updates.
- Six additional primary sources bring registration to **632 assessed:568 scoped
  RECHECKED,52 CONTEXT_ONLY,12 UNAVAILABLE,0 missing**. Separate retrieval inventory:
  **910 URLs /835 retrievable**. A challenge body is not successful legal content.

These five follow-ups do not inflate initial-profile counts or historical field
attempt/closure totals. The web explicitly separates them:100 unique profiles,
756 field attempts,55 historical closures; current652 CHECKED/848 UNKNOWN. The
last initial six-company block remains60 attempts/zero closures. All score
proposals and canonical company/process/certificate/QA/coding/independent-review/
score files remain byte-identical. No internal company/CRM data were used.

Validation:267 Python tests, JavaScript syntax, complete632-source/100-finding
renderers, clarified-operator navigation and current gate-specific next actions,
pipeline write/check and whitespace checks. Browser visual QA is unavailable in
this managed environment. Publish only the tested green-CI merged web snapshot
to the existing owner-private Site.
