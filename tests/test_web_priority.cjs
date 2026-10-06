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
assert.match(html, /P30/);
assert.match(html, /QA/);
assert.match(html, /Informationsgewinn \(Proxy\)/);
const ranking = html.split('<h3>Next Best Coding Companies</h3>')[1].split('</section>')[0];
assert.equal((ranking.match(/<th(?:\s|>)/g) || []).length, 9);
const rows = [...ranking.matchAll(/<tr[^>]*>(.*?)<\/tr>/gs)].filter(m => m[1].includes('<td'));
assert.equal(rows.length, 10);
for (const [, row] of rows) assert.equal((row.match(/<td(?:\s|>)/g) || []).length, 9);
assert.match(rows[0][1], /Privat-Brauerei Zötler GmbH/);
assert.match(rows[0][1], /PASS/);
assert.match(rows[0][1], /HIGH/);
assert.match(rows[0][1], /<td>B<\/td><td>B<\/td>/);
// Evidence explanations must remain escaped when inserted into the card.
context.payload.company_work_summary.next_best_company.priority_reason = '<script>unsafe</script>';
vm.runInContext('renderFunctional("analysis");', context);
html = sinks.get('#functionalContent').innerHTML;
assert.ok(!html.includes('<script>unsafe</script>'));
assert.ok(html.includes('&lt;script&gt;unsafe&lt;/script&gt;'));
console.log('Scoring renderer: next company, QA/gain/coverage, 9 aligned columns and escaped evidence passed.');
