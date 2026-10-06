const state={
  data:null,
  selectedId:null,
  page:1,
  pageSize:10,
  query:"",
  focus:"",
  scope:"all",
  detailTab:"overview",
  researchQuery:"",
  sortMode:"name",
  activeNav:"companies"
};
const $=s=>document.querySelector(s);
const $$=s=>Array.from(document.querySelectorAll(s));

function esc(v){return String(v??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;")}
function titleCase(v){return String(v||"").replaceAll("_"," ").replace(/\b\w/g,c=>c.toUpperCase())}
function n(v){return new Intl.NumberFormat("de-DE").format(v||0)}
function money(v){return v===null||v===undefined||v===""?"—":new Intl.NumberFormat("de-DE",{maximumFractionDigits:2}).format(v)}
function uniq(a){return Array.from(new Set(a.filter(Boolean)))}
function eligibility(c){return c.opportunities?.[0]?.sample_eligibility_status||"PROVISIONAL_PASS"}
function actionability(c){return c.opportunities?.[0]?.actionability_status||"PROVISIONAL"}

const stateAbbr={
  "Bavaria":"BY","Bayern":"BY","Baden-Württemberg":"BW","North Rhine-Westphalia":"NRW",
  "Nordrhein-Westfalen":"NRW","Hesse":"HE","Hessen":"HE","Lower Saxony":"NI","Niedersachsen":"NI",
  "Saxony":"SN","Sachsen":"SN","Thuringia":"TH","Thüringen":"TH","Brandenburg":"BB",
  "Rhineland-Palatinate":"RP","Saarland":"SL","Schleswig-Holstein":"SH","Hamburg":"HH",
  "Berlin":"BE","Bremen":"HB","Saxony-Anhalt":"ST","Sachsen-Anhalt":"ST",
  "Mecklenburg-Vorpommern":"MV"
};

function sectorLabel(c){
  const map={
    plastics_processing:"Kunststoff",
    food_beverage:"Lebensmittel",
    ceramics:"Keramik",
    metal_finishing:"Oberfläche",
    glass:"Glas",
    paper:"Papier",
    chemicals:"Chemie",
    pharma:"Pharma",
    packaging:"Verpackung"
  };
  return map[c.process_stratum]||titleCase(c.process_stratum)||"Industrie";
}
function priority(c){
  const values=(c.opportunities||[]).map(o=>(o.priority||o.opportunity_level||"").toUpperCase());
  if(values.includes("HIGH")) return "A";
  if(values.includes("MEDIUM")) return "B";
  return "C";
}
function priorityClass(p){return p==="A"?"priority-a":p==="B"?"priority-b":"priority-c"}
function statusInfo(c){
  const e=eligibility(c);
  if(e==="CONFIRMED") return ["Qualifiziert","status-qualified"];
  if(e==="ELIGIBILITY_PENDING") return ["In Prüfung","status-review"];
  if(e==="EXCLUDED") return ["Blockiert","status-blocked"];
  return ["Vorläufig","status-watch"];
}
function confClass(g){return g==="A"?"conf-a":g==="B"?"conf-b":"conf-c"}
function isoCell(c){
  const s=(c.certifications?.iso_50001||"").toUpperCase();
  if(s==="VALID"||s==="CURRENT"||s==="YES") return '<span class="iso-yes">● Ja</span>';
  if(s==="EXPIRED") return '<span class="iso-no">◌ Abgelaufen</span>';
  if(s==="NOT_FOUND_AFTER_CHECK") return '<span class="iso-no">—</span>';
  return '<span class="iso-no">?</span>';
}
function topTask(c){return (c.research_tasks||[]).slice().sort((a,b)=>(a.research_rank||9999)-(b.research_rank||9999))[0]||null}
function storageGet(key,fallback){
  try{const value=localStorage.getItem(key);return value?JSON.parse(value):fallback}catch(_){return fallback}
}
function storageSet(key,value){
  try{localStorage.setItem(key,JSON.stringify(value))}catch(_){}
}
function recentIds(){return storageGet("sme-etoi-recent",[])}
function pinnedIds(){return storageGet("sme-etoi-pinned",[])}
function notesMap(){return storageGet("sme-etoi-notes",{})}
function markRecent(id){
  if(!id)return;
  const next=[id,...recentIds().filter(x=>x!==id)].slice(0,20);
  storageSet("sme-etoi-recent",next);
}
function togglePinned(id){
  const current=pinnedIds();
  const next=current.includes(id)?current.filter(x=>x!==id):[id,...current];
  storageSet("sme-etoi-pinned",next);
  return next.includes(id);
}
function companyById(id){return state.data?.companies?.find(c=>c.company_id===id)||null}
function openCompany(id){
  if(!companyById(id))return;
  state.selectedId=id;markRecent(id);state.detailTab="overview";
  setActiveNav("companies");showCompanies();renderTable();renderDetail();
}
function setActiveNav(view){
  state.activeNav=view;
  $(".nav-row").forEach(x=>x.classList.toggle("active",x.dataset.nav===view));
}
function setPageChrome(title,showTabs){
  const h=$(".page-title-line h1");if(h)h.textContent=title;
  const tabs=$(".tabs");if(tabs)tabs.hidden=!showTabs;
}
function genericTable(headers,rows){
  return '<div class="functional-table-wrap"><table class="entity-table"><thead><tr>'+
    headers.map(h=>'<th>'+esc(h)+'</th>').join("")+
    '</tr></thead><tbody>'+rows.join("")+'</tbody></table></div>';
}
function aggregateBy(items,keyFn){
  const map=new Map();
  items.forEach(item=>{const key=keyFn(item)||"Unbekannt";if(!map.has(key))map.set(key,[]);map.get(key).push(item)});
  return map;
}
function bindFunctionalCompanyRows(){
  $("#functionalContent [data-company-id]").forEach(row=>row.addEventListener("click",()=>openCompany(row.dataset.companyId)));
}
function companies(){
  let rows=state.data.companies.slice();
  const q=state.query.trim().toLowerCase();
  if(q) rows=rows.filter(c=>[
    c.legal_entity,c.city,c.state,c.process_stratum,c.nace_label,
    ...(c.processes||[]).map(p=>p.process_name+" "+p.process_name_raw)
  ].join(" ").toLowerCase().includes(q));
  if(state.focus==="pending") rows=rows.filter(c=>eligibility(c)==="ELIGIBILITY_PENDING");
  if(state.focus==="high") rows=rows.filter(c=>priority(c)==="A");
  if(state.focus==="score") rows=rows.filter(c=>c.opportunity_score!==null&&c.opportunity_score!==undefined);
  if(state.scope==="potential") rows.sort((a,b)=>priority(a).localeCompare(priority(b))-(0)||((b.opportunity_score||-1)-(a.opportunity_score||-1))||a.legal_entity.localeCompare(b.legal_entity));
  else if(state.scope==="region") rows.sort((a,b)=>(a.state||"").localeCompare(b.state||"")||a.legal_entity.localeCompare(b.legal_entity));
  else if(state.scope==="sector") rows.sort((a,b)=>sectorLabel(a).localeCompare(sectorLabel(b))||a.legal_entity.localeCompare(b.legal_entity));
  else rows.sort((a,b)=>a.legal_entity.localeCompare(b.legal_entity));
  return rows;
}
function showToast(msg){
  const t=$("#toast");t.textContent=msg;t.hidden=false;
  clearTimeout(showToast.timer);showToast.timer=setTimeout(()=>t.hidden=true,2400);
}
function renderMetrics(){
  const rows=companies();
  const opps=rows.flatMap(c=>c.opportunities||[]);
  const ab=rows.filter(c=>["A","B"].includes(c.evidence_confidence)).length;
  const pending=rows.filter(c=>eligibility(c)==="ELIGIBILITY_PENDING").length;
  const cards=[
    ["kpiTotal","Gesamtanzahl Zielunternehmen",rows.length,"aktueller Filter"],
    ["kpiQuality","Qualifiziert (A/B)",ab,"Evidence Confidence"],
    ["kpiReview","In Prüfung",pending,"SME / Gruppenstatus"],
    ["kpiSignals","Opportunity Signale",opps.length,"technische Signale"]
  ];
  cards.forEach(([id,label,value,sub])=>{
    $("#"+id).innerHTML='<div class="metric-label">'+esc(label)+'</div><div class="metric-value">'+n(value)+'</div><div class="metric-sub">'+esc(sub)+'</div>';
  });
}
function renderRegionChart(){
  const counts=new Map();
  companies().forEach(c=>counts.set(c.state||"Unbekannt",(counts.get(c.state||"Unbekannt")||0)+1));
  const rows=Array.from(counts.entries()).sort((a,b)=>b[1]-a[1]).slice(0,5);
  const max=Math.max(...rows.map(r=>r[1]),1);
  $("#regionChart").innerHTML=rows.map(([name,count])=>
    '<div class="region-col"><div class="region-value">'+count+'</div><div class="region-bar-wrap"><div class="region-bar" style="height:'+((count/max)*100).toFixed(1)+'%"></div></div><div class="region-label">'+esc(stateAbbr[name]||name.slice(0,3).toUpperCase())+'</div></div>'
  ).join("");
}
function renderPriority(){
  const rows=companies(), counts={A:0,B:0,C:0};
  rows.forEach(c=>counts[priority(c)]++);
  const total=rows.length||1;
  const a=counts.A/total*100,b=counts.B/total*100;
  const bg='conic-gradient(#107c10 0 '+a+'%, #0f6cbd '+a+'% '+(a+b)+'%, #ff8c00 '+(a+b)+'% 100%)';
  $("#priorityDonut").innerHTML=
    '<div class="priority-donut" style="background:'+bg+'"><div class="priority-center"><strong>'+rows.length+'</strong><span>Zielunternehmen</span></div></div>'+
    '<div class="priority-legend">'+
      '<div class="priority-legend-row"><span class="legend-dot" style="background:#107c10"></span><span>High (A)</span><strong>'+counts.A+'</strong></div>'+
      '<div class="priority-legend-row"><span class="legend-dot" style="background:#0f6cbd"></span><span>Medium (B)</span><strong>'+counts.B+'</strong></div>'+
      '<div class="priority-legend-row"><span class="legend-dot" style="background:#ff8c00"></span><span>Low (C)</span><strong>'+counts.C+'</strong></div>'+
    '</div>';
}
function renderTable(){
  const all=companies(), pages=Math.max(1,Math.ceil(all.length/state.pageSize));
  if(state.page>pages) state.page=pages;
  const start=(state.page-1)*state.pageSize, visible=all.slice(start,start+state.pageSize);
  if(!state.selectedId||!all.some(c=>c.company_id===state.selectedId)) state.selectedId=visible[0]?.company_id||all[0]?.company_id||null;
  $("#companyRows").innerHTML=visible.map(c=>{
    const p=priority(c),[status,statusClass]=statusInfo(c),task=topTask(c);
    const score=c.opportunity_score;
    return '<tr class="'+(c.company_id===state.selectedId?"selected":"")+'" data-id="'+esc(c.company_id)+'">'+
      '<td><span class="radio">'+(c.company_id===state.selectedId?"✓":"")+'</span></td>'+
      '<td><strong>'+esc(c.legal_entity)+'</strong></td>'+
      '<td>'+esc(sectorLabel(c))+'</td>'+
      '<td>'+esc(stateAbbr[c.state]||c.state||"—")+'</td>'+
      '<td>'+(score!=null?'<div class="score-cell"><div class="score-track"><div class="score-fill" style="width:'+Math.min(100,score)+'%"></div></div><span>'+score+'</span></div>':'—')+'</td>'+
      '<td><span class="priority-badge '+priorityClass(p)+'">'+p+'</span></td>'+
      '<td>'+isoCell(c)+'</td>'+
      '<td><span class="status-badge '+statusClass+'">'+esc(status)+'</span></td>'+
      '<td><span class="confidence-badge '+confClass(c.evidence_confidence)+'">'+esc(c.evidence_confidence||"?")+'</span></td>'+
      '<td class="next-step" title="'+esc(task?.research_question||"Keine offene priorisierte Aufgabe")+'">'+esc(task?task.research_question:"—")+'</td>'+
      '<td>⋮</td>'+
    '</tr>';
  }).join("")||'<tr><td colspan="11">Keine Zielunternehmen für diesen Filter.</td></tr>';
  $("#pagerText").textContent=(all.length?start+1:0)+" - "+Math.min(start+state.pageSize,all.length)+" von "+all.length;
  $("#pageLabel").textContent="Seite "+state.page+" / "+pages;
  $("#prevPage").disabled=state.page<=1;$("#nextPage").disabled=state.page>=pages;
  $("#companyRows tr[data-id]").forEach(row=>row.addEventListener("click",()=>{state.selectedId=row.dataset.id;markRecent(row.dataset.id);renderTable();renderDetail()}));
}
function techStrength(o){
  const l=(o.opportunity_level||o.priority||"").toUpperCase();
  return l==="HIGH"?92:l==="MEDIUM"?68:l==="LOW"?42:25;
}
function renderDetail(){
  const c=state.data.companies.find(x=>x.company_id===state.selectedId);
  if(!c){$("#detailContent").innerHTML='<div class="detail-body">Kein Unternehmen ausgewählt.</div>';return}
  const [status,statusClass]=statusInfo(c),p=priority(c);
  const ops=(c.opportunities||[]).slice().sort((a,b)=>techStrength(b)-techStrength(a));
  const why=uniq(ops.map(o=>o.why_now).filter(Boolean)).slice(0,4);
  const task=topTask(c);
  const initial=(c.legal_entity||"?").trim().charAt(0).toUpperCase();
  const score=c.opportunity_score;
  const tabs='<div class="detail-tabs">'+
    [["overview","Übersicht"],["analysis","ETOI Analyse"],["research","Research"],["sources","Quellen"]].map(([id,l])=>'<button class="detail-tab '+(state.detailTab===id?"active":"")+'" data-detail-tab="'+id+'">'+l+'</button>').join("")+
    '</div>';
  let body="";
  if(state.detailTab==="overview"){
    body='<div class="detail-body">'+
      '<div class="info-grid"><div class="info-list">'+
        '<div class="info-item"><span>Branche</span><strong>'+esc(sectorLabel(c))+'</strong></div>'+
        '<div class="info-item"><span>Region</span><strong>'+esc(c.state||"—")+'</strong></div>'+
        '<div class="info-item"><span>Mitarbeiter</span><strong>'+esc(c.employees??"—")+'</strong></div>'+
        '<div class="info-item"><span>Umsatz</span><strong>'+(c.revenue_eur_m!=null?"€ "+money(c.revenue_eur_m)+" Mio.":"—")+'</strong></div>'+
        '<div class="info-item"><span>ISO 50001</span><strong>'+esc(titleCase(c.certifications?.iso_50001||"UNKNOWN"))+'</strong></div>'+
        '<div class="info-item"><span>ISO 14001</span><strong>'+esc(titleCase(c.certifications?.iso_14001||"UNKNOWN"))+'</strong></div>'+
      '</div><div class="score-box">'+
        '<div class="score-box-row"><span>ETOI Score</span><span class="score-big">'+(score!=null?score:"—")+'</span></div>'+
        '<div class="score-box-row"><span>Priorität</span><span class="priority-badge '+priorityClass(p)+'">'+p+'</span></div>'+
        '<div class="score-box-row"><span>Status</span><span class="status-badge '+statusClass+'">'+esc(status)+'</span></div>'+
        '<div class="score-box-row"><span>Confidence</span><span class="confidence-badge '+confClass(c.evidence_confidence)+'">'+esc(c.evidence_confidence||"?")+'</span></div>'+
      '</div></div>'+
      '<section class="section-card"><div class="section-card-title">Technische Relevanz</div><div class="section-card-body tech-list">'+
        (ops.length?ops.slice(0,6).map(o=>'<div class="tech-row"><span>'+esc(titleCase(o.opportunity_type))+'</span><div class="tech-track"><div class="tech-fill" style="width:'+techStrength(o)+'%"></div></div><strong>'+esc((o.opportunity_level||o.priority||"—").toUpperCase())+'</strong></div>').join(""):'Keine Opportunities')+
      '</div></section>'+
      '<div class="detail-two-col">'+
        '<section class="section-card"><div class="section-card-title">Wichtige Informationen</div><div class="section-card-body info-list">'+
          '<div class="info-item"><span>SME Status</span><strong>'+esc(titleCase(c.sme_status))+'</strong></div>'+
          '<div class="info-item"><span>Group Check</span><strong>'+esc(titleCase(c.group_check))+'</strong></div>'+
          '<div class="info-item"><span>EMAS</span><strong>'+esc(titleCase(c.certifications?.emas||"UNKNOWN"))+'</strong></div>'+
          '<div class="info-item"><span>Quellen</span><strong>'+((c.sources||[]).length)+'</strong></div>'+
        '</div></section>'+
        '<section class="section-card"><div class="section-card-title">Why Now</div><div class="section-card-body">'+
          (why.length?'<ul class="bullet-list">'+why.map(x=>'<li>'+esc(x)+'</li>').join("")+'</ul>':'<span class="action-text">Kein zusätzlicher Why-Now-Faktor dokumentiert.</span>')+
        '</div></section>'+
      '</div>'+
      '<section class="section-card"><div class="section-card-title">Nächste Maßnahme</div><div class="section-card-body next-action-box"><div class="action-icon">▤</div><div><div class="action-title">'+esc(task?titleCase(task.opportunity_type):"Keine offene Aufgabe")+'</div><div class="action-text">'+esc(task?.research_question||"Keine priorisierte Research-Aufgabe vorhanden.")+'</div></div><div class="action-meta">'+esc(task?.task_status||"")+'</div></div></section>'+
    '</div>';
  }else if(state.detailTab==="analysis"){
    body='<div class="detail-body"><section class="section-card"><div class="section-card-title">ETOI Analyse</div><div class="section-card-body tech-list">'+
      (ops.length?ops.map(o=>'<div class="tech-row"><span>'+esc(titleCase(o.opportunity_type))+'</span><div class="tech-track"><div class="tech-fill" style="width:'+techStrength(o)+'%"></div></div><strong>'+esc(o.opportunity_level||o.priority||"—")+'</strong></div>').join(""):'Keine Opportunity-Signale')+
      '</div></section><section class="section-card"><div class="section-card-title">Methodischer Status</div><div class="section-card-body action-text">'+
      (score!=null?'Für diesen Pilotfall liegt ein expliziter Opportunity Score von '+score+' ('+esc(c.opportunity_band||"") +') vor.':'Für dieses Unternehmen liegt noch kein expliziter ETOI-Gesamtscore vor. Die Oberfläche zeigt daher nur abgeleitete Opportunity-Signale und Prioritäten.')+
      '</div></section></div>';
  }else if(state.detailTab==="research"){
    body='<div class="detail-body"><section class="section-card"><div class="section-card-title">Research Queue · '+(c.research_tasks||[]).length+'</div><div class="section-card-body source-list">'+
      ((c.research_tasks||[]).length?(c.research_tasks||[]).map(t=>'<div class="source-item"><strong>#'+esc(t.research_rank??"—")+' · '+esc(titleCase(t.opportunity_type))+'</strong><div class="action-text">'+esc(t.research_question)+'</div><div class="source-meta">'+esc(t.research_priority)+' priority · '+esc(t.task_status||"OPEN")+'</div></div>').join(""):'Keine offenen Tasks')+
      '</div></section></div>';
  }else{
    body='<div class="detail-body"><section class="section-card"><div class="section-card-title">Evidence Trail · '+(c.sources||[]).length+' Quellen</div><div class="section-card-body source-list">'+
      ((c.sources||[]).length?(c.sources||[]).map(s=>'<div class="source-item"><a href="'+esc(s.final_url||"#")+'" target="_blank" rel="noopener">'+esc(s.document_title||s.publisher||s.source_id)+' ↗</a><div class="source-meta">'+esc([s.source_id,titleCase(s.source_type),s.publisher].filter(Boolean).join(" · "))+'</div></div>').join(""):'Keine Quellen im Register')+
      '</div></section></div>';
  }
  const isPinned=pinnedIds().includes(c.company_id);
  $("#detailContent").innerHTML=
    '<div class="detail-header"><div class="detail-title-row"><div class="company-icon">'+esc(initial)+'</div><div class="detail-title"><h2>'+esc(c.legal_entity)+'</h2><div class="sub">'+esc(c.company_id)+' · '+esc(sectorLabel(c))+'</div></div><button class="detail-pin" id="detailPin" title="Anheften">'+(isPinned?"★":"☆")+'</button><button class="detail-close" id="detailClose">×</button></div>'+tabs+'</div>'+body;
  $$("[data-detail-tab]").forEach(b=>b.addEventListener("click",()=>{state.detailTab=b.dataset.detailTab;renderDetail()}));
  $("#detailPin")?.addEventListener("click",()=>{const now=togglePinned(c.company_id);showToast(now?"Unternehmen angeheftet.":"Anheftung entfernt.");renderDetail()});
  $("#detailClose")?.addEventListener("click",()=>{state.selectedId=null;renderTable();renderDetail()});
}
function renderResearch(){
  const q=state.researchQuery.trim().toLowerCase();
  let tasks=state.data.companies.flatMap(c=>(c.research_tasks||[]).map(t=>({...t,company_id:c.company_id,legal_entity:c.legal_entity})));
  tasks.sort((a,b)=>(a.research_rank||9999)-(b.research_rank||9999));
  if(q) tasks=tasks.filter(t=>[t.legal_entity,t.opportunity_type,t.research_question].join(" ").toLowerCase().includes(q));
  $("#researchRows").innerHTML=tasks.map(t=>'<tr data-id="'+esc(t.company_id)+'"><td>'+esc(t.research_rank??"—")+'</td><td><strong>'+esc(t.legal_entity)+'</strong></td><td>'+esc(titleCase(t.opportunity_type))+'</td><td style="white-space:normal;min-width:420px">'+esc(t.research_question)+'</td><td>'+esc(t.research_priority)+'</td><td>'+esc(t.decision_impact)+'</td><td>'+esc(t.task_status||"OPEN")+'</td></tr>').join("");
  $$("#researchRows tr[data-id]").forEach(r=>r.addEventListener("click",()=>{state.selectedId=r.dataset.id;showCompanies();renderTable();renderDetail()}));
}
function renderFunctional(view){
  const root=$("#functionalContent");
  const title=$("#functionalTitle");
  const sub=$("#functionalSubtitle");
  const kicker=$("#functionalKicker");
  const actions=$("#functionalActions");
  const all=state.data.companies;
  kicker.textContent="SME-ETOI";
  actions.innerHTML="";

  if(view==="home"){
    title.textContent="Startseite";
    sub.textContent="Arbeitsübersicht über Zielunternehmen, offene Research-Fragen und aktuelle persönliche Arbeitslisten.";
    const tasks=all.flatMap(c=>c.research_tasks||[]);
    const recent=recentIds().map(companyById).filter(Boolean).slice(0,5);
    const top=all.slice().sort((a,b)=>priority(a).localeCompare(priority(b))||((b.opportunities||[]).length-(a.opportunities||[]).length)).slice(0,5);
    root.innerHTML=
      '<div class="functional-kpis">'+
        '<div class="functional-kpi"><span>Zielunternehmen</span><strong>'+all.length+'</strong></div>'+
        '<div class="functional-kpi"><span>Opportunity Signale</span><strong>'+all.reduce((s,c)=>s+(c.opportunities||[]).length,0)+'</strong></div>'+
        '<div class="functional-kpi"><span>Research Tasks</span><strong>'+tasks.length+'</strong></div>'+
        '<div class="functional-kpi"><span>Eligibility offen</span><strong>'+all.filter(c=>eligibility(c)==="ELIGIBILITY_PENDING").length+'</strong></div>'+
      '</div>'+
      '<div class="functional-two-col">'+
        '<section class="functional-card"><h3>Zuletzt geöffnet</h3>'+(recent.length?genericTable(["Unternehmen","Branche","Priorität"],recent.map(c=>'<tr data-company-id="'+esc(c.company_id)+'"><td><strong>'+esc(c.legal_entity)+'</strong></td><td>'+esc(sectorLabel(c))+'</td><td>'+priority(c)+'</td></tr>')):'<p class="functional-empty">Noch keine Firmen geöffnet.</p>')+'</section>'+
        '<section class="functional-card"><h3>Top Potenzial</h3>'+genericTable(["Unternehmen","Signale","Priorität"],top.map(c=>'<tr data-company-id="'+esc(c.company_id)+'"><td><strong>'+esc(c.legal_entity)+'</strong></td><td>'+(c.opportunities||[]).length+'</td><td>'+priority(c)+'</td></tr>'))+'</section>'+
      '</div>';
    bindFunctionalCompanyRows();return;
  }

  if(view==="recent"||view==="pinned"){
    const ids=view==="recent"?recentIds():pinnedIds();
    const rows=ids.map(companyById).filter(Boolean);
    title.textContent=view==="recent"?"Letzte":"Angeheftet";
    sub.textContent=view==="recent"?"Zuletzt geöffnete Unternehmen auf diesem Gerät.":"Deine lokal angehefteten Unternehmen.";
    root.innerHTML=rows.length?genericTable(["Unternehmen","Branche","Region","Priorität","Tasks"],rows.map(c=>'<tr data-company-id="'+esc(c.company_id)+'"><td><strong>'+esc(c.legal_entity)+'</strong></td><td>'+esc(sectorLabel(c))+'</td><td>'+esc(c.state||"—")+'</td><td>'+priority(c)+'</td><td>'+(c.research_tasks||[]).length+'</td></tr>')):'<div class="functional-empty">'+(view==="recent"?"Noch keine Firmen geöffnet.":"Noch keine Firmen angeheftet. Öffne eine Firma und nutze ☆ im Detailpanel.")+'</div>';
    bindFunctionalCompanyRows();return;
  }

  if(view==="tasks"){
    title.textContent="Aufgaben";
    sub.textContent="Arbeitsliste aus der Research Queue, sortiert nach Research Rank.";
    const tasks=all.flatMap(c=>(c.research_tasks||[]).map(t=>({...t,company:c}))).sort((a,b)=>(a.research_rank||9999)-(b.research_rank||9999));
    root.innerHTML=genericTable(["Rang","Unternehmen","Aufgabe","Priorität","Status"],tasks.map(t=>'<tr data-company-id="'+esc(t.company.company_id)+'"><td>'+esc(t.research_rank??"—")+'</td><td><strong>'+esc(t.company.legal_entity)+'</strong></td><td class="wrap-cell">'+esc(t.research_question)+'</td><td>'+esc(t.research_priority)+'</td><td>'+esc(t.task_status||"OPEN")+'</td></tr>'));
    bindFunctionalCompanyRows();return;
  }

  if(view==="notes"){
    title.textContent="Notizen";
    sub.textContent="Lokale Arbeitsnotizen je Unternehmen. Sie werden nur in diesem Browser gespeichert und nicht ins Repository geschrieben.";
    const notes=notesMap();
    const options=all.slice().sort((a,b)=>a.legal_entity.localeCompare(b.legal_entity)).map(c=>'<option value="'+esc(c.company_id)+'">'+esc(c.legal_entity)+'</option>').join("");
    const noted=Object.entries(notes).map(([id,text])=>({company:companyById(id),text})).filter(x=>x.company&&x.text);
    root.innerHTML=
      '<section class="functional-card note-editor"><label>Unternehmen<select id="noteCompany"><option value="">Bitte wählen…</option>'+options+'</select></label><label>Notiz<textarea id="noteText" rows="7" placeholder="Eigene Arbeitsnotiz…"></textarea></label><div class="note-actions"><button id="saveNote" class="primary-action">Notiz speichern</button><button id="deleteNote">Notiz löschen</button></div></section>'+
      '<section class="functional-card"><h3>Gespeicherte Notizen</h3><div id="savedNotes">'+(noted.length?noted.map(x=>'<article class="note-item" data-company-id="'+esc(x.company.company_id)+'"><strong>'+esc(x.company.legal_entity)+'</strong><p>'+esc(x.text)+'</p></article>').join(""):'<p class="functional-empty">Noch keine Notizen gespeichert.</p>')+'</div></section>';
    const select=$("#noteCompany"),textarea=$("#noteText");
    select.addEventListener("change",()=>{textarea.value=notesMap()[select.value]||""});
    $("#saveNote").addEventListener("click",()=>{if(!select.value){showToast("Bitte zuerst ein Unternehmen wählen.");return}const m=notesMap();m[select.value]=textarea.value.trim();storageSet("sme-etoi-notes",m);showToast("Notiz gespeichert.");renderFunctional("notes")});
    $("#deleteNote").addEventListener("click",()=>{if(!select.value)return;const m=notesMap();delete m[select.value];storageSet("sme-etoi-notes",m);showToast("Notiz gelöscht.");renderFunctional("notes")});
    $(".note-item[data-company-id]").forEach(x=>x.addEventListener("click",()=>openCompany(x.dataset.companyId)));return;
  }

  if(view==="opportunities"){
    title.textContent="Opportunities";
    sub.textContent="Alle vom Opportunity Engine abgeleiteten technischen und kommerziellen Signale.";
    const rows=all.flatMap(c=>(c.opportunities||[]).map(o=>({company:c,...o}))).sort((a,b)=>a.company.legal_entity.localeCompare(b.company.legal_entity)||a.opportunity_type.localeCompare(b.opportunity_type));
    root.innerHTML=genericTable(["Unternehmen","Technologie","Level","Commercial Status","Actionability","Confidence","Why Now"],rows.map(o=>'<tr data-company-id="'+esc(o.company.company_id)+'"><td><strong>'+esc(o.company.legal_entity)+'</strong></td><td>'+esc(titleCase(o.opportunity_type))+'</td><td>'+esc(o.opportunity_level||"—")+'</td><td>'+esc(titleCase(o.commercial_status))+'</td><td>'+esc(titleCase(o.actionability_status))+'</td><td>'+esc(o.confidence||"—")+'</td><td class="wrap-cell">'+esc(o.why_now||"—")+'</td></tr>'));
    bindFunctionalCompanyRows();return;
  }

  if(view==="analysis"){
    title.textContent="ETOI Analyse";
    sub.textContent="Unternehmenssicht auf Scores, Opportunity-Signale und Evidenz. Explizite Gesamtscores werden nur angezeigt, wenn sie tatsächlich berechnet wurden.";
    const rows=all.slice().sort((a,b)=>(b.opportunity_score??-1)-(a.opportunity_score??-1)||priority(a).localeCompare(priority(b)));
    root.innerHTML=genericTable(["Unternehmen","ETOI Score","Band","Priorität","Signale","Confidence","Eligibility"],rows.map(c=>'<tr data-company-id="'+esc(c.company_id)+'"><td><strong>'+esc(c.legal_entity)+'</strong></td><td>'+(c.opportunity_score??"—")+'</td><td>'+esc(c.opportunity_band||"—")+'</td><td>'+priority(c)+'</td><td>'+(c.opportunities||[]).length+'</td><td>'+esc(c.evidence_confidence||"—")+'</td><td>'+esc(titleCase(eligibility(c)))+'</td></tr>'));
    bindFunctionalCompanyRows();return;
  }

  if(view==="market"||view==="sectors"){
    const groups=aggregateBy(all,c=>view==="market"?sectorLabel(c):(c.nace_label||sectorLabel(c)));
    const rows=Array.from(groups.entries()).map(([name,list])=>({name,list,opps:list.reduce((s,c)=>s+(c.opportunities||[]).length,0),tasks:list.reduce((s,c)=>s+(c.research_tasks||[]).length,0),high:list.filter(c=>priority(c)==="A").length,pending:list.filter(c=>eligibility(c)==="ELIGIBILITY_PENDING").length})).sort((a,b)=>b.list.length-a.list.length);
    title.textContent=view==="market"?"Marktanalyse":"Branchen";
    sub.textContent=view==="market"?"Aggregierte Sicht nach SME-ETOI-Prozess-/Branchencluster.":"Branchenverteilung auf Basis der vorhandenen NACE-/Unternehmensdaten.";
    root.innerHTML=genericTable([view==="market"?"Cluster":"Branche","Unternehmen","High Priority","Eligibility offen","Opportunity Signale","Research Tasks"],rows.map(r=>'<tr><td><strong>'+esc(r.name)+'</strong></td><td>'+r.list.length+'</td><td>'+r.high+'</td><td>'+r.pending+'</td><td>'+r.opps+'</td><td>'+r.tasks+'</td></tr>'));return;
  }

  if(view==="regions"){
    title.textContent="Regionen";
    sub.textContent="Verteilung und Opportunity-Dichte nach Bundesland.";
    const groups=aggregateBy(all,c=>c.state||"Unbekannt");
    const rows=Array.from(groups.entries()).map(([name,list])=>({name,list,opps:list.reduce((s,c)=>s+(c.opportunities||[]).length,0),tasks:list.reduce((s,c)=>s+(c.research_tasks||[]).length,0),high:list.filter(c=>priority(c)==="A").length})).sort((a,b)=>b.list.length-a.list.length);
    root.innerHTML=genericTable(["Region","Unternehmen","High Priority","Opportunity Signale","Research Tasks"],rows.map(r=>'<tr><td><strong>'+esc(r.name)+'</strong></td><td>'+r.list.length+'</td><td>'+r.high+'</td><td>'+r.opps+'</td><td>'+r.tasks+'</td></tr>'));return;
  }

  if(view==="technologies"){
    title.textContent="Technologien";
    sub.textContent="Technologieportfolio aus den Opportunity-Engine-Ausgaben.";
    const allOpps=all.flatMap(c=>c.opportunities||[]);
    const groups=aggregateBy(allOpps,o=>o.opportunity_type);
    const rows=Array.from(groups.entries()).map(([name,list])=>({name,total:list.length,high:list.filter(o=>(o.opportunity_level||o.priority)==="HIGH").length,medium:list.filter(o=>(o.opportunity_level||o.priority)==="MEDIUM").length,research:list.filter(o=>o.commercial_status==="RESEARCH_REQUIRED").length})).sort((a,b)=>b.total-a.total);
    root.innerHTML=genericTable(["Technologie","Signale","High","Medium","Research Required"],rows.map(r=>'<tr><td><strong>'+esc(titleCase(r.name))+'</strong></td><td>'+r.total+'</td><td>'+r.high+'</td><td>'+r.medium+'</td><td>'+r.research+'</td></tr>'));return;
  }

  if(view==="methodology"){
    title.textContent="Methodik";
    sub.textContent="Die zentralen Forschungsregeln, die das SME-ETOI-System erzwingt.";
    root.innerHTML='<div class="functional-two-col">'+
      '<section class="functional-card"><h3>Technical Relevance Engine</h3><p>Bewertet, welche Energielösungen aufgrund öffentlich belegter Prozesssignale technisch relevant sind.</p></section>'+
      '<section class="functional-card"><h3>Commercial White Space</h3><p>Trennt technische Relevanz davon, was öffentlich bereits als implementiert belegt ist.</p></section>'+
      '<section class="functional-card"><h3>Research Queue</h3><p>Priorisiert fehlende Fakten nach erwartetem Entscheidungswert. SME-Eligibility-Gates stehen vor Deployment-Recherche.</p></section>'+
      '<section class="functional-card"><h3>Research Safeguard</h3><p><strong>UNKNOWN bleibt UNKNOWN.</strong> Fehlende öffentliche Evidenz ist kein Beweis für Nicht-Deployment oder White Space.</p></section>'+
      '<section class="functional-card"><h3>Human Review Gate</h3><p>Research-Ergebnisse dürfen kanonische Firmendaten nicht still überschreiben. Bestätigte Änderungen brauchen Review und Canonical Update.</p></section>'+
      '<section class="functional-card"><h3>Eligibility</h3><p>Technische Relevanz bleibt sichtbar, aber ungeklärte SME-/Gruppenstruktur blockiert die Actionability.</p></section>'+
    '</div>';return;
  }

  if(view==="documentation"){
    title.textContent="Dokumentation";
    sub.textContent="Aktueller Projektaufbau und reproduzierbare Ausführung.";
    root.innerHTML='<div class="functional-two-col">'+
      '<section class="functional-card"><h3>Pipeline</h3><pre>python src/run_pipeline.py\npython src/run_pipeline.py --check-only</pre><p>QA → Opportunity Engine → Research Queue → Output Checks → Web Snapshot</p></section>'+
      '<section class="functional-card"><h3>Web-App</h3><pre>python -m http.server 8000 --directory web</pre><p>Browser: http://localhost:8000</p></section>'+
      '<section class="functional-card"><h3>Wichtige Dateien</h3><p><code>docs/product_architecture.md</code><br><code>data/company_intelligence.csv</code><br><code>outputs/opportunities.csv</code><br><code>outputs/research_queue.csv</code></p></section>'+
      '<section class="functional-card"><h3>Current Pilot</h3><p>'+state.data.meta.company_count+' Unternehmen · '+state.data.meta.opportunity_count+' Opportunity-Zeilen · '+state.data.meta.research_task_count+' Research Tasks · '+state.data.meta.eligibility_gate_count+' Eligibility Gates</p></section>'+
    '</div>';return;
  }
}
function showFunctional(view){
  $("#analyticsBand").hidden=true;
  $(".master-detail").hidden=true;
  $("#researchPage").hidden=true;
  $("#functionalPage").hidden=false;
  setPageChrome(view==="home"?"Startseite":titleCase(view),false);
  renderFunctional(view);
}
function showNav(view){
  setActiveNav(view);
  if(view==="companies"||view==="dashboard"){
    setPageChrome(view==="dashboard"?"Dashboard":"Zielunternehmen",true);
    showCompanies();renderAll();if(view==="dashboard")$("#analyticsBand").scrollIntoView({behavior:"smooth"});return;
  }
  if(view==="research"){
    setPageChrome("Research Queue",false);showResearch();return;
  }
  showFunctional(view);
}
function renderAll(){renderMetrics();renderRegionChart();renderPriority();renderTable();renderDetail();renderResearch()}
function showCompanies(){
  $("#functionalPage").hidden=true;$("#analyticsBand").hidden=false;$(".master-detail").hidden=false;$("#researchPage").hidden=true;
}
function showResearch(){
  $("#functionalPage").hidden=true;$("#analyticsBand").hidden=true;$(".master-detail").hidden=true;$("#researchPage").hidden=false;renderResearch();
}
function exportCsv(){
  const rows=companies(), header=["company_id","legal_entity","sector","region","score","priority","confidence","status"];
  const lines=[header.join(",")].concat(rows.map(c=>{
    const [status]=statusInfo(c);
    return [c.company_id,c.legal_entity,sectorLabel(c),c.state,c.opportunity_score??"",priority(c),c.evidence_confidence,status].map(v=>'"'+String(v??"").replaceAll('"','""')+'"').join(",");
  }));
  const blob=new Blob([lines.join("\n")],{type:"text/csv;charset=utf-8"});
  const url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download="sme-etoi-zielunternehmen.csv";a.click();URL.revokeObjectURL(url);
}
function bind(){
  $("#refreshCommand").addEventListener("click",()=>location.reload());
  $("#newViewCommand").addEventListener("click",()=>{state.query="";state.focus="";state.scope="all";state.page=1;$("#tableSearch").value="";$("#globalSearch").value="";$("#focusFilter").value="";renderAll();showToast("Ansicht zurückgesetzt")});
  $("#exportCommand").addEventListener("click",exportCsv);
  $("#chartsCommand").addEventListener("click",()=>{$("#analyticsBand").scrollIntoView({behavior:"smooth"});showCompanies()});
  $("#methodCommand").addEventListener("click",()=>showToast("Methodik ist im Repository unter docs/product_architecture.md dokumentiert."));
  $("#backCommand").addEventListener("click",()=>history.back());
  $("#viewModeSelect").addEventListener("change",e=>{$("#analyticsBand").hidden=e.target.value==="table"});
  $("#focusFilter").addEventListener("change",e=>{state.focus=e.target.value;state.page=1;renderAll()});
  $("#tableSearch").addEventListener("input",e=>{state.query=e.target.value;$("#globalSearch").value=e.target.value;state.page=1;renderAll()});
  $("#globalSearch").addEventListener("input",e=>{state.query=e.target.value;$("#tableSearch").value=e.target.value;state.page=1;renderAll();showCompanies()});
  $("#prevPage").addEventListener("click",()=>{if(state.page>1){state.page--;renderTable()}});
  $("#nextPage").addEventListener("click",()=>{state.page++;renderTable()});
  $("#researchSearch").addEventListener("input",e=>{state.researchQuery=e.target.value;renderResearch()});
  $$(".tab[data-scope]").forEach(b=>b.addEventListener("click",()=>{
    $$(".tab").forEach(x=>x.classList.remove("active"));b.classList.add("active");
    state.scope=b.dataset.scope;state.page=1;
    if(state.scope==="research") showResearch(); else {showCompanies();renderAll()}
  }));
  $("[data-nav]").forEach(b=>b.addEventListener("click",()=>showNav(b.dataset.nav)));
}
async function init(){
  bind();
  try{
    const r=await fetch("data/sme_etoi.json",{cache:"no-store"});if(!r.ok)throw new Error("HTTP "+r.status);
    state.data=await r.json();
    setPageChrome("Zielunternehmen",true);renderAll();
  }catch(e){console.error(e);$("#errorState").hidden=false}
}
init();
