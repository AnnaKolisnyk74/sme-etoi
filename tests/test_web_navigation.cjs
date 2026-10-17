// Exercise real handlers and renderers with the complete export and DOM event sinks.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const nodes=new Map(),stored=new Map();
function element(key,dataset){
  if(!nodes.has(key)){
    const classes=new Set();
    nodes.set(key,{dataset:dataset||{},innerHTML:'',textContent:'',value:'',hidden:false,handlers:{},
      classList:{toggle(c,on){const yes=on===undefined?!classes.has(c):on;if(yes)classes.add(c);else classes.delete(c);return yes;},add(c){classes.add(c)},remove(c){classes.delete(c)},contains(c){return classes.has(c)}},
      addEventListener(type,fn){this.handlers[type]=fn},scrollIntoView(){this.scrolled=true},focus(){this.focused=true}});
  }
  if(dataset)nodes.get(key).dataset=dataset;
  return nodes.get(key);
}
const html=fs.readFileSync(path.join(root,'web/index.html'),'utf8');
const navs=[...html.matchAll(/data-nav="([^"]+)"/g)].map(([,nav])=>element('nav:'+nav,{nav}));
const tabs=[...html.matchAll(/data-scope="([^"]+)"/g)].map(([,scope])=>element('scope:'+scope,{scope}));
const detailTabs=['overview','analysis','research','sources'].map(detailTab=>element('detail:'+detailTab,{detailTab}));
const findingRows=()=>[...element('#researchFindings').innerHTML.matchAll(/data-company-id="([^"]+)"/g)].map(([,id],i)=>element('finding:'+i,{companyId:id}));
const taskRows=()=>[...element('#researchRows').innerHTML.matchAll(/data-id="([^"]+)"/g)].map(([,id],i)=>element('task:'+i,{id}));
const companyRows=()=>[...element('#companyRows').innerHTML.matchAll(/data-id="([^"]+)"/g)].map(([,id])=>element('company:'+id,{id}));
const context=vm.createContext({Intl,
  localStorage:{getItem:k=>stored.get(k)??null,setItem:(k,v)=>stored.set(k,v)},
  setTimeout:()=>1,clearTimeout(){},history:{back(){}},location:{reload(){}},
  document:{body:element('body'),querySelector:s=>element(s),querySelectorAll(s){
    if(s==='.tab[data-scope]'||s==='.tab')return tabs;
    if(s==='.nav-row'||s==='[data-nav]')return navs;
    if(s==='[data-detail-tab]')return detailTabs;
    if(s==='#companyRows tr[data-id]')return companyRows();
    if(s==='#researchRows tr[data-id]')return taskRows();
    if(s==='#researchFindings [data-company-id]')return findingRows();
    return [];
  }}
});
const run=code=>vm.runInContext(code,context);
const fire=(selector,type='click',value)=>{const e=element(selector);assert.equal(typeof e.handlers[type],'function',selector+' handler');e.handlers[type]({target:{value,closest(){return null;}}});};
context.payload=JSON.parse(fs.readFileSync(path.join(root,'web/data/sme_etoi.json'),'utf8'));
const before=JSON.stringify(context.payload);
run(fs.readFileSync(path.join(root,'web/app.js'),'utf8').replace(/init\(\);\s*$/,''));
run('state.data=payload; bind();');

// Opening a known firm from another area clears incompatible old filters and
// lands on its actual page, keeping the selection, detail and chart consistent.
run('state.query="__no_match__";state.focus="high";state.scope="mine";state.page=9;showNav("sources");openCompany("P71");');
assert.equal(run('state.selectedId'),'P71');
assert.equal(run('state.query'),'');assert.equal(run('state.focus'),'');assert.equal(run('state.scope'),'all');
assert.equal(element('#globalSearch').value,'');assert.equal(element('#focusFilter').value,'');
assert.match(element('#companyRows').innerHTML,/<tr class="selected" data-id="P71">/);
assert.ok(element('#detailContent').innerHTML.includes(run('esc(companyById("P71").legal_entity)')));
assert.equal(run('state.activeNav'),'companies');assert.equal(element('.page-title-line h1').textContent,'Zielunternehmen');
assert.equal(element('.tabs').hidden,false);
assert.match(element('#kpiTotal').innerHTML,/>100<\/div>/);
run('state.query="P71";openCompany("P71","research");');
assert.equal(run('state.query'),'P71');assert.equal(run('state.detailTab'),'research');
assert.equal(run('companies().length'),1);
assert.equal(element('#tableSearch').value,'P71');
const oldSelection=run('state.selectedId');run('openCompany("__outside_sample__");');assert.equal(run('state.selectedId'),oldSelection);

// Pagination must update the selected row and its detail together. Closing the
// panel must remain closed until another row/action selects a company.
run('state.query="";state.focus="";state.scope="all";state.page=1;state.selectedId=null;showNav("companies");');
const first=run('state.selectedId');fire('#nextPage');
assert.equal(run('state.page'),2);assert.notEqual(run('state.selectedId'),first);
const second=run('state.selectedId');
assert.match(element('#companyRows').innerHTML,new RegExp('<tr class="selected" data-id="'+second+'">'));
assert.ok(element('#detailContent').innerHTML.includes(run('esc(companyById(state.selectedId).legal_entity)')));
fire('#prevPage');assert.equal(run('state.page'),1);assert.equal(run('state.selectedId'),first);
fire('#detailClose');assert.equal(run('state.selectedId'),null);assert.match(element('#detailContent').innerHTML,/Kein Unternehmen ausgewählt/);
assert.ok(!element('#companyRows').innerHTML.includes('class="selected"'));
fire('company:'+first);assert.equal(run('state.selectedId'),first);

// Personal scope is the pinned subset; removing the last pin updates the list,
// counts and detail immediately instead of showing an unrelated company.
run('togglePinned("P11");togglePinned("P71");state.scope="mine";state.page=1;showNav("companies");');
assert.deepEqual(JSON.parse(run('JSON.stringify(companies().map(c=>c.company_id).sort())')),['P11','P71']);
fire('#detailPin');assert.equal(run('companies().length'),1);
fire('#detailPin');assert.equal(run('companies().length'),0);
assert.equal(run('state.selectedId'),null);assert.match(element('#companyRows').innerHTML,/Keine angehefteten Unternehmen/);
assert.match(element('#kpiTotal').innerHTML,/>0<\/div>/);
run('openCompany("P71");');assert.equal(run('state.scope'),'all');assert.equal(run('state.selectedId'),'P71');

// Search a company ID in both the queue and finding history, then open a finding
// directly on the research detail. Clicking a source link keeps the history open.
run('state.researchQuery="P71";showNav("research");');
assert.match(element('#researchRows').innerHTML,/data-id="P71"/);
assert.ok(findingRows().length>0);
assert.ok(findingRows().every(r=>r.dataset.companyId==='P71'));
const finding=findingRows()[0];
finding.handlers.click({target:{closest(){return {};}}});
assert.equal(run('state.activeNav'),'research');
finding.handlers.click({target:{closest(){return null;}}});
assert.equal(run('state.selectedId'),'P71');assert.equal(run('state.detailTab'),'research');
assert.match(element('#detailContent').innerHTML,/Öffentliche Recherchebefunde/);
run('state.researchQuery="__no_match__";renderResearch();');
assert.match(element('#researchRows').innerHTML,/Keine Rechercheaufgaben/);
assert.match(element('#researchFindings').innerHTML,/Recherchebefund-Protokoll · 0/);

// Switching areas keeps chrome and view mode synchronized; a dashboard explicitly
// shows charts, while ordinary company navigation preserves table-only mode.
fire('#viewModeSelect','change','table');assert.equal(element('#analyticsBand').hidden,true);
run('showNav("sources");openCompany("P11");');assert.equal(element('#analyticsBand').hidden,true);
run('showNav("dashboard");');assert.equal(element('#analyticsBand').hidden,false);assert.equal(element('#viewModeSelect').value,'analysis');
run('showNav("quality");');assert.equal(element('.page-title-line h1').textContent,'Qualitätssicherung');
fire('#globalSearch','input','P71');assert.equal(run('state.activeNav'),'companies');assert.equal(run('companies().length'),1);
run('showNav("methodology");');fire('#newViewCommand');
assert.equal(run('state.scope'),'all');assert.equal(run('state.query'),'');assert.equal(run('companies().length'),100);
assert.equal(run('state.activeNav'),'companies');assert.equal(element('#functionalPage').hidden,true);
fire('.nav-toggle');assert.equal(element('.app').classList.contains('nav-collapsed'),true);
fire('#waffleCommand');assert.equal(element('.app').classList.contains('nav-collapsed'),false);
assert.equal(JSON.stringify(context.payload),before,'navigation must not change company facts or evidence');
console.log('Navigation: filtered company links, paging/detail, close, pins, research links/search, chrome and chart mode passed on all 100 companies.');

// A firm without generated opportunities still opens its outstanding field work.
run('openCompany("P35");');
assert.match(element('#detailContent').innerHTML,/data-next-action="field"/);
fire('#nextActionCommand');assert.equal(run('state.detailTab'),'analysis');
assert.match(element('#detailContent').innerHTML,/Fehlender Fakt:/);
fire('#viewDocsCommand');assert.equal(run('state.activeNav'),'documentation');
assert.equal(JSON.stringify(context.payload),before);
console.log('Next action: a company with no generated opportunity opens its actual field questions; view help opens documentation.');

// The recovered complete imprint removes the false operator conflict.
run('openCompany("P95");');
assert.match(element('#detailContent').innerHTML,/data-next-action="research"/);
fire('#nextActionCommand');assert.equal(run('state.detailTab'),'research');
assert.match(element('#detailContent').innerHTML,/Betreiber identifiziert · Anlagenzuordnung offen/);
assert.equal(JSON.stringify(context.payload),before);
