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
  sortMode:"name"
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
  $$("#companyRows tr[data-id]").forEach(row=>row.addEventListener("click",()=>{state.selectedId=row.dataset.id;renderTable();renderDetail()}));
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
  $("#detailContent").innerHTML=
    '<div class="detail-header"><div class="detail-title-row"><div class="company-icon">'+esc(initial)+'</div><div class="detail-title"><h2>'+esc(c.legal_entity)+'</h2><div class="sub">'+esc(c.company_id)+' · '+esc(sectorLabel(c))+'</div></div><button class="detail-close" id="detailClose">×</button></div>'+tabs+'</div>'+body;
  $$("[data-detail-tab]").forEach(b=>b.addEventListener("click",()=>{state.detailTab=b.dataset.detailTab;renderDetail()}));
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
function renderAll(){renderMetrics();renderRegionChart();renderPriority();renderTable();renderDetail();renderResearch()}
function showCompanies(){
  $("#analyticsBand").hidden=false;$(".master-detail").hidden=false;$("#researchPage").hidden=true;
}
function showResearch(){
  $("#analyticsBand").hidden=true;$(".master-detail").hidden=true;$("#researchPage").hidden=false;renderResearch();
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
  $("#methodNav").addEventListener("click",()=>showToast("Methodik ist im Repository unter docs/product_architecture.md dokumentiert."));
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
  $$("[data-nav]").forEach(b=>b.addEventListener("click",()=>{
    $$(".nav-row").forEach(x=>x.classList.remove("active"));b.classList.add("active");
    const v=b.dataset.nav;if(v==="research"){showResearch();return}
    showCompanies();if(v==="analysis"||v==="dashboard") $("#analyticsBand").scrollIntoView({behavior:"smooth"});
  }));
}
async function init(){
  bind();
  try{
    const r=await fetch("data/sme_etoi.json",{cache:"no-store"});if(!r.ok)throw new Error("HTTP "+r.status);
    state.data=await r.json();
    renderAll();
  }catch(e){console.error(e);$("#errorState").hidden=false}
}
init();
