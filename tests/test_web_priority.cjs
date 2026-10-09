// Exercise the actual scoring renderer with exported data and minimal DOM sinks.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const sinks = new Map();
const context = vm.createContext({Intl, document: {
  querySelector(selector) {
    if (!sinks.has(selector)) sinks.set(selector, {innerHTML: '', textContent: '', addEventListener() {}});
    return sinks.get(selector);
  },
  querySelectorAll() {return [];},
}});
const code = fs.readFileSync(path.join(root, 'web/app.js'), 'utf8').replace(/init\(\);\s*$/, '');
vm.runInContext(code, context);
context.payload = JSON.parse(fs.readFileSync(path.join(root, 'web/data/sme_etoi.json'), 'utf8'));
vm.runInContext('state.data = payload; renderFunctional("analysis");', context);
let html = sinks.get('#functionalContent').innerHTML;
assert.match(html, /Erstbewertung abgeschlossen/);
assert.ok(!html.includes('<h3>Next Best Coding Companies</h3>'));
assert.match(html, /100 \/ 100 Unternehmen/);
assert.match(html, /1500 \/ 1500 Felder bewertet/);
assert.match(html, /605 Zahlenvorschläge · Geprüft/);
assert.match(html, /895 dokumentierte Recherchelücken/);
assert.match(html, /Erstbewertung ist keine Score-Freigabe/);
assert.ok(!/KI[- ·]*geprüft/i.test(html));
assert.ok(!html.includes('Zahlenvorschläge warten auf Human Review'));
assert.match(html, /Finale Score-Freigabe abgeschlossen:<\/strong> 0 \/ 100/);
const batch = html.split('<h3>Zuletzt ausgewählter Coding-Batch · NBCC-2026-10-07-07</h3>')[1].split('</section>')[0];
const batchRows = [...batch.matchAll(/<tr[^>]*>(.*?)<\/tr>/gs)].filter(m => m[1].includes('<td'));
assert.equal(batchRows.length, 16);
for (const [, row] of batchRows) assert.equal((row.match(/<td(?:\s|>)/g) || []).length, 5);
assert.match(batchRows[0][1], /Flötzinger/);
assert.ok(batchRows[0][1].includes('<td>6</td><td>9</td>'));
const gates = html.split('<h3>Dokumentarische Bewertung bei offener Eligibility · 12 Unternehmen</h3>')[1].split('</section>')[0];
const gateRows = [...gates.matchAll(/<tr[^>]*>(.*?)<\/tr>/gs)].filter(m => m[1].includes('<td'));
assert.equal(gateRows.length,12);
for (const [, row] of gateRows) {
  assert.equal((row.match(/<td(?:\s|>)/g) || []).length, 5);
  assert.match(row, /15/);
  assert.match(row, /group_check/);
}
// Keep the ranked rendering branch tested independently of the completed sample.
const example = context.payload.companies.find(c=>c.company_id==='P71');
example.workflow_priority.workflow_action='CODE_NOW';
example.workflow_priority.coding_rank=1;
context.payload.company_work_summary.next_best_company={company_id:'P71',legal_entity:example.legal_entity,coding_rank:1,priority_reason:'<script>unsafe</script>'};
vm.runInContext('renderFunctional("analysis");', context);
html=sinks.get('#functionalContent').innerHTML;
const ranking=html.split('<h3>Next Best Coding Companies</h3>')[1].split('</section>')[0];
assert.equal((ranking.match(/<th(?:\s|>)/g)||[]).length,9);
const rankRows=[...ranking.matchAll(/<tr[^>]*>(.*?)<\/tr>/gs)].filter(m=>m[1].includes('<td'));
assert.equal(rankRows.length,1);
assert.equal((rankRows[0][1].match(/<td(?:\s|>)/g)||[]).length,9);
assert.ok(html.includes('&lt;script&gt;unsafe&lt;/script&gt;'));
// A company with zero matching opportunity rules retains readiness gates.
context.noMatchGate = {opportunities: [], score_readiness: {score_status: 'NOT_SCOREABLE_ELIGIBILITY'}};
assert.equal(vm.runInContext('eligibility(noMatchGate)', context), 'ELIGIBILITY_PENDING');
assert.equal(vm.runInContext('actionability(noMatchGate)', context), 'ELIGIBILITY_BLOCKED');
context.noMatchCompany = context.payload.companies.find(c => c.company_id === 'P35');
assert.equal(context.noMatchCompany.opportunities.length, 0);
assert.equal(vm.runInContext('eligibility(noMatchCompany)', context), 'PROVISIONAL_PASS');
// Evidence explanations must remain escaped when inserted into the card.
context.payload.company_work_summary.next_best_company.priority_reason = '<script>unsafe</script>';
context.payload.coding_batches.at(-1).companies[0].legal_entity = '<img onerror=unsafe>';
context.payload.eligibility_coding_selections[0].legal_entity = '<script>gate unsafe</script>';
vm.runInContext('renderFunctional("analysis");', context);
html = sinks.get('#functionalContent').innerHTML;
assert.ok(!html.includes('<script>unsafe</script>'));
assert.ok(html.includes('&lt;script&gt;unsafe&lt;/script&gt;'));
assert.ok(!html.includes('<img onerror=unsafe>'));
assert.ok(html.includes('&lt;img onerror=unsafe&gt;'));
assert.ok(!html.includes('<script>gate unsafe</script>'));
assert.ok(html.includes('&lt;script&gt;gate unsafe&lt;/script&gt;'));
vm.runInContext('renderFunctional("sources");', context);
html = sinks.get('#functionalContent').innerHTML;
assert.match(html, /100 \/ 100 Sample-Firmen geprüft/);
assert.match(html, /HTTP 200 bestätigt keine Unternehmenszuordnung/);
assert.match(html, /Prüfabdeckung aller Sample-Firmen/);
const coverage = html.split('<h3>Prüfabdeckung aller Sample-Firmen</h3>')[1].split('</section>')[0];
const coveredRows = [...coverage.matchAll(/<tr[^>]*>(.*?)<\/tr>/gs)].filter(m => m[1].includes('<td'));
assert.equal(coveredRows.length, 100);
for (const [, row] of coveredRows) assert.equal((row.match(/<td(?:\s|>)/g) || []).length, 6);
context.payload.source_audit_summary.recovery_cases[0].supported_scope = '<script>bad recovery</script>';
vm.runInContext('renderFunctional("sources");', context);
html = sinks.get('#functionalContent').innerHTML;
assert.ok(!html.includes('<script>bad recovery</script>'));
assert.ok(html.includes('&lt;script&gt;bad recovery&lt;/script&gt;'));
console.log('Scoring/source renderers: priority, live batch, all 100 audited companies, aligned columns and escaped evidence passed.');

// Render all field statuses, including withdrawn evidence, in the real detail view.
vm.runInContext('state.selectedId="P23"; state.detailTab="analysis"; renderDetail();', context);
html = sinks.get('#detailContent').innerHTML;
assert.equal((html.match(/<tr data-score-field=/g) || []).length, 15);
const withdrawn = html.match(/<tr data-score-field="temperature_fit_score">(.*?)<\/tr>/s)[1];
assert.match(withdrawn, /UNKNOWN/);
assert.match(withdrawn, /Recherche nötig/);
assert.match(html, /<td>Geprüft<\/td>/);
assert.ok(!/KI[- ·]*geprüft/i.test(html));
const proposal = context.payload.companies.find(c => c.company_id === 'P23').score_proposals[0];
proposal.evidence_basis = '<script>unsafe field</script>';
vm.runInContext('renderDetail();', context);
html = sinks.get('#detailContent').innerHTML;
assert.ok(!html.includes('<script>unsafe field</script>'));
assert.ok(html.includes('&lt;script&gt;unsafe field&lt;/script&gt;'));
console.log('Detail renderer: 15 field statuses, withdrawn values and escaped source rationale passed.');

// The company table distinguishes field evidence, SME eligibility and ISO absence.
vm.runInContext('state.query=""; state.page=1; state.pageSize=100; renderTable(); renderMetrics(); renderEvidenceOverview();', context);
html = sinks.get('#companyRows').innerHTML;
const companyRows = [...html.matchAll(/<tr[^>]*>(.*?)<\/tr>/gs)];
assert.equal(companyRows.length, 100);
for (const [, row] of companyRows) assert.equal((row.match(/<td(?:\s|>)/g) || []).length, 12);
assert.ok(!html.includes('Vorläufig'));
assert.match(html, /KMU wahrscheinlich/);
assert.match(html, /KMU-Prüfung offen/);
assert.match(html, /Kein öffentlicher Nachweis/);
assert.match(html, /Gültig belegt/);
assert.match(html, /Geprüft: [0-9]+ \/ 15/);
assert.ok(!sinks.get('#kpiQuality').innerHTML.includes('Qualifiziert'));
html = sinks.get('#evidenceOverview').innerHTML;
assert.match(html, /605 Felder · Geprüft/);
assert.match(html, /895 Feldfragen offen/);
assert.match(html, /ISO 50001 13 · ISO 14001 27 · EMAS 4/);
vm.runInContext('state.query="FM-Plast"; renderEvidenceOverview();', context);
html = sinks.get('#evidenceOverview').innerHTML;
assert.match(html, /1 Unternehmen/);
assert.match(html, /ISO 50001 1/);
vm.runInContext('state.query=""; state.selectedId="P12"; state.detailTab="overview"; renderDetail();', context);
html = sinks.get('#detailContent').innerHTML;
assert.match(html, /Zertifikatsnachweise/);
assert.match(html, /Abgelaufen/);
assert.match(html, /2026-09-11/);
assert.match(html, /Kein öffentlicher Nachweis/);
const cert = context.payload.companies.find(c => c.company_id === 'P12').certificate_checks[0];
cert.notes = '<script>unsafe certificate</script>';
cert.direct_certificate_url = 'javascript:alert(1)';
vm.runInContext('renderDetail();', context);
html = sinks.get('#detailContent').innerHTML;
assert.ok(html.includes('&lt;script&gt;unsafe certificate&lt;/script&gt;'));
assert.ok(!html.includes('javascript:'));
vm.runInContext('state.selectedId="P26"; state.detailTab="sources"; renderDetail();', context);
html = sinks.get('#detailContent').innerHTML;
assert.match(html, /Inhalt nicht abrufbar/);
assert.match(html, /Inhalt nachgeprüft/);
assert.match(html, /Aussageumfang:/);
console.log('Company view: ISO evidence, separate SME status, filtered field counts and certificate/source details passed.');
// Decision findings stay visible and escaped, including conflicting legal names.
vm.runInContext('renderFunctional("analysis");', context);
html = sinks.get('#functionalContent').innerHTML;
assert.match(html, /20 technische Firmenprofile · 12 KMU-Prüfungen · 2 Firmenzuordnungen/);
assert.match(html, /146 offene Felder untersucht, 8 zusätzlich geprüft/);
assert.match(html, /Letzter Rechercheblock: 10 Firmen · 96 offene Felder untersucht · 6 zusätzlich geprüft · 90 weiterhin offen/);
for (const cid of ['P47','P65','P88','P109','P110','P18','P77','P96','P98','P99']) {
  context.profileCompany=context.payload.companies.find(c=>c.company_id===cid);
  const card=vm.runInContext('decisionProfile(profileCompany)',context);
  assert.match(card, /Vertiefte Firmenprüfung/);
  assert.match(card, /Nächster Schritt/);
}
context.profileCompany=context.payload.companies.find(c=>c.company_id==='P110');
context.profileCompany.decision_research_profile.finding='<script>scope unsafe</script>';
const card=vm.runInContext('decisionProfile(profileCompany)',context);
assert.ok(card.includes('&lt;script&gt;scope unsafe&lt;/script&gt;'));
assert.ok(!card.includes('<script>scope unsafe</script>'));
assert.match(card,/Firmenzuordnung widersprüchlich/);
console.log('Decision profiles: selection counts, legal-entity conflicts, source links and escaped findings passed.');
