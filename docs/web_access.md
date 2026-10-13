# Hosted SME-ETOI web interface

URL: https://sme-etoi.fairorbit8.chatgpt.site

The Site is private to Anna's account. Open it while signed in to the associated
ChatGPT account. The existing static interface and checked dataset are copied
from the repository's `web/` directory; hosted source has its own version history.
The refresh button reloads the currently deployed snapshot.

## Update the existing Site

- Preserve Sites project ID `appgprj_6ace562b587881918393506c5382be9d`; do not create
  a second Site for subsequent research blocks.
- Read current Site/access metadata and use the Sites source helper with a fresh
  repository credential to open its source. Preserve the existing audience.
- After a research PR has passed CI and merged, copy the exact tested `web/`
  files into the Site's `dist/`, update `source-revision.json` with the merged
  GitHub commit, and preserve `.openai/hosting.json` and its project ID.
- Check JavaScript/data consistency, then synchronize/package with the source
  helper and publish the matching source commit and archive. Confirm successful
  deployment before reporting that the online data is updated.

The Site uses no internal Bayernwerk or CRM data. Source/anchor checks, unknown
facts, canonical scores and personal approval remain separated exactly as in
this repository.

## Local access

From this repository directory:

```bash
python -m http.server 8000 --directory web
```

Open http://localhost:8000 on the computer running that server.
