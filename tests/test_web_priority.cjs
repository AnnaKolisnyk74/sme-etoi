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
// A commercial RESEARCH status must not erase an evidenced technical level.
const fixture = (level, confidence='B', commercial='RESEARCH') => ({
  opportunities: [{opportunity_level:level, confidence, priority:commercial,
    sample_eligibility_status:'PROVISIONAL_PASS', commercial_status:'RESEARCH_REQUIRED'}],
  score_readiness:{score_status:'NEEDS_NUMERIC_CODING'}, opportunity_score:null,
});
for (const [company, expected] of [
  [fixture('HIGH'), 'A'], [fixture('MEDIUM'), 'B'], [fixture('LOW'), 'C'],
  [fixture('RESEARCH_REQUIRED'), 'UNKNOWN'], [fixture('', 'A', 'HIGH'), 'UNKNOWN'],
  [fixture('HIGH', 'C'), 'UNKNOWN'], [{opportunities:[]}, 'UNKNOWN'],
  [{opportunities:[],score_readiness:{score_status:'NOT_SCOREABLE_ELIGIBILITY'}}, 'BLOCKED'],
  [{...fixture('HIGH'),opportunities:[{...fixture('HIGH').opportunities[0],sample_eligibility_status:'ELIGIBILITY_PENDING'}]}, 'BLOCKED'],
]) {
  context.priorityFixture = company;
  const before = JSON.stringify(company);
  assert.equal(vm.runInContext('priority(priorityFixture)',context), expected);
  assert.equal(JSON.stringify(company),before);
}
context.priorityFixture = {...fixture('MEDIUM'),opportunities:[...fixture('HIGH','C').opportunities,...fixture('MEDIUM','B').opportunities]};
assert.equal(vm.runInContext('priority(priorityFixture)',context),'B');
const untouched = JSON.stringify(context.payload);
vm.runInContext('state.data=payload; renderPriority();',context);
let priorityHtml=sinks.get('#priorityDonut').innerHTML;
assert.ok(priorityHtml.includes('data-priority="UNKNOWN"'));
assert.ok(priorityHtml.includes('data-priority="BLOCKED"'));
assert.ok(priorityHtml.includes('Low (C)</span><strong>0</strong>'));
const priorityCounts=JSON.parse(vm.runInContext('JSON.stringify(payload.companies.reduce((a,c)=>{const p=priority(c);a[p]=(a[p]||0)+1;return a},{}))',context));
assert.ok(priorityCounts.A>0 && priorityCounts.B>0);
assert.equal(priorityCounts.BLOCKED,12);
assert.equal(Object.values(priorityCounts).reduce((a,b)=>a+b,0),100);
assert.equal(JSON.stringify(context.payload),untouched);
vm.runInContext('state.focus="high"; state.scope="potential"; renderPriority();',context);
assert.equal(vm.runInContext('companies().length',context),priorityCounts.A);
assert.ok(sinks.get('#priorityDonut').innerHTML.includes('High (A)</span><strong>'+priorityCounts.A+'</strong>'));
vm.runInContext('state.query="__no_such_company__"; renderPriority();',context);
assert.ok(!sinks.get('#priorityDonut').innerHTML.includes('NaN'));
assert.ok(sinks.get('#priorityDonut').innerHTML.includes('background:#edebe9'));
vm.runInContext('state.focus=""; state.query=""; state.scope="all";',context);
let exported='';
context.Blob=class {constructor(parts){exported=parts.join('');}};
context.URL={createObjectURL(){return 'blob:test'},revokeObjectURL(){}};
context.document.createElement=()=>({click(){}});
vm.runInContext('exportCsv();',context);
assert.ok(exported.split('\n')[0].includes('technical_priority'));
assert.ok(exported.includes('"UNKNOWN"') && exported.includes('"BLOCKED"'));
assert.equal(JSON.stringify(context.payload),untouched);
console.log('Technical priority: A/B survive commercial research; open facts and gates stay separate; filter, empty state and CSV passed.');
vm.runInContext('state.data = payload; renderFunctional("analysis");', context);
let html = sinks.get('#functionalContent').innerHTML;
assert.match(html, /Erstbewertung abgeschlossen/);
assert.ok(!html.includes('<h3>Next Best Coding Companies</h3>'));
assert.match(html, /100 \/ 100 Unternehmen/);
assert.match(html, /1500 \/ 1500 Felder bewertet/);
assert.match(html, /670 Zahlenvorschläge · Geprüft/);
assert.match(html, /830 dokumentierte Recherchelücken/);
assert.match(html, /Erstbewertung ist keine Score-Freigabe/);
assert.ok(!/KI[- ·]*geprüft/i.test(html));
assert.ok(!html.includes('Zahlenvorschläge warten auf Human Review'));
assert.match(html, /Finale Score-Freigabe abgeschlossen:<\/strong> 0 \/ 100/);
const batch = html.split('<h3>Zuletzt ausgewählter Coding-Batch · NBCC-2026-10-07-07</h3>')[1].split('</section>')[0];
const batchRows = [...batch.matchAll(/<tr[^>]*>(.*?)<\/tr>/gs)].filter(m => m[1].includes('<td'));
assert.equal(batchRows.length, 16);
for (const [, row] of batchRows) assert.equal((row.match(/<td(?:\s|>)/g) || []).length, 5);
assert.match(batchRows[0][1], /Flötzinger/);
assert.ok(batchRows[0][1].includes('<td>10</td><td>5</td>'));
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
assert.match(html, /673 \/ 673 registrierte Quellen eingestuft/);
assert.match(html, /610 im dokumentierten Umfang nachgeprüft/);
assert.match(html, /53 nur Kontext/);
assert.match(html, /10 nicht abrufbar/);
assert.match(html, /0 ohne Inhaltsprüfung/);
const boundaries = html.split('<h3>Inhaltliche Grenzen im Quellenbestand</h3>')[1].split('</section>')[0];
const boundaryRows = [...boundaries.matchAll(/<tr[^>]*>(.*?)<\/tr>/gs)].filter(m => m[1].includes('<td'));
assert.equal(boundaryRows.length, 63);
for (const [, row] of boundaryRows) assert.equal((row.match(/<td(?:\s|>)/g) || []).length, 4);
context.payload.source_content_review_summary.boundary_sources[0].scope_note = '<script>bad content</script>';
const coverage = html.split('<h3>Prüfabdeckung aller Sample-Firmen</h3>')[1].split('</section>')[0];
const coveredRows = [...coverage.matchAll(/<tr[^>]*>(.*?)<\/tr>/gs)].filter(m => m[1].includes('<td'));
assert.equal(coveredRows.length, 100);
for (const [, row] of coveredRows) assert.equal((row.match(/<td(?:\s|>)/g) || []).length, 6);
context.payload.source_audit_summary.recovery_cases[0].supported_scope = '<script>bad recovery</script>';
vm.runInContext('renderFunctional("sources");', context);
html = sinks.get('#functionalContent').innerHTML;
assert.ok(!html.includes('<script>bad recovery</script>'));
assert.ok(html.includes('&lt;script&gt;bad recovery&lt;/script&gt;'));
assert.ok(!html.includes('<script>bad content</script>'));
assert.ok(html.includes('&lt;script&gt;bad content&lt;/script&gt;'));
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
assert.match(html, /670 Felder · Geprüft/);
assert.match(html, /830 Feldfragen offen/);
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
assert.match(html, /86 technische Firmenprofile · 12 KMU-Prüfungen · 2 Firmenzuordnungen/);
assert.match(html, /933 offene Felder untersucht, 74 zusätzlich geprüft/);
assert.match(html, /Letzter Rechercheblock: 6 Firmen · 60 offene Felder untersucht · 0 zusätzlich geprüft · 60 weiterhin offen/);
assert.match(html,/Zusätzliche Nachprüfung: 3 Firmen · 29 Feldfragen untersucht · 3 zusätzlich geprüft · 26 weiterhin offen/);
assert.equal(context.payload.decision_research_summary.batches[2].reassessed_checked_field_count, 4);
assert.doesNotMatch(html, /5 frühere Feldvorschläge erneut bewertet/); // Prior block must not be labelled as latest.
assert.doesNotMatch(html, /1 Zahlenvorschlag zurückgenommen/);
context.loadProofFixture=context.payload.companies.find(c=>c.company_id==='P109').score_proposals.find(p=>p.score_field==='incremental_load_score');
assert.equal(context.loadProofFixture.proposed_value,null);
assert.match(vm.runInContext('fieldProof(loadProofFixture)',context),/Frühere Begründung/);
context.loadProofFixture.check_history.at(-1).original_evidence_basis='<script>old rationale unsafe</script>';
const oldProof=vm.runInContext('fieldProof(loadProofFixture)',context);
assert.ok(oldProof.includes('&lt;script&gt;old rationale unsafe&lt;/script&gt;'));
assert.ok(!oldProof.includes('<script>old rationale unsafe</script>'));

assert.ok(!html.includes('4 ältere geprüfte Vorschläge anhand neuer Quellen korrigiert')); // Latest block made no reassessments.
for (const cid of ['P47','P65','P88','P109','P110','P18','P77','P96','P98','P99','P11','P21','P107']) {
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
context.profileCompany=context.payload.companies.find(c=>c.company_id==='P24');
assert.match(vm.runInContext('decisionProfile(profileCompany)',context), /Auswahl 1 von 6 · Feldarbeitsrang 33/);
console.log('Decision profiles: selection counts, legal-entity conflicts, source links and escaped findings passed.');

// Full inventory coverage in the real renderers, using a fresh unmodified export.
context.payload=JSON.parse(fs.readFileSync(path.join(root,'web/data/sme_etoi.json'),'utf8'));
vm.runInContext('state.data=payload; state.researchQuery="";',context);
for(const view of ['home','recent','pinned','tasks','notes','opportunities','analysis','market','sectors','regions','technologies','methodology','quality','documentation','sources']){
  vm.runInContext(`renderFunctional(${JSON.stringify(view)});`,context);
  assert.ok(sinks.get('#functionalContent').innerHTML.length>50,view+' must render content');
}
vm.runInContext('renderFunctional("sources");',context);
html=sinks.get('#functionalContent').innerHTML;
assert.equal((html.match(/data-source-id=/g)||[]).length,673);
assert.equal((html.match(/data-certificate-key=/g)||[]).length,321);
assert.ok(html.includes('647 Quellen des aktuellen Samples · 26 außerhalb des Samples'));
vm.runInContext('renderResearch();',context);
html=sinks.get('#researchFindings').innerHTML;
assert.equal((html.match(/data-finding-id=/g)||[]).length,105);
assert.match(html,/16 dokumentierte YES-Befunde/);
vm.runInContext('renderFunctional("quality");',context);
html=sinks.get('#functionalContent').innerHTML;
assert.equal((html.match(/data-qa-company=/g)||[]).length,100);
assert.equal((html.match(/data-reliability-field=/g)||[]).length,16);
assert.match(html,/UNKNOWN/);
assert.match(html,/leere Konfliktliste bestätigt keine Übereinstimmung/);
vm.runInContext('renderFunctional("technologies");',context);
assert.equal((sinks.get('#functionalContent').innerHTML.match(/data-technology-id=/g)||[]).length,8);
vm.runInContext('renderFunctional("methodology");',context);
html=sinks.get('#functionalContent').innerHTML;
assert.equal((html.match(/data-score-field=/g)||[]).length,15);
assert.equal((html.match(/data-process-id=/g)||[]).length,13);
assert.equal((html.match(/data-rule-id=/g)||[]).length,9);
vm.runInContext('renderFunctional("documentation");',context);
html=sinks.get('#functionalContent').innerHTML;
assert.match(html,/https:\/\/sme-etoi\.fairorbit8\.chatgpt\.site/);
assert.match(html,/web_coverage_audit_20261013/);
vm.runInContext('state.selectedId="P11"; state.detailTab="analysis"; renderDetail();',context);
html=sinks.get('#detailContent').innerHTML;
assert.match(html,/Erneut bewertet/);
assert.match(html,/Fehlender Fakt:/);
assert.match(html,/QA-Prüfprotokoll/);
vm.runInContext('state.selectedId="P71"; state.detailTab="overview"; renderDetail();',context);
assert.match(sinks.get('#detailContent').innerHTML,/Energie- und Prozessstammdaten/);
context.payload.research_findings[0].finding_summary='<script>unsafe finding</script>';
context.payload.additional_sources[0].source_link='javascript:alert(1)';
context.payload.source_audit_summary.recovery_cases[0].original_url='javascript:alert(1)';
vm.runInContext('renderResearch(); renderFunctional("sources");',context);
assert.ok(sinks.get('#researchFindings').innerHTML.includes('&lt;script&gt;unsafe finding&lt;/script&gt;'));
assert.ok(!sinks.get('#functionalContent').innerHTML.includes('href="javascript:'));
context.taskFixture={research_tasks:[{research_rank:1,task_status:'EVIDENCE_FOUND'},{research_rank:2,task_status:'OPEN'}]};
assert.equal(vm.runInContext('topTask(taskFixture).research_rank',context),2);
console.log('Coverage: all 673 sources, 321 certificates, 105 findings, 100 QA protocols, libraries, methodology, history and safe links passed.');
// Expanding source boundaries or opening evidence links must keep the register visible.
let rowClick;
context.document.querySelectorAll=()=>[{dataset:{companyId:'P11'},addEventListener(type,callback){rowClick=callback;}}];
vm.runInContext('var savedOpenCompany=openCompany; var clickedCompany=null; openCompany=id=>{clickedCompany=id}; bindFunctionalCompanyRows();',context);
for(const element of ['a','details','button']){
  rowClick({target:{closest(selector){return selector.split(',').includes(element)?{}:null;}}});
  assert.equal(vm.runInContext('clickedCompany',context),null);
}
rowClick({target:{closest(){return null;}}});
assert.equal(vm.runInContext('clickedCompany',context),'P11');
vm.runInContext('openCompany=savedOpenCompany;',context);
console.log('Register navigation: evidence links and expanded boundaries keep the register open; company cells navigate.');

// Qualitative engine levels must not manufacture percentages or inherit a
// commercial HIGH/RESEARCH priority when the technical level is unknown.
context.document.querySelectorAll=()=>[];
for(const [o,expected] of [[{opportunity_level:'HIGH',priority:'RESEARCH'},'HIGH'],[{opportunity_level:'MEDIUM'},'MEDIUM'],[{opportunity_level:'LOW'},'LOW'],[{priority:'HIGH'},'UNKNOWN'],[{opportunity_level:'RESEARCH_REQUIRED',priority:'HIGH'},'UNKNOWN']]){
  context.signalFixture=o;
  assert.equal(vm.runInContext('technicalLevel(signalFixture)',context),expected);
  const output=vm.runInContext('technicalSignalRow(signalFixture)',context);
  assert.ok(output.includes('data-tech-level="'+expected+'"'));
  assert.ok(!output.includes('style="width:'));
  assert.ok(!output.includes('tech-fill'));
}
for(const value of ['',null,'UNKNOWN','not-a-grade']){
  context.confFixture=value;assert.equal(vm.runInContext('confClass(confFixture)',context),'conf-open');
}
context.signalFixture={opportunity_type:'<script>bad type</script>',confidence:'<script>bad confidence</script>',commercial_status:'<script>bad status</script>'};
const safeSignal=vm.runInContext('technicalSignalRow(signalFixture)',context);
assert.ok(!safeSignal.includes('<script>'));assert.match(safeSignal,/&lt;script&gt;bad type/i);
context.payload=JSON.parse(fs.readFileSync(path.join(root,'web/data/sme_etoi.json'),'utf8'));
const signalInput=JSON.stringify(context.payload);
vm.runInContext('state.data=payload;state.query="";state.focus="";state.scope="all";state.pageSize=100;renderTable();',context);
assert.equal(vm.runInContext('payload.companies.filter(c=>!nextStep(c)).length',context),0);
assert.equal(vm.runInContext('payload.companies.filter(c=>nextStep(c).kind==="eligibility").length',context),12);
for(const id of ['P35','P87','P110']){
  context.caseId=id;
  vm.runInContext('state.selectedId=caseId;state.detailTab="overview";renderDetail();',context);
  const output=sinks.get('#detailContent').innerHTML;
  assert.ok(!output.includes('Keine offene Aufgabe'));
  assert.ok(output.includes('id="nextActionCommand"'));
  assert.ok(!output.includes('tech-fill'));
}
for(const company of context.payload.companies){
  context.caseId=company.company_id;
  for(const tab of ['overview','analysis']){
    context.caseTab=tab;
    vm.runInContext('state.selectedId=caseId;state.detailTab=caseTab;renderDetail();',context);
    assert.equal((sinks.get('#detailContent').innerHTML.match(/data-tech-level=/g)||[]).length,company.opportunities.length);
  }
}
assert.equal(vm.runInContext('nextStep(companyById("P35")).kind',context),'field');
assert.equal(vm.runInContext('nextStep(companyById("P110")).kind',context),'identity');
context.stepFixture={opportunities:[],research_tasks:[{task_status:'EVIDENCE_FOUND',research_question:'already found'}],score_proposals:[{proposal_status:'NEEDS_RESEARCH',missing_fact:'<script>missing fact</script>'}]};
assert.equal(vm.runInContext('nextStep(stepFixture).kind',context),'field');
assert.ok(vm.runInContext('nextActionCard(stepFixture,nextStep(stepFixture))',context).includes('&lt;script&gt;missing fact'));
context.stepFixture={opportunities:[],score_proposals:[{proposal_status:'CHECKED'}]};
assert.equal(vm.runInContext('nextStep(stepFixture).kind',context),'approval');
assert.equal(vm.runInContext('nextStep(stepFixture).status',context),'CHECKED_PROPOSALS');
context.stepFixture={opportunities:[],score_proposals:[{proposal_status:'CHECKED'}],score_readiness:{score_status:'FINAL_SCORE_READY'}};
assert.equal(vm.runInContext('nextStep(stepFixture)',context),null);
assert.equal(JSON.stringify(context.payload),signalInput);
console.log('Signal/action semantics: categorical levels without invented percentages; unknown confidence stays neutral; all 100 companies retain their actual open work.');

context.gateCompany=context.payload.companies.find(c=>c.company_id==='P47');
assert.equal(vm.runInContext('nextStep(gateCompany).kind',context),'eligibility');
assert.match(vm.runInContext('nextStep(gateCompany).text',context),/Jahresarbeitseinheiten/);
