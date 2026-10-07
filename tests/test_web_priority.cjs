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
assert.match(html, /P77/);
assert.match(html, /QA/);
assert.match(html, /Informationsgewinn \(Proxy\)/);
const ranking = html.split('<h3>Next Best Coding Companies</h3>')[1].split('</section>')[0];
assert.equal((ranking.match(/<th(?:\s|>)/g) || []).length, 9);
const rows = [...ranking.matchAll(/<tr[^>]*>(.*?)<\/tr>/gs)].filter(m => m[1].includes('<td'));
assert.equal(rows.length, 10);
for (const [, row] of rows) assert.equal((row.match(/<td(?:\s|>)/g) || []).length, 9);
assert.match(rows[0][1], /metak GmbH &amp; Co. KG/);
assert.match(rows[0][1], /PASS/);
assert.match(rows[0][1], /MEDIUM/);
assert.match(rows[0][1], /<td>B<\/td><td>B<\/td>/);
const batch = html.split('<h3>Zuletzt ausgewählter Coding-Batch · NBCC-2026-10-07-04</h3>')[1].split('</section>')[0];
assert.match(batch, /Feldzahlen sind keine SME-ETOI Scores/);
assert.equal((batch.match(/<th(?:\s|>)/g) || []).length, 5);
const batchRows = [...batch.matchAll(/<tr[^>]*>(.*?)<\/tr>/gs)].filter(m => m[1].includes('<td'));
assert.equal(batchRows.length, 12);
for (const [, row] of batchRows) {
  assert.equal((row.match(/<td(?:\s|>)/g) || []).length, 5);
  assert.match(row, /RESEARCH FIRST/);
}
for (const [i, name, numeric, gaps] of [[0,/Spritzguß Müller/,5,10],[1,/Stocker/,1,14],[2,/Dorn/,9,6],[3,/AK Kunststoff/,4,11],[4,/Horstmann/,4,11],[5,/Kaltenkirchen/,4,11],[6,/Wieland/,5,10],[7,/KPM/,3,12],[8,/TechnoKer/,6,9],[9,/ceram/,4,11],[10,/Falter/,2,13],[11,/Si-Tech/,8,7]]) {
  assert.match(batchRows[i][1], name);
  assert.ok(batchRows[i][1].includes(`<td>${numeric}</td><td>${gaps}</td>`));
}
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
vm.runInContext('renderFunctional("analysis");', context);
html = sinks.get('#functionalContent').innerHTML;
assert.ok(!html.includes('<script>unsafe</script>'));
assert.ok(html.includes('&lt;script&gt;unsafe&lt;/script&gt;'));
assert.ok(!html.includes('<img onerror=unsafe>'));
assert.ok(html.includes('&lt;img onerror=unsafe&gt;'));
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
