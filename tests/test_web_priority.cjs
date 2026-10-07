// Exercise the actual scoring renderer with exported data and minimal DOM sinks.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const sinks = new Map();
const context = vm.createContext({Intl, document: {
  querySelector(selector) {
    if (!sinks.has(selector)) sinks.set(selector, {innerHTML: '', textContent: ''});
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
assert.match(html, /1500 \/ 1500 Felder geprüft/);
assert.match(html, /554 Zahlenvorschläge/);
assert.match(html, /946 dokumentierte Recherchelücken/);
assert.match(html, /Erstbewertung ist keine Score-Freigabe/);
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
