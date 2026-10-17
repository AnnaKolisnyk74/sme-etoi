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
  viewMode:"analysis",
  activeNav:"companies"
};
const $=s=>document.querySelector(s);
const $$=s=>Array.from(document.querySelectorAll(s));

function esc(v){return String(v??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;")}
const statusLabels={CHECKED:"Geprüft",CHECKED_PROPOSALS:"Geprüft",APPROVED:"Freigegeben",UNKNOWN:"Unbekannt",NEEDS_RESEARCH:"Recherche nötig",RESEARCH_NEEDED:"Recherche nötig",RESEARCH_FIRST:"Recherche nötig",ELIGIBILITY_FIRST:"KMU-Prüfung zuerst",OPEN_GATE:"KMU-Prüfung offen",PROVISIONAL_PASS:"KMU wahrscheinlich",ELIGIBILITY_PENDING:"KMU-Prüfung offen",CONFIRMED:"KMU bestätigt",PROVISIONAL:"KMU-Bestätigung offen",ELIGIBILITY_BLOCKED:"KMU-Prüfung offen",READY_TO_CODE:"Bewertung möglich",CODE_NOW:"Bewertung möglich",AWAITING_HUMAN_REVIEW:"Freigabe offen",REVIEW_PROPOSALS:"Freigabe offen",NEEDS_NUMERIC_CODING:"Feldbelege fehlen",NOT_SCOREABLE_ELIGIBILITY:"KMU-Prüfung offen",NOT_SCOREABLE_CERTIFICATES:"Zertifikatsprüfung offen",PROVISIONAL_SCORE_ONLY:"Score-Freigabe offen",FINAL_SCORE_READY:"Score bereit",PENDING:"Offen",OPEN:"Offen",UNRESOLVED:"Offen",COMPLETE:"Abgeschlossen",MISSING:"Fehlt",NOT_STARTED:"Offen",RESEARCH_ONLY:"Recherchestand",HTTP_OK:"Abrufbar",REDIRECT_SCOPE_OK:"Abrufbar nach Weiterleitung",RECHECKED:"Inhalt nachgeprüft",CONTEXT_ONLY:"Nur Kontext / Aussage nicht bestätigt",UNAVAILABLE:"Inhalt nicht abrufbar",NOT_CHECKED:"Noch nicht geprüft"};
function titleCase(v){return statusLabels[v]||String(v||"").replaceAll("_"," ").replace(/\b\w/g,c=>c.toUpperCase())}
function proposalSummaryLabel(v){return String(v||"").replace(/\b(CHECKED|APPROVED|NEEDS_RESEARCH|AWAITING_HUMAN_REVIEW)\b/g,s=>titleCase(s))}
function n(v){return new Intl.NumberFormat("de-DE").format(v||0)}
function money(v){return v===null||v===undefined||v===""?"—":new Intl.NumberFormat("de-DE",{maximumFractionDigits:2}).format(v)}
function uniq(a){return Array.from(new Set(a.filter(Boolean)))}
function eligibility(c){return c.opportunities?.[0]?.sample_eligibility_status||(c.score_readiness?.score_status==="NOT_SCOREABLE_ELIGIBILITY"?"ELIGIBILITY_PENDING":"PROVISIONAL_PASS")}
function actionability(c){return c.opportunities?.[0]?.actionability_status||(c.score_readiness?.score_status==="NOT_SCOREABLE_ELIGIBILITY"?"ELIGIBILITY_BLOCKED":"PROVISIONAL")}

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
// Technical research priority is separate from commercial status and ETOI scores.
function priority(c){
  if(["ELIGIBILITY_PENDING","EXCLUDED"].includes(eligibility(c))) return "BLOCKED";
  const values=(c.opportunities||[])
    .filter(o=>["A","B"].includes(String(o.confidence||"").toUpperCase()))
    .map(o=>String(o.opportunity_level||"").toUpperCase());
  if(values.includes("HIGH")) return "A";
  if(values.includes("MEDIUM")) return "B";
  if(values.includes("LOW")) return "C";
  return "UNKNOWN";
}
function priorityLabel(p){return p==="UNKNOWN"?"Belege offen":p==="BLOCKED"?"KMU offen":p}
function priorityRank(c){return {A:0,B:1,C:2,UNKNOWN:3,BLOCKED:4}[priority(c)]}
function priorityClass(p){return p==="A"?"priority-a":p==="B"?"priority-b":p==="C"?"priority-c":"priority-open"}
function statusInfo(c){
  const e=eligibility(c);
  if(e==="CONFIRMED") return ["KMU bestätigt","status-qualified"];
  if(e==="ELIGIBILITY_PENDING") return ["KMU-Prüfung offen","status-review"];
  if(e==="EXCLUDED") return ["Blockiert","status-blocked"];
  return ["KMU wahrscheinlich","status-watch"];
}
function confClass(g){return {A:"conf-a",B:"conf-b",C:"conf-c"}[String(g||"").toUpperCase()]||"conf-open"}
function scoreStatusClass(c){
  const s=c.score_readiness?.score_status||"";
  if(s==="FINAL_SCORE_READY")return "status-qualified";
  if(s==="NEEDS_NUMERIC_CODING"||s==="PROVISIONAL_SCORE_ONLY")return "status-review";
  if(s.startsWith("NOT_SCOREABLE")||s==="EXCLUDED")return "status-blocked";
  return "status-watch";
}
function certificateInfo(status){
  const s=String(status||"").toUpperCase();
  if(["VALID","CURRENT","YES"].includes(s))return ["Gültig belegt","iso-yes"];
  if(s==="EXPIRED")return ["Abgelaufen","iso-no"];
  if(s==="NOT_FOUND_AFTER_CHECK")return ["Kein öffentlicher Nachweis","iso-no"];
  if(s==="CLAIM_ONLY")return ["Unternehmensangabe","iso-no"];
  if(s==="DOCUMENT_FOUND_VALIDITY_UNCLEAR")return ["Gültigkeit offen","iso-no"];
  return ["Nachweis offen","iso-no"];
}
function certificateCell(status){
  const [label,cls]=certificateInfo(status);
  return '<span class="'+cls+'">'+esc(label)+'</span>';
}
function isoCell(c){return certificateCell(c.certifications?.iso_50001)}
function fieldProgress(c){
  const rows=c.score_proposals||[];
  const checked=rows.filter(p=>p.proposal_status==="CHECKED").length;
  const approved=rows.filter(p=>p.proposal_status==="APPROVED").length;
  return {checked,approved,open:Math.max(0,15-checked-approved),assessed:rows.length};
}
function fieldProgressCell(c){
  const p=fieldProgress(c);
  return '<span class="field-check-count">Geprüft: '+p.checked+' / 15</span><span class="field-open-count">'+p.open+' offen'+(p.approved?' · '+p.approved+' freigegeben':'')+'</span>';
}
function safeLink(url,label){
  return /^https?:\/\//i.test(url||"")?'<a href="'+esc(url)+'" target="_blank" rel="noopener">'+esc(label)+' ↗</a>':esc(label);
}
function certificateDetails(c){
  return '<section class="section-card"><div class="section-card-title">Zertifikatsnachweise</div><div class="section-card-body source-list"><p>Kein öffentlicher Nachweis bedeutet keine bestätigte Aussage über das Vorhandensein eines Zertifikats.</p>'+(c.certificate_checks||[]).map(r=>'<div class="source-item"><strong>'+esc(r.standard)+'</strong> · '+certificateCell(r.certificate_status)+'<div class="source-meta">Geprüft am '+esc(r.checked_date||"—")+(r.valid_until?' · Gültig bis '+esc(r.valid_until):'')+'</div>'+(r.certificate_holder?'<div class="action-text">Inhaber: '+esc(r.certificate_holder)+'</div>':'')+(r.certificate_number?'<div class="source-meta">'+esc(r.certificate_number)+(r.issuer?' · '+esc(r.issuer):'')+'</div>':'')+'<div class="action-text">'+esc(r.notes||"")+'</div><div>'+safeLink(r.direct_certificate_url||r.certificate_index_url,r.direct_certificate_url?'Zertifikatsbeleg':'Geprüfte Quelle')+'</div></div>').join("")+'</div></section>';
}
function renderEvidenceOverview(){
  const rows=companies(), progress=rows.map(fieldProgress);
  const checked=progress.reduce((sum,p)=>sum+p.checked,0),open=progress.reduce((sum,p)=>sum+p.open,0);
  const count=key=>rows.filter(c=>["VALID","CURRENT","YES"].includes(c.certifications?.[key])).length;
  $("#evidenceOverview").innerHTML='<div><strong>'+n(checked)+' Felder · Geprüft</strong><span>'+n(open)+' Feldfragen offen · '+rows.length+' Unternehmen</span></div><div><strong>Gültig belegt: ISO 50001 '+count("iso_50001")+' · ISO 14001 '+count("iso_14001")+' · EMAS '+count("emas")+'</strong><span>Feldprüfung: '+esc(state.data.proposal_check_summary?.checked_date||"—")+' · KMU-Einstufung und finale Score-Freigabe separat</span></div>';
}
function topTask(c){return (c.research_tasks||[]).filter(t=>t.task_status!=='EVIDENCE_FOUND').slice().sort((a,b)=>(a.research_rank||9999)-(b.research_rank||9999))[0]||null}
function nextStep(c){
  const sr=c.score_readiness||{},profile=c.decision_research_profile;
  if(["ELIGIBILITY_PENDING","EXCLUDED"].includes(eligibility(c))){
    const gate=(c.score_work_tasks||[]).find(t=>t.task_status==="OPEN_GATE");
    return {kind:"eligibility",title:"KMU-Zuordnung klären",text:(profile?.workstream==="ELIGIBILITY"?profile.next_action:"")||gate?.next_action||sr.next_action||"Eigentümer- und Gruppenverhältnisse mit firmenspezifischen Belegen klären.",status:"OPEN_GATE",tab:"analysis"};
  }
  if(sr.score_status==="NOT_SCOREABLE_CERTIFICATES")return {kind:"certificate",title:"Zertifikatsprüfung abschließen",text:sr.next_action||"Zertifikatsnachweise und ihre Gültigkeit prüfen.",status:"NEEDS_RESEARCH",tab:"sources"};
  if(profile?.workstream==="IDENTITY"||profile?.outcome==="ENTITY_CONFLICT")return {kind:"identity",title:"Firmenzuordnung prüfen",text:profile.next_action||"Rechtsträger und eigene Standorte eindeutig zuordnen.",status:"NEEDS_RESEARCH",tab:"research"};
  const task=topTask(c);
  if(task)return {kind:"research",title:titleCase(task.opportunity_type),text:task.research_question,status:task.task_status||"OPEN",tab:"research"};
  const gaps=(c.score_proposals||[]).filter(p=>p.proposal_status==="NEEDS_RESEARCH");
  if(gaps.length){
    const work=(c.score_work_tasks||[]).filter(t=>t.task_status==="RESEARCH_NEEDED").slice().sort((a,b)=>(a.work_rank||999999)-(b.work_rank||999999))[0];
    return {kind:"field",title:"Feldbelege recherchieren · "+gaps.length+" offen",text:gaps[0].missing_fact||work?.next_action||sr.next_action||"Die offenen Feldbelege prüfen; UNKNOWN bleibt UNKNOWN.",status:"NEEDS_RESEARCH",tab:"analysis"};
  }
  if(sr.score_status!=="FINAL_SCORE_READY"&&(c.score_proposals||[]).some(p=>p.proposal_status==="CHECKED"))return {kind:"approval",title:"Geprüfte Vorschläge zur Übernahme prüfen",text:"Geprüfte Feldvorschläge sind getrennt von kanonischen Scores. Ihre Übernahme und die unabhängige Freigabe stehen separat aus.",status:"CHECKED_PROPOSALS",tab:"analysis"};
  if(sr.score_status&&sr.score_status!=="FINAL_SCORE_READY")return {kind:"score",title:"Offene Score-Prüfung",text:sr.next_action||sr.blocking_reasons||"Die dokumentierten Score-Voraussetzungen prüfen.",status:sr.score_status,tab:"analysis"};
  return null;
}
function nextActionCard(c,step){
  return '<section class="section-card"><div class="section-card-title">Nächste Maßnahme</div><div class="section-card-body next-action-box" data-next-action="'+esc(step?.kind||'none')+'"><div class="action-icon">▤</div><div><div class="action-title">'+esc(step?.title||"Keine weitere Maßnahme dokumentiert")+'</div><div class="action-text">'+esc(step?.text||"In den vorliegenden Arbeitslisten ist kein nächster Schritt verzeichnet. Das ist keine Bestätigung vollständiger Evidenz.")+'</div>'+(step?'<button id="nextActionCommand" class="primary-action">Prüfung öffnen</button>':'')+'</div><div class="action-meta">'+esc(titleCase(step?.status||""))+'</div></div></section>';
}
function decisionProfile(c){
  const p=c.decision_research_profile;
  if(!p)return "";
  const label={EXCLUSION_SIGNAL:"KMU-Ausschluss prüfen",ENTITY_IDENTIFIED_ASSET_SCOPE_OPEN:"Betreiber identifiziert · Anlagenzuordnung offen",PUBLIC_CONTROL_EXCEPTION_OPEN:"Öffentliche Kontrolle: Ausnahme prüfen",ENTITY_CONFLICT:"Firmenzuordnung widersprüchlich",NAME_CORRECTION_PROPOSED:"Rechtsname präzisieren",NEW_FIELD_EVIDENCE:"Neue Feldbelege gefunden",PARTIAL_EVIDENCE:"Teilweise belegt",AGGREGATION_OPEN:"Gruppenaggregation offen",FINANCIAL_AND_OWNERSHIP_OPEN:"Eigentümer und Finanzdaten offen",SOURCE_ACCESS_AND_FINANCIAL_OPEN:"Quellenzugang und Finanzdaten offen"}[p.outcome]||titleCase(p.outcome);
  const proof=(c.sources||[]).filter(s=>(p.source_ids||[]).includes(s.source_id));
  return '<section class="section-card"><div class="section-card-title">Vertiefte Firmenprüfung · '+esc(p.checked_date)+'</div><div class="section-card-body">'+
    '<strong>'+esc(label)+'</strong>'+
    (p.selection_rank?'<div class="source-meta">Auswahl '+esc(p.selection_rank)+' von '+esc(p.selection_count||10)+' · '+(p.queue_source==='SCORE_WORK_QUEUE'?'Feldarbeitsrang ':'Entscheidungsrang ')+esc(p.queue_rank)+'</div>':"")+
    (p.verified_legal_entity?'<p><strong>Aktuelles Impressum:</strong> '+esc(p.verified_legal_entity)+'</p>':"")+
    (p.followup_reason?'<p class="source-meta">Nachprüfung: '+esc(p.followup_reason)+'</p>':'')+
    '<p>'+esc(p.finding)+'</p><div class="action-text"><strong>Nächster Schritt:</strong> '+esc(p.next_action)+'</div>'+
    '<div class="source-meta">'+(proof.length?proof.map(s=>safeLink(s.source_link,s.source_id)).join(' · '):'Kein belastbarer neuer Inhaltsbeleg; Abrufgrenze dokumentiert.')+'</div>'+
    '<div class="source-meta">Belegte Feldvorschläge: Geprüft. KMU-Entscheidung und finale Score-Freigabe separat.</div></div></section>';
}
function decisionResearchOverview(){
  const r=state.data.decision_research_summary;
  if(!r?.profile_count)return "";
  const b=r.latest_batch;
  const f=r.latest_followup;
  const followup=f?.company_count?'<p>Zusätzliche Nachprüfung: '+esc(f.company_count)+' Firmen'+(f.entity_clarified_company_count?' · '+esc(f.entity_clarified_company_count)+' Betreiberzuordnung geklärt':'')+(f.field_attempt_count?' · '+esc(f.field_attempt_count)+' Feldfragen untersucht · '+esc(f.new_checked_field_count)+' zusätzlich geprüft · '+esc(f.still_unknown_field_count)+' weiterhin offen':' · keine zusätzliche Feldschließung')+'.</p>':"";
  const corrections=b?.reassessed_checked_field_count?'<p>'+esc(b.reassessed_checked_field_count)+' ältere geprüfte Vorschläge anhand neuer Quellen korrigiert; Vorher-/Nachher-Entscheidungen dokumentiert.</p>':"";
  const latest=b?'<p>Letzter Rechercheblock: '+esc(b.profile_count)+' Firmen · '+esc(b.field_attempt_count)+' offene Felder untersucht · '+esc(b.new_checked_field_count)+' zusätzlich geprüft · '+esc(b.still_unknown_field_count)+' weiterhin offen.</p>'+corrections:"";
  return '<section class="functional-card"><h3>Vertiefte Firmenprüfung · '+esc(r.checked_date)+'</h3><p>'+esc(r.technical_company_count)+' technische Firmenprofile · '+esc(r.eligibility_company_count)+' KMU-Prüfungen · '+esc(r.identity_company_count)+' Firmenzuordnungen. '+esc(r.field_attempt_count)+' offene Felder untersucht, '+esc(r.new_checked_field_count)+' zusätzlich geprüft.</p>'+latest+followup+genericTable(['Unternehmen','Prüfung','Ergebnis / nächster Schritt'],r.profiles.map(p=>'<tr data-company-id="'+esc(p.company_id)+'"><td><strong>'+esc(p.legal_entity)+'</strong></td><td>'+esc({TECHNICAL:'Technik',ELIGIBILITY:'KMU',IDENTITY:'Firmenzuordnung'}[p.workstream])+'</td><td class="wrap-cell">'+esc(p.finding)+'<div class="source-meta">'+esc(p.next_action)+'</div></td></tr>'))+'</section>';
}
function allSourceRecords(){
  return (state.data.companies||[]).flatMap(c=>(c.sources||[]).map(s=>({...s,company_id:c.company_id,legal_entity:c.legal_entity,sample_member:true}))).concat(state.data.additional_sources||[]);
}
function allCertificateRecords(){
  return (state.data.companies||[]).flatMap(c=>(c.certificate_checks||[]).map(r=>({...r,company_id:c.company_id,legal_entity:c.legal_entity,sample_member:true}))).concat(state.data.additional_certificate_checks||[]);
}
function sourceLinks(ids){
  const sources=allSourceRecords();
  return String(ids||'').split('|').map(s=>s.trim()).filter(Boolean).map(id=>{const s=sources.find(r=>r.source_id===id);return s?safeLink(s.source_link,id):esc(id)}).join(' · ')||'—';
}
function knownValue(v){return v===null||v===undefined||v===''?'UNKNOWN':String(v)}
function publicFindings(findings){
  if(!findings.length)return '<p class="functional-empty">Keine zusätzlichen Recherchebefunde dokumentiert.</p>';
  return genericTable(['Firma / Datum','Befund','Ergebnis / Status','Aussageumfang / Belege'],findings.map(r=>
    '<tr data-finding-id="'+esc(r.task_id)+'" data-company-id="'+esc(r.company_id)+'"><td><strong>'+esc(r.legal_entity)+'</strong><div class="source-meta">'+esc(r.company_id)+' · '+esc(r.checked_date)+'</div></td><td class="wrap-cell">'+esc(r.finding_summary)+'<div class="source-meta">'+esc(r.missing_fact)+'</div></td><td>'+esc(knownValue(r.resulting_value))+'<div class="source-meta">'+esc(titleCase(r.research_status))+' · '+esc(r.evidence_level)+'</div><div class="source-meta">Nächste Prüfung: '+esc(r.next_review_date||'—')+'</div></td><td class="wrap-cell">'+esc(r.search_scope)+'<div>'+sourceLinks(r.source_ids)+'</div><div class="source-meta">'+esc(r.decision_effect)+'</div></td></tr>'
  ));
}
function companyFindings(c){
  const rows=(state.data.research_findings||[]).filter(r=>r.company_id===c.company_id);
  return '<section class="section-card"><div class="section-card-title">Öffentliche Recherchebefunde · '+rows.length+'</div><div class="section-card-body"><p>Datierte Beobachtungen mit ihrem Aussageumfang; die Übernahme in Stammdaten und finale Scores erfolgt separat.</p>'+publicFindings(rows)+'</div></section>';
}
function fieldProof(p){
  const labels={CONFIRMED:'Bestätigt',CORRECTED:'Korrigiert',NEEDS_RESEARCH:'Zurückgenommen / offen',NEW_EVIDENCE:'Neuer Beleg',REASSESSED:'Erneut bewertet'};
  return '<div>'+esc(p.evidence_basis||'')+'</div>'+
    (p.missing_fact?'<div class="missing-fact"><strong>Fehlender Fakt:</strong> '+esc(p.missing_fact)+'</div>':'')+
    '<div class="source-meta">'+sourceLinks(p.evidence_source_ids)+' · '+esc(p.proposal_confidence)+'</div>'+
    ((p.check_history||[]).length?'<details class="audit-details"><summary>Prüfverlauf · '+p.check_history.length+'</summary>'+p.check_history.map(r=>'<div class="source-item"><strong>'+esc(r.checked_date)+' · '+esc(labels[r.outcome]||r.outcome)+'</strong><div>'+esc(knownValue(r.original_value))+' ('+esc(r.original_confidence||'UNKNOWN')+') → '+esc(knownValue(r.checked_value))+' ('+esc(r.checked_confidence||'UNKNOWN')+')</div><p>'+esc(r.checked_evidence_basis||r.decision_note||'')+'</p><div>'+sourceLinks(r.checked_source_ids)+'</div><div class="source-meta">Quellen-/Ankerprüfung: '+esc(r.checked_by||'—')+' · Finale Freigabe: '+esc(r.final_score_approval==='NOT_GRANTED'?'nicht erteilt':r.final_score_approval||'offen')+'</div></div>').join('')+'</details>':'');
}
function companyFacts(c){
  const fields={three_shift_operation:'Dreischichtbetrieb',pv_present:'Photovoltaik',public_load_profile_available:'Öffentliches Lastprofil',public_fossil_heat_signal:'Fossiler Wärmehinweis',refrigeration_or_compressor_signal:'Kälte / Druckluft',batch_or_refrigeration_signal:'Chargen / Kühlung',rectifier_converter_furnace_signal:'Gleichrichter / Umrichter / Ofen',multi_shift_or_batch_signal:'Mehrschicht / Chargen'};
  const deployments={heat_recovery_deployed:'Wärmerückgewinnung',energy_management_deployed:'Energiemanagement',flexibility_solution_deployed:'Lastflexibilität',thermal_storage_deployed:'Thermischer Speicher',battery_storage_deployed:'Batteriespeicher',power_quality_solution_deployed:'Power Quality',industrial_heat_electrification_deployed:'Elektrische Prozesswärme'};
  const value=v=>({YES:'Ja',NO:'Nein',UNKNOWN:'Unbekannt'}[v]||'Unbekannt');
  return '<section class="section-card"><div class="section-card-title">Energie- und Prozessstammdaten · '+esc(c.last_verified_date||'—')+'</div><div class="section-card-body"><details class="audit-details"><summary>Öffentliche Signale und Technikbestand</summary>'+genericTable(['Signal','Stammdatenwert'],Object.entries(fields).map(([k,l])=>'<tr><td>'+l+'</td><td>'+value(c.public_signals?.[k])+'</td></tr>'))+genericTable(['Technikbestand','Stammdatenwert'],Object.entries(deployments).map(([k,l])=>'<tr><td>'+l+'</td><td>'+value(c.canonical_deployments?.[k])+'</td></tr>'))+'<p>Neu recherchierte Befunde sind mit Datum im Rechercheprotokoll sichtbar.</p></details><h4>Dokumentierte Ziele</h4><p>'+esc(c.public_signals?.public_targets_summary||'Keine Angabe')+'</p><h4>Dokumentierte Investitionen</h4><p>'+esc(c.public_signals?.public_investments_summary||'Keine Angabe')+'</p>'+genericTable(['Eigener Prozess','Beleg / Aussageumfang'],(c.processes||[]).map(p=>'<tr><td>'+esc(p.process_name_raw||p.process_name)+'<div class="source-meta">'+esc(p.process_id)+' · '+esc(p.confidence)+' · '+esc(p.review_status)+'</div></td><td class="wrap-cell">'+esc(p.evidence_note||'')+'<div>'+safeLink(p.evidence_url,'Prozessbeleg')+'</div></td></tr>'))+'</div></section>';
}
function companyQA(c){
  const q=c.qa_review||{};
  if(!q.company_id)return '';
  return '<section class="section-card"><div class="section-card-title">QA-Prüfprotokoll · '+esc(q.qa_date)+'</div><div class="section-card-body"><p>'+esc(q.qa_result)+' · Unabhängige Zweitprüfung: '+esc(titleCase(q.independent_human_review_status||'UNKNOWN'))+'</p><p>'+esc(q.remaining_limitation||'Keine weitere Einschränkung dokumentiert.')+'</p><div class="source-meta">Prüfperson / Methode: '+esc(q.qa_reviewer||'—')+'</div></div></section>';
}
function sourceRecoveryDetails(c){
  const rows=(state.data.source_audit_summary?.recovery_cases||[]).filter(r=>r.company_id===c.company_id);
  if(!rows.length)return '';
  return '<section class="section-card"><div class="section-card-title">Ersatzbelege und Zugriffsgrenzen · '+rows.length+'</div><div class="section-card-body">'+rows.map(r=>'<div class="source-item">'+safeLink(r.original_url,'Originalquelle')+'<div class="source-meta">'+esc(r.checked_date)+' · '+esc(titleCase(r.resolution_status))+'</div><p>'+esc(r.supported_scope)+'</p><div>'+sourceLinks(r.replacement_source_ids)+'</div><div class="action-text"><strong>Offen:</strong> '+esc(r.remaining_gap||'—')+'</div></div>').join('')+'</div></section>';
}
function fullSourceRegister(){
  const rows=allSourceRecords();
  return '<section class="functional-card"><h3>Vollständiges Quellenregister · '+rows.length+'</h3><p>'+rows.filter(s=>s.sample_member).length+' Quellen des aktuellen Samples · '+rows.filter(s=>!s.sample_member).length+' außerhalb des Samples.</p>'+genericTable(['Firma / Umfang','Quelle','Abruf / Inhalt','Aussage / Zeitraum'],rows.map(s=>'<tr data-source-id="'+esc(s.source_id)+'" data-company-id="'+esc(s.company_id)+'"><td>'+esc(s.company_id+' · '+s.legal_entity)+'<div class="source-meta">'+(s.sample_member?'Aktuelles Sample':'Außerhalb des Samples')+'</div></td><td class="wrap-cell">'+safeLink(s.source_link,s.source_id+' · '+s.document_title)+'</td><td>'+esc(titleCase(s.retrieval_status))+'<div class="source-meta">Inhalt: '+esc(titleCase(s.content_review_status))+'</div></td><td class="wrap-cell"><details class="audit-details"><summary>Aussage und Prüfgrenzen</summary><p>'+esc(s.evidence_fact)+'</p><p>'+esc(s.content_scope_note)+'</p><p><strong>Ursprünglich registrierte Aussage:</strong> '+esc(s.registered_evidence_fact)+'</p><div class="source-meta">Zeitraum: '+esc(s.reporting_period||'offen')+' · Veröffentlichung: '+esc(s.publication_date||'nicht angegeben')+' · Inhalt geprüft: '+esc(s.content_checked_at?.slice(0,10)||'—')+'</div><div class="source-meta">Fundstelle: '+esc(s.relevant_location||'—')+' · Abruf geprüft: '+esc(s.retrieval_checked_at||'—')+' · Registerzugriff: '+esc(s.access_date||'—')+'</div></details></td></tr>'))+'</section>';
}
function fullCertificateRegister(){
  const rows=allCertificateRecords();
  return '<section class="functional-card"><h3>Vollständiges Zertifikatsregister · '+rows.length+'</h3><p>Alle dokumentierten ISO-50001-, ISO-14001- und EMAS-Prüfungen; außerhalb des Samples geführte Nachweise werden separat gekennzeichnet.</p>'+genericTable(['Firma / Standard','Status / Gültigkeit','Inhaber / Beleg'],rows.map(r=>'<tr data-certificate-key="'+esc(r.company_id+'-'+r.standard)+'" data-company-id="'+esc(r.company_id)+'"><td>'+esc(r.company_id+' · '+r.legal_entity)+'<div>'+esc(r.standard)+'</div><div class="source-meta">'+(r.sample_member?'Aktuelles Sample':'Außerhalb des Samples')+'</div></td><td>'+certificateCell(r.certificate_status)+'<div class="source-meta">'+esc(r.valid_from||'offen')+' – '+esc(r.valid_until||'offen')+'</div></td><td class="wrap-cell">'+esc(r.certificate_holder||'Inhaber nicht dokumentiert')+'<div class="source-meta">'+esc(r.certificate_number||'—')+' · '+esc(r.issuer||'—')+'</div>'+safeLink(r.direct_certificate_url||r.certificate_index_url,'Nachweis / geprüfte Quelle')+'<details class="audit-details"><summary>Prüfhinweis · '+esc(r.checked_date)+'</summary>'+esc(r.notes)+'</details></td></tr>'))+'</section>';
}

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
function syncCompanyControls(){
  $("#tableSearch").value=state.query;$("#globalSearch").value=state.query;
  $("#focusFilter").value=state.focus;
  $$(".tab[data-scope]").forEach(b=>b.classList.toggle("active",b.dataset.scope===state.scope));
}
function openCompany(id,detailTab="overview"){
  if(!companyById(id))return;
  // Cross-area links must reveal the requested company even under an old filter.
  if(!companies().some(c=>c.company_id===id)){
    state.query="";state.focus="";
    if(state.scope==="mine"&&!pinnedIds().includes(id))state.scope="all";
  }
  if(state.scope==="research")state.scope="all";
  syncCompanyControls();
  const index=companies().findIndex(c=>c.company_id===id);
  state.page=Math.floor(index/state.pageSize)+1;
  state.selectedId=id;markRecent(id);state.detailTab=detailTab;
  showNav("companies");
}
function setActiveNav(view){
  state.activeNav=view;
  $$(".nav-row").forEach(x=>x.classList.toggle("active",x.dataset.nav===view));
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
  $$("#functionalContent [data-company-id]").forEach(row=>row.addEventListener("click",event=>{if(event.target.closest("a,button,input,select,textarea,details"))return;openCompany(row.dataset.companyId)}));
}
function companies(){
  let rows=state.data.companies.slice();
  const q=state.query.trim().toLowerCase();
  if(q) rows=rows.filter(c=>[
    c.company_id,c.legal_entity,c.city,c.state,c.process_stratum,c.nace_label,
    ...(c.processes||[]).map(p=>p.process_name+" "+p.process_name_raw)
  ].join(" ").toLowerCase().includes(q));
  if(state.scope==="mine")rows=rows.filter(c=>pinnedIds().includes(c.company_id));
  if(state.focus==="pending") rows=rows.filter(c=>eligibility(c)==="ELIGIBILITY_PENDING");
  if(state.focus==="high") rows=rows.filter(c=>priority(c)==="A");
  if(state.focus==="score") rows=rows.filter(c=>c.opportunity_score!==null&&c.opportunity_score!==undefined);
  if(state.scope==="potential") rows.sort((a,b)=>priorityRank(a)-priorityRank(b)||((b.opportunity_score||-1)-(a.opportunity_score||-1))||a.legal_entity.localeCompare(b.legal_entity));
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
    ["kpiQuality","Belegqualität A/B",ab,"Qualität der öffentlichen Evidenz"],
    ["kpiReview","KMU-Prüfung offen",pending,"Gruppenverhältnisse ungeklärt"],
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
  const rows=companies(), counts={A:0,B:0,C:0,UNKNOWN:0,BLOCKED:0};
  rows.forEach(c=>counts[priority(c)]++);
  const categories=[
    ["A","High (A)","#107c10"],
    ["B","Medium (B)","#0f6cbd"],
    ["C","Low (C)","#ff8c00"],
    ["UNKNOWN","Belege offen","#c8c6c4"],
    ["BLOCKED","KMU-Prüfung offen","#605e5c"]
  ];
  let end=0;
  const stops=categories.map(([key,,color])=>{const start=end;end+=counts[key]/(rows.length||1)*100;return color+" "+start+"% "+end+"%"});
  const bg=rows.length?'conic-gradient('+stops.join(', ')+')':'#edebe9';
  $("#priorityDonut").innerHTML=
    '<div class="priority-donut" style="background:'+bg+'"><div class="priority-center"><strong>'+rows.length+'</strong><span>Zielunternehmen</span></div></div>'+
    '<div class="priority-legend">'+categories.map(([key,label,color])=>
      '<div class="priority-legend-row" data-priority="'+key+'"><span class="legend-dot" style="background:'+color+'"></span><span>'+label+'</span><strong>'+counts[key]+'</strong></div>'
    ).join('')+'</div>';
}
function renderTable(selectFirst=true){
  const all=companies(), pages=Math.max(1,Math.ceil(all.length/state.pageSize));
  if(state.page>pages) state.page=pages;
  const start=(state.page-1)*state.pageSize, visible=all.slice(start,start+state.pageSize);
  if(state.selectedId&&!visible.some(c=>c.company_id===state.selectedId))state.selectedId=null;
  if(selectFirst&&!state.selectedId)state.selectedId=visible[0]?.company_id||null;
  $("#companyRows").innerHTML=visible.map(c=>{
    const p=priority(c),[status,statusClass]=statusInfo(c),step=nextStep(c);
    const score=c.opportunity_score;
    return '<tr class="'+(c.company_id===state.selectedId?"selected":"")+'" data-id="'+esc(c.company_id)+'">'+
      '<td><span class="radio">'+(c.company_id===state.selectedId?"✓":"")+'</span></td>'+
      '<td><strong>'+esc(c.legal_entity)+'</strong></td>'+
      '<td>'+esc(sectorLabel(c))+'</td>'+
      '<td>'+esc(stateAbbr[c.state]||c.state||"—")+'</td>'+
      '<td>'+(score!=null?'<div class="score-cell"><div class="score-track"><div class="score-fill" style="width:'+Math.min(100,score)+'%"></div></div><span>'+score+'</span></div>':'—')+'</td>'+
      '<td><span class="priority-badge '+priorityClass(p)+'">'+esc(priorityLabel(p))+'</span></td>'+
      '<td>'+isoCell(c)+'</td>'+
      '<td>'+fieldProgressCell(c)+'</td>'+
      '<td><span class="status-badge '+statusClass+'">'+esc(status)+'</span></td>'+
      '<td><span class="confidence-badge '+confClass(c.evidence_confidence)+'">'+esc(c.evidence_confidence||"?")+'</span></td>'+
      '<td class="next-step" title="'+esc(step?.text||"Keine weitere Maßnahme dokumentiert")+'">'+esc(step?.title||"—")+'</td>'+
      '<td>⋮</td>'+
    '</tr>';
  }).join("")||'<tr><td colspan="12">'+(state.scope==="mine"?'Keine angehefteten Unternehmen für diesen Filter. Nutze ☆ in der Firmenansicht.':'Keine Zielunternehmen für diesen Filter.')+'</td></tr>';
  $("#pagerText").textContent=(all.length?start+1:0)+" - "+Math.min(start+state.pageSize,all.length)+" von "+all.length;
  $("#pageLabel").textContent="Seite "+state.page+" / "+pages;
  $("#prevPage").disabled=state.page<=1;$("#nextPage").disabled=state.page>=pages;
  $$("#companyRows tr[data-id]").forEach(row=>row.addEventListener("click",()=>{state.selectedId=row.dataset.id;markRecent(row.dataset.id);renderTable();renderDetail()}));
}
function technicalLevel(o){
  const level=String(o.opportunity_level||"").toUpperCase();
  return ["HIGH","MEDIUM","LOW"].includes(level)?level:"UNKNOWN";
}
function technicalRank(o){return {HIGH:3,MEDIUM:2,LOW:1,UNKNOWN:0}[technicalLevel(o)]}
function technicalSignalRow(o){
  const level=technicalLevel(o),label={HIGH:"HIGH · Hoch",MEDIUM:"MEDIUM · Mittel",LOW:"LOW · Niedrig",UNKNOWN:"Belege offen"}[level];
  return '<div class="tech-row" data-tech-level="'+level+'"><span>'+esc(titleCase(o.opportunity_type))+'</span><strong class="signal-label signal-'+level.toLowerCase()+'">'+label+'</strong><div class="signal-meta">Belegqualität: <span class="confidence-badge '+confClass(o.confidence)+'">'+esc(o.confidence||"UNKNOWN")+'</span> · Kommerzieller Status: '+esc(titleCase(o.commercial_status||"UNKNOWN"))+'</div></div>';
}
function technicalSignals(ops){
  return '<p class="signal-note">Qualitative technische Einordnung, kein Prozentwert und kein ETOI-Score. Die Firmenpriorität berücksichtigt zusätzlich Belegqualität A/B und KMU-Gates.</p>'+ (ops.length?ops.map(technicalSignalRow).join(""):'Keine technischen Signale dokumentiert; offene Feldfragen bleiben separat sichtbar.');
}
function renderDetail(){
  const c=state.data.companies.find(x=>x.company_id===state.selectedId);
  if(!c){$("#detailContent").innerHTML='<div class="detail-body">Kein Unternehmen ausgewählt.</div>';return}
  const [status,statusClass]=statusInfo(c),p=priority(c);
  const ops=(c.opportunities||[]).slice().sort((a,b)=>technicalRank(b)-technicalRank(a));
  const why=uniq(ops.map(o=>o.why_now).filter(Boolean)).slice(0,4);
  const step=nextStep(c);
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
        '<div class="info-item"><span>ISO 50001</span><strong>'+certificateCell(c.certifications?.iso_50001)+'</strong></div>'+
        '<div class="info-item"><span>ISO 14001</span><strong>'+certificateCell(c.certifications?.iso_14001)+'</strong></div>'+
      '</div><div class="score-box">'+
        '<div class="score-box-row"><span>ETOI Score</span><span class="score-big">'+(score!=null?score:"—")+'</span></div>'+
        '<div class="score-box-row"><span>Technische Priorität</span><span class="priority-badge '+priorityClass(p)+'">'+esc(priorityLabel(p))+'</span></div>'+
        '<div class="score-box-row"><span>KMU-Einstufung</span><span class="status-badge '+statusClass+'">'+esc(status)+'</span></div>'+
        '<div class="score-box-row"><span>Feldprüfung</span><span>'+fieldProgressCell(c)+'</span></div>'+
        '<div class="score-box-row"><span>Confidence</span><span class="confidence-badge '+confClass(c.evidence_confidence)+'">'+esc(c.evidence_confidence||"?")+'</span></div>'+
      '</div></div>'+
      '<section class="section-card"><div class="section-card-title">Technische Relevanz</div><div class="section-card-body tech-list">'+
        technicalSignals(ops)+
      '</div></section>'+
      '<div class="detail-two-col">'+
        '<section class="section-card"><div class="section-card-title">Wichtige Informationen</div><div class="section-card-body info-list">'+
          '<div class="info-item"><span>SME Status</span><strong>'+esc(titleCase(c.sme_status))+'</strong></div>'+
          '<div class="info-item"><span>Group Check</span><strong>'+esc(titleCase(c.group_check))+'</strong></div>'+
          '<div class="info-item"><span>EMAS</span><strong>'+certificateCell(c.certifications?.emas)+'</strong></div>'+
          '<div class="info-item"><span>Quellen</span><strong>'+((c.sources||[]).length)+'</strong></div>'+
        '</div></section>'+
        '<section class="section-card"><div class="section-card-title">Why Now</div><div class="section-card-body">'+
          (why.length?'<ul class="bullet-list">'+why.map(x=>'<li>'+esc(x)+'</li>').join("")+'</ul>':'<span class="action-text">Kein zusätzlicher Why-Now-Faktor dokumentiert.</span>')+
        '</div></section>'+
      '</div>'+
      decisionProfile(c)+certificateDetails(c)+companyFacts(c)+
      nextActionCard(c,step)+
    '</div>';
  }else if(state.detailTab==="analysis"){
    const sr=c.score_readiness||{};
    body='<div class="detail-body"><section class="section-card"><div class="section-card-title">ETOI Analyse</div><div class="section-card-body tech-list">'+
      technicalSignals(ops)+
      '</div></section>'+
      '<section class="section-card"><div class="section-card-title">Score Readiness</div><div class="section-card-body">'+
        '<div class="info-list">'+
          '<div class="info-item"><span>Score Status</span><strong>'+esc(titleCase(sr.score_status||"UNKNOWN"))+'</strong></div>'+
          '<div class="info-item"><span>Eligibility Gate</span><strong>'+esc(titleCase(sr.eligibility_gate||"UNKNOWN"))+'</strong></div>'+
          '<div class="info-item"><span>Zertifikatschecks</span><strong>'+esc(titleCase(sr.certificate_check_status||"UNKNOWN"))+'</strong></div>'+
          '<div class="info-item"><span>Numerische Codierung</span><strong>'+esc(titleCase(sr.numeric_coding_status||"UNKNOWN"))+'</strong></div>'+
          '<div class="info-item"><span>Finale Score-Freigabe</span><strong>'+esc(titleCase(sr.independent_human_review_status||"UNKNOWN"))+'</strong></div>'+
          '<div class="info-item"><span>Bestehender Score</span><strong>'+(score!=null?score+" / "+esc(c.opportunity_band||""):"—")+'</strong></div>'+
        '</div>'+
        '<div class="action-text" style="margin-top:10px"><strong>Nächster Score-Schritt:</strong> '+esc(sr.next_action||"—")+'</div>'+
        (sr.blocking_reasons?'<div class="action-text" style="margin-top:7px"><strong>Blocker:</strong> '+esc(sr.blocking_reasons)+'</div>':"")+
      '</div></section>'+
      '<section class="section-card"><div class="section-card-title">Feldprüfung</div><div class="section-card-body"><p>Geprüfte Vorschläge und offene Belegfragen. Werte sind keine freigegebenen Scores.</p>'+genericTable(["Feld","Vorschlag","Status","Beleg"],(c.score_proposals||[]).map(p=>'<tr data-score-field="'+esc(p.score_field)+'"><td>'+esc(titleCase(p.score_field))+'</td><td>'+esc(p.proposed_value??"UNKNOWN")+'</td><td>'+esc(p.proposal_status==="NEEDS_RESEARCH"?"Recherche nötig":titleCase(p.proposal_status))+'</td><td class="wrap-cell">'+fieldProof(p)+'</td></tr>'))+'</div></section>'+
      '<section class="section-card"><div class="section-card-title">Scoring Work Queue · '+(c.score_work_tasks||[]).length+'</div><div class="section-card-body source-list">'+
        ((c.score_work_tasks||[]).length?(c.score_work_tasks||[]).map(t=>
          '<div class="source-item"><strong>#'+esc(t.work_rank??"—")+' · '+esc(t.dimension?titleCase(t.dimension):titleCase(t.task_type))+'</strong><div class="action-text"><strong>Canonical missing:</strong> '+esc(t.missing_fields||"Keine offenen Felder")+'</div>'+(t.proposal_status_summary?'<div class="action-text"><strong>Proposal:</strong> '+esc(proposalSummaryLabel(t.proposal_status_summary))+'</div>':"")+(t.research_gap_fields?'<div class="action-text"><strong>Research gaps:</strong> '+esc(t.research_gap_fields)+'</div>':"")+'<div class="source-meta">'+esc(t.workstream)+' · '+esc(t.work_priority)+' · '+esc(titleCase(t.task_status))+'</div><div class="action-text">'+esc(t.next_action||"")+'</div></div>'
        ).join(""):'Keine offene Scoring-Arbeit.')+
      '</div></section>'+companyQA(c)+'</div>';
  }else if(state.detailTab==="research"){
    body='<div class="detail-body">'+decisionProfile(c)+companyFindings(c)+'<section class="section-card"><div class="section-card-title">Research Queue · '+(c.research_tasks||[]).length+'</div><div class="section-card-body source-list">'+
      ((c.research_tasks||[]).length?(c.research_tasks||[]).map(t=>'<div class="source-item"><strong>#'+esc(t.research_rank??"—")+' · '+esc(titleCase(t.opportunity_type))+'</strong><div class="action-text">'+esc(t.research_question)+'</div>'+(t.last_finding?'<p>'+esc(t.last_finding)+'</p>':"")+'<div class="source-meta">'+esc(t.research_priority)+' priority · '+esc(t.task_status==='EVIDENCE_FOUND'?'Beleg gefunden':titleCase(t.task_status||"OPEN"))+'</div></div>').join(""):'Keine offenen Tasks')+
      '</div></section></div>';
  }else{
    body='<div class="detail-body"><section class="section-card"><div class="section-card-title">Evidence Trail · '+(c.sources||[]).length+' Quellen</div><div class="section-card-body source-list">'+
      '<p>Abrufprüfung und inhaltliche Nachprüfung sind getrennt dokumentiert. Erreichbarkeit allein bestätigt keine Aussage oder Zertifikatsgültigkeit.</p>'+
      ((c.sources||[]).length?(c.sources||[]).map(s=>'<div class="source-item">'+safeLink(s.final_url,s.document_title||s.publisher||s.source_id)+'<div class="source-meta">'+esc([s.source_id,titleCase(s.source_type),s.publisher].filter(Boolean).join(" · "))+'</div><div class="source-meta">Abruf: '+esc(titleCase(s.retrieval_status||"NOT_CHECKED"))+' · '+esc(s.link_check_date||"—")+'</div><div class="source-meta">Inhaltsprüfung: '+esc(titleCase(s.content_review_status||"NOT_CHECKED"))+(s.content_checked_at?' · '+esc(s.content_checked_at.slice(0,10)):'')+'</div><div class="action-text">'+esc(s.evidence_fact||"")+'</div>'+(s.content_scope_note?'<div class="source-meta">Aussageumfang: '+esc(s.content_scope_note)+'</div>':'')+'</div>').join(""):'Keine Quellen im Register')+
      '</div></section>'+sourceRecoveryDetails(c)+'</div>';
  }
  const isPinned=pinnedIds().includes(c.company_id);
  $("#detailContent").innerHTML=
    '<div class="detail-header"><div class="detail-title-row"><div class="company-icon">'+esc(initial)+'</div><div class="detail-title"><h2>'+esc(c.legal_entity)+'</h2><div class="sub">'+esc(c.company_id)+' · '+esc(sectorLabel(c))+'</div></div><button class="detail-pin" id="detailPin" title="Anheften">'+(isPinned?"★":"☆")+'</button><button class="detail-close" id="detailClose">×</button></div>'+tabs+'</div>'+body;
  $$("[data-detail-tab]").forEach(b=>b.addEventListener("click",()=>{state.detailTab=b.dataset.detailTab;renderDetail()}));
  $("#nextActionCommand")?.addEventListener("click",()=>{if(step){state.detailTab=step.tab;renderDetail()}});
  $("#detailPin")?.addEventListener("click",()=>{const now=togglePinned(c.company_id);showToast(now?"Unternehmen angeheftet.":"Anheftung entfernt.");if(state.scope==="mine")renderAll();else renderDetail()});
  $("#detailClose")?.addEventListener("click",()=>{state.selectedId=null;renderTable(false);renderDetail()});
}
function researchMatches(r,q){
  return !q||[r.company_id,r.legal_entity,r.opportunity_type,r.research_question,r.missing_fact,r.finding_summary,r.source_ids,r.task_status,r.research_status,r.resulting_value].join(" ").toLowerCase().includes(q);
}
function renderResearch(){
  const q=state.researchQuery.trim().toLowerCase();
  let tasks=state.data.companies.flatMap(c=>(c.research_tasks||[]).map(t=>({...t,company_id:c.company_id,legal_entity:c.legal_entity})));
  tasks.sort((a,b)=>(a.research_rank||9999)-(b.research_rank||9999));
  if(q) tasks=tasks.filter(t=>researchMatches(t,q));
  $("#researchRows").innerHTML=tasks.map(t=>'<tr data-id="'+esc(t.company_id)+'"><td>'+esc(t.research_rank??"—")+'</td><td><strong>'+esc(t.legal_entity)+'</strong></td><td>'+esc(titleCase(t.opportunity_type))+'</td><td style="white-space:normal;min-width:420px">'+esc(t.research_question)+'</td><td>'+esc(t.research_priority)+'</td><td>'+esc(t.decision_impact)+'</td><td>'+esc(titleCase(t.task_status||"OPEN"))+'</td></tr>').join("");
  if(!tasks.length)$("#researchRows").innerHTML='<tr><td colspan="7">Keine Rechercheaufgaben für diese Suche.</td></tr>';
  const found=(state.data.research_findings||[]).filter(r=>researchMatches(r,q));
  $("#researchFindings").innerHTML='<section class="functional-card"><h3>Recherchebefund-Protokoll · '+found.length+'</h3><p>Alle datierten Befunde, einschließlich Einträgen ohne eigene Queue-Aufgabe. '+found.filter(r=>r.resulting_value==='YES').length+' dokumentierte YES-Befunde im aktuellen Suchumfang. Stammdaten und finale Freigaben bleiben separat.</p>'+publicFindings(found)+'</section>';
  $$("#researchRows tr[data-id]").forEach(r=>r.addEventListener("click",()=>openCompany(r.dataset.id,"research")));
  $$("#researchFindings [data-company-id]").forEach(r=>r.addEventListener("click",event=>{if(event.target.closest("a,button,input,select,textarea,details"))return;openCompany(r.dataset.companyId,"research")}));
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

  if(view==="sources"){
    title.textContent="Quellenprüfung";
    sub.textContent="Abrufprüfung aller 100 Firmen und dokumentierte Inhaltsprüfungen. Ersatzbelege gelten nur im belegten Aussageumfang.";
    const audit=state.data.source_audit_summary||{};
    const cases=audit.recovery_cases||[];
    const content=state.data.source_content_review_summary||{};
    root.innerHTML='<section class="functional-card"><h3>Inhaltsprüfung des Quellenbestands</h3><p>'+esc(content.assessed_source_count??0)+' / '+esc(content.registered_source_count??0)+' registrierte Quellen eingestuft · '+esc(content.rechecked_source_count??0)+' im dokumentierten Umfang nachgeprüft · '+esc(content.context_only_source_count??0)+' nur Kontext · '+esc(content.unavailable_source_count??0)+' nicht abrufbar · '+esc(content.missing_source_count??0)+' ohne Inhaltsprüfung</p><p>Der Durchgang umfasst auch ausgeschlossene Kandidaten. Geprüft wurde jeweils die dokumentierte Aussage oder der relevante Abschnitt. Eine Einstufung als Kontext oder nicht abrufbar bestätigt die ursprüngliche Aussage nicht. Offene Feldfragen und persönliche Freigabe bleiben separat.</p></section>'+
      '<section class="functional-card"><h3>Öffentliche Quellen · Abrufprüfung</h3><p>'+esc(audit.checked_company_count??0)+' / '+esc(audit.sample_company_count??0)+' Sample-Firmen geprüft · '+esc(audit.retrievable_url_count??0)+' / '+esc(audit.audited_url_count??0)+' URLs abrufbar · Stand '+esc(audit.last_checked_at||"—")+'</p><p>Die URL-Zahlen enthalten auch ausgeschlossene Kandidaten, Weiterleitungsziele und Ersatzbelege. HTTP 200 bestätigt keine Unternehmenszuordnung, aktuelle Zertifikatsgültigkeit oder Human Review. UNKNOWN bleibt UNKNOWN.</p></section>'+
      '<section class="functional-card"><h3>Inhaltliche Grenzen im Quellenbestand</h3>'+genericTable(["Firma","Quelle","Inhaltsprüfung","Aussagegrenze"],(content.boundary_sources||[]).map(r=>'<tr data-company-id="'+esc(r.company_id)+'"><td>'+esc(r.company_id)+'</td><td class="wrap-cell">'+safeLink(r.source_url,r.source_id+' · '+r.document_title)+'</td><td>'+esc(titleCase(r.content_review_status))+'</td><td class="wrap-cell">'+esc(r.scope_note||"—")+'</td></tr>'))+'</section>'+
      '<section class="functional-card"><h3>Ersatzbelege und offene Aussagegrenzen</h3>'+genericTable(["Firma","Originalquelle","Ergebnis","Ersatz-/Kontext-IDs","Belegter Umfang","Offene Lücke"],cases.map(r=>'<tr data-company-id="'+esc(r.company_id)+'"><td>'+esc(r.company_id)+'</td><td class="wrap-cell">'+safeLink(r.original_url,r.original_url)+'</td><td>'+esc(titleCase(r.resolution_status))+'</td><td>'+sourceLinks(r.replacement_source_ids)+'</td><td class="wrap-cell">'+esc(r.supported_scope)+'</td><td class="wrap-cell">'+esc(r.remaining_gap||"—")+'</td></tr>'))+'</section>'+
      '<section class="functional-card"><h3>Prüfabdeckung aller Sample-Firmen</h3>'+genericTable(["Firma","Coding bereits begonnen","Geprüfte URLs","Abrufbar","Abrufprobleme","Offene Beleggrenzen"],(audit.companies||[]).map(r=>'<tr data-company-id="'+esc(r.company_id)+'"><td><strong>'+esc(r.company_id)+' · '+esc(r.legal_entity)+'</strong></td><td>'+esc(r.has_coding_assessment==="YES"?"Ja":"Nein")+'</td><td>'+esc(r.audited_url_count)+'</td><td>'+esc(r.retrievable_url_count)+'</td><td>'+esc(r.retrieval_issue_count)+'</td><td>'+esc(r.scope_gap_count)+'</td></tr>'))+'</section>';
    root.innerHTML+=fullSourceRegister()+fullCertificateRegister();
    bindFunctionalCompanyRows();return;
  }

  if(view==="home"){
    title.textContent="Startseite";
    sub.textContent="Arbeitsübersicht über Zielunternehmen, offene Research-Fragen und aktuelle persönliche Arbeitslisten.";
    const tasks=all.flatMap(c=>c.research_tasks||[]);
    const recent=recentIds().map(companyById).filter(Boolean).slice(0,5);
    const top=all.slice().sort((a,b)=>priorityRank(a)-priorityRank(b)||((b.opportunities||[]).length-(a.opportunities||[]).length)).slice(0,5);
    root.innerHTML=
      '<div class="functional-kpis">'+
        '<div class="functional-kpi"><span>Zielunternehmen</span><strong>'+all.length+'</strong></div>'+
        '<div class="functional-kpi"><span>Opportunity Signale</span><strong>'+all.reduce((s,c)=>s+(c.opportunities||[]).length,0)+'</strong></div>'+
        '<div class="functional-kpi"><span>Research Tasks</span><strong>'+tasks.length+'</strong></div>'+
        '<div class="functional-kpi"><span>Eligibility offen</span><strong>'+all.filter(c=>eligibility(c)==="ELIGIBILITY_PENDING").length+'</strong></div>'+
      '</div>'+
      '<div class="functional-two-col">'+
        '<section class="functional-card"><h3>Zuletzt geöffnet</h3>'+(recent.length?genericTable(["Unternehmen","Branche","Technische Priorität"],recent.map(c=>'<tr data-company-id="'+esc(c.company_id)+'"><td><strong>'+esc(c.legal_entity)+'</strong></td><td>'+esc(sectorLabel(c))+'</td><td>'+esc(priorityLabel(priority(c)))+'</td></tr>')):'<p class="functional-empty">Noch keine Firmen geöffnet.</p>')+'</section>'+
        '<section class="functional-card"><h3>Top Potenzial</h3>'+genericTable(["Unternehmen","Signale","Technische Priorität"],top.map(c=>'<tr data-company-id="'+esc(c.company_id)+'"><td><strong>'+esc(c.legal_entity)+'</strong></td><td>'+(c.opportunities||[]).length+'</td><td>'+esc(priorityLabel(priority(c)))+'</td></tr>'))+'</section>'+
      '</div>';
    bindFunctionalCompanyRows();return;
  }

  if(view==="recent"||view==="pinned"){
    const ids=view==="recent"?recentIds():pinnedIds();
    const rows=ids.map(companyById).filter(Boolean);
    title.textContent=view==="recent"?"Letzte":"Angeheftet";
    sub.textContent=view==="recent"?"Zuletzt geöffnete Unternehmen auf diesem Gerät.":"Deine lokal angehefteten Unternehmen.";
    root.innerHTML=rows.length?genericTable(["Unternehmen","Branche","Region","Technische Priorität","Tasks"],rows.map(c=>'<tr data-company-id="'+esc(c.company_id)+'"><td><strong>'+esc(c.legal_entity)+'</strong></td><td>'+esc(sectorLabel(c))+'</td><td>'+esc(c.state||"—")+'</td><td>'+esc(priorityLabel(priority(c)))+'</td><td>'+(c.research_tasks||[]).length+'</td></tr>')):'<div class="functional-empty">'+(view==="recent"?"Noch keine Firmen geöffnet.":"Noch keine Firmen angeheftet. Öffne eine Firma und nutze ☆ im Detailpanel.")+'</div>';
    bindFunctionalCompanyRows();return;
  }

  if(view==="tasks"){
    title.textContent="Aufgaben";
    sub.textContent="Arbeitsliste aus der Research Queue, sortiert nach Research Rank.";
    const tasks=all.flatMap(c=>(c.research_tasks||[]).map(t=>({...t,company:c}))).sort((a,b)=>(a.research_rank||9999)-(b.research_rank||9999));
    root.innerHTML=genericTable(["Rang","Unternehmen","Aufgabe","Priorität","Status"],tasks.map(t=>'<tr data-company-id="'+esc(t.company.company_id)+'"><td>'+esc(t.research_rank??"—")+'</td><td><strong>'+esc(t.company.legal_entity)+'</strong></td><td class="wrap-cell">'+esc(t.research_question)+'</td><td>'+esc(t.research_priority)+'</td><td>'+esc(titleCase(t.task_status||"OPEN"))+'</td></tr>'));
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
    $$(".note-item[data-company-id]").forEach(x=>x.addEventListener("click",()=>openCompany(x.dataset.companyId)));return;
  }

  if(view==="opportunities"){
    title.textContent="Opportunities";
    sub.textContent="Alle vom Opportunity Engine abgeleiteten technischen und kommerziellen Signale.";
    const rows=all.flatMap(c=>(c.opportunities||[]).map(o=>({company:c,...o}))).sort((a,b)=>a.company.legal_entity.localeCompare(b.company.legal_entity)||a.opportunity_type.localeCompare(b.opportunity_type));
    root.innerHTML=genericTable(["Unternehmen","Technologie","Level","Commercial Status","Actionability","Confidence","Begründung / nächster Schritt"],rows.map(o=>'<tr data-company-id="'+esc(o.company.company_id)+'"><td><strong>'+esc(o.company.legal_entity)+'</strong></td><td>'+esc(titleCase(o.opportunity_type))+'</td><td>'+esc(o.opportunity_level||"—")+'</td><td>'+esc(titleCase(o.commercial_status))+'</td><td>'+esc(titleCase(o.actionability_status))+'</td><td>'+esc(o.confidence||"—")+'</td><td class="wrap-cell">'+esc(o.why_now||"—")+'<div class="action-text"><strong>Nächster Schritt:</strong> '+esc(o.next_action||"—")+'</div><div class="source-meta">Regel: '+esc(o.rule_id||"—")+'</div></td></tr>'));
    bindFunctionalCompanyRows();return;
  }

  if(view==="analysis"){
    title.textContent="ETOI Analyse";
    sub.textContent="Scoring-Arbeitsliste nach Methodik v0.2. Eligibility-Gates stehen vor numerischer Codierung; fehlende Werte werden nie automatisch aus generischen Prozessannahmen erzeugt.";
    const rows=all.slice().sort((a,b)=>{
      const order={"NOT_SCOREABLE_ELIGIBILITY":0,"NOT_SCOREABLE_CERTIFICATES":1,"NEEDS_NUMERIC_CODING":2,"PROVISIONAL_SCORE_ONLY":3,"FINAL_SCORE_READY":4};
      return (order[a.score_readiness?.score_status]??9)-(order[b.score_readiness?.score_status]??9)||a.legal_entity.localeCompare(b.legal_entity);
    });
    const work=all.flatMap(c=>(c.score_work_tasks||[]).map(t=>({...t,company:c}))).sort((a,b)=>(a.work_rank||999999)-(b.work_rank||999999));
    const summary=state.data.score_readiness_summary||{};
    const workSummary=state.data.score_work_summary||{};
    const companyWorkSummary=state.data.company_work_summary||{};
    const workflowCounts=companyWorkSummary.workflow_action_counts||{};
    const nextBest=companyWorkSummary.next_best_company||{};
    const codingCompanies=all.filter(c=>c.workflow_priority?.workflow_action==="CODE_NOW").sort((a,b)=>(a.workflow_priority?.coding_rank||9999)-(b.workflow_priority?.coding_rank||9999));
    const batches=state.data.coding_batches||[];
    const latestBatch=batches.length?batches[batches.length-1]:null;
    const batchCard=latestBatch?'<section class="functional-card"><h3>Zuletzt ausgewählter Coding-Batch · '+esc(latestBatch.batch_id)+'</h3><p>Auswahl vom '+esc(latestBatch.selected_date)+'. Die Auswahl bleibt festgehalten; Feldstatus und Workflow zeigen den aktuellen Stand. Feldzahlen sind keine SME-ETOI Scores.</p>'+genericTable(["Auswahlrang","Unternehmen","Geprüft","Recherchelücken","Workflow jetzt"],latestBatch.companies.map(c=>'<tr data-company-id="'+esc(c.company_id)+'"><td>'+esc(c.selection_rank)+'</td><td><strong>'+esc(c.legal_entity)+'</strong></td><td>'+esc(c.checked_fields??0)+'</td><td>'+esc(c.needs_research_fields)+'</td><td>'+esc(titleCase(c.current_workflow_action))+'</td></tr>'))+'</section>':"";
    const assessment=state.data.field_assessment_summary||{};
    const gateSelections=state.data.eligibility_coding_selections||[];
    const assessmentById=new Map((assessment.companies||[]).map(c=>[c.company_id,c]));
    const coverageCard='<section class="functional-card field-assessment-card"><h3>Dokumentierte Erstbewertung · '+esc(assessment.complete_company_count??0)+' / '+esc(assessment.company_count??all.length)+' Unternehmen</h3><p><strong>'+esc(assessment.assessed_field_count??0)+' / '+esc(assessment.expected_field_count??0)+' Felder bewertet</strong> · '+esc(assessment.checked_fields??0)+' Zahlenvorschläge · Geprüft · '+esc(assessment.needs_research_fields??0)+' dokumentierte Recherchelücken. Erstbewertung ist keine Score-Freigabe; UNKNOWN bleibt erhalten.</p><p>'+esc(assessment.eligibility_gate_company_count??0)+' Unternehmen haben weiterhin eine offene Eligibility-Prüfung.</p></section>';
    const gateCard=gateSelections.length?'<section class="functional-card eligibility-assessment-card"><h3>Dokumentarische Bewertung bei offener Eligibility · '+gateSelections.length+' Unternehmen</h3><p>Separat vor der Recherche ausgewählt. Die Konzernprüfung bleibt offen; kanonische Scores bleiben gesperrt.</p>'+genericTable(["Unternehmen","Bewertete Felder","Geprüft","Recherchelücken","KMU-Einstufung"],gateSelections.map(c=>{const a=assessmentById.get(c.company_id)||{};return '<tr data-company-id="'+esc(c.company_id)+'"><td><strong>'+esc(c.legal_entity)+'</strong></td><td>'+esc(a.assessed_field_count??0)+' / 15</td><td>'+esc(a.checked_fields??0)+'</td><td>'+esc(a.needs_research_fields??0)+'</td><td>'+esc(c.eligibility_gate_fields)+'</td></tr>';}))+'</section>':"";
    const humanDone=all.filter(c=>["APPROVED","COMPLETE","COMPLETED","REVIEWED","DONE"].includes(c.score_readiness?.independent_human_review_status)).length;
    root.innerHTML=
      '<div class="functional-kpis">'+
        '<div class="functional-kpi"><span>Code now</span><strong>'+(workflowCounts.CODE_NOW||0)+'</strong></div>'+
        '<div class="functional-kpi"><span>Research first</span><strong>'+(workflowCounts.RESEARCH_FIRST||0)+'</strong></div>'+
        '<div class="functional-kpi"><span>Geprüft</span><strong>'+(assessment.checked_fields||0)+'</strong></div>'+
        '<div class="functional-kpi"><span>Eligibility first</span><strong>'+(workflowCounts.ELIGIBILITY_FIRST||0)+'</strong></div>'+
      '</div>'+
      (nextBest.company_id?'<section class="functional-card next-best-card" data-company-id="'+esc(nextBest.company_id)+'"><div class="secondary-kicker">Next Best Company to Code</div><h3>#'+esc(nextBest.coding_rank||1)+' · '+esc(nextBest.legal_entity)+'</h3><div class="next-best-grid"><span><strong>'+esc(nextBest.company_id)+'</strong><small>Company ID</small></span><span><strong>'+esc(nextBest.work_priority||"—")+'</strong><small>Work Priority</small></span><span><strong>'+esc(nextBest.evidence_confidence||"—")+'</strong><small>Evidence</small></span><span><strong>'+esc(nextBest.process_confidence||"—")+'</strong><small>Process</small></span><span><strong>'+esc(nextBest.verified_source_count??"—")+'</strong><small>Verifizierte URLs</small></span><span><strong>'+esc(nextBest.qa_result||"—")+'</strong><small>QA</small></span><span><strong>'+esc(titleCase(nextBest.expected_information_gain||"UNKNOWN"))+'</strong><small>Informationsgewinn (Proxy)</small></span></div><p>'+esc(nextBest.priority_reason||"")+'</p><div class="action-text">'+esc(nextBest.next_action||"")+'</div></section>':"")+
      (codingCompanies.length?'<section class="functional-card"><h3>Next Best Coding Companies</h3>'+
        genericTable(["Coding Rank","Unternehmen","Priority","Evidence","Process","QA","Informationsgewinn (Proxy)","Quellenabdeckung","Verifizierte URLs"],codingCompanies.slice(0,10).map(c=>'<tr data-company-id="'+esc(c.company_id)+'"><td>'+esc(c.workflow_priority?.coding_rank??"—")+'</td><td><strong>'+esc(c.legal_entity)+'</strong></td><td>'+esc(c.workflow_priority?.work_priority||"—")+'</td><td>'+esc(c.evidence_confidence||"—")+'</td><td>'+esc(c.workflow_priority?.process_confidence||"—")+'</td><td>'+esc(c.workflow_priority?.qa_result||"—")+'</td><td>'+esc(titleCase(c.workflow_priority?.expected_information_gain||"UNKNOWN"))+'</td><td class="wrap-cell">'+esc(c.workflow_priority?.source_coverage||"—")+'</td><td>'+esc(c.workflow_priority?.verified_source_count??"—")+'</td></tr>'))+
      '</section>':'<section class="functional-card"><h3>Erstbewertung abgeschlossen</h3><p>Keine weiteren Unternehmen für den ersten Coding-Durchlauf. Als Nächstes folgen die dokumentierten Recherchelücken, KMU-Prüfungen und die finale Score-Freigabe.</p></section>')+
      coverageCard+decisionResearchOverview()+batchCard+gateCard+
      '<section class="functional-card"><h3>Scoring Work Queue · '+work.length+' Arbeitspakete</h3>'+
        genericTable(["Rang","Unternehmen","Workstream","Dimension","Status","Priorität","Proposal / Research","Offene Felder","Nächste Aktion"],work.map(t=>
          '<tr data-company-id="'+esc(t.company.company_id)+'"><td>'+esc(t.work_rank??"—")+'</td><td><strong>'+esc(t.company.legal_entity)+'</strong></td><td>'+esc(titleCase(t.workstream))+'</td><td>'+esc(t.dimension?titleCase(t.dimension):titleCase(t.task_type))+'</td><td><span class="status-badge '+(t.task_status==="RESEARCH_NEEDED"?"status-blocked":t.task_status==="AWAITING_HUMAN_REVIEW"?"status-review":["CHECKED","READY_TO_CODE"].includes(t.task_status)?"status-qualified":"status-watch")+'">'+esc(titleCase(t.task_status||"UNKNOWN"))+'</span></td><td>'+esc(t.work_priority||"—")+'</td><td class="wrap-cell">'+esc(t.research_gap_fields||proposalSummaryLabel(t.proposal_status_summary)||t.proposal_covered_fields||"—")+'</td><td class="wrap-cell">'+esc(t.missing_fields||"—")+'</td><td class="wrap-cell">'+esc(t.next_action||"—")+'</td></tr>'
        ))+
      '</section>'+
      '<section class="functional-card"><h3>Score Readiness nach Unternehmen</h3>'+
        genericTable(["Unternehmen","ETOI Score","Band","Score Status","Nächster Score-Schritt","Signale","Confidence","Eligibility"],rows.map(c=>{
          const sr=c.score_readiness||{};
          return '<tr data-company-id="'+esc(c.company_id)+'"><td><strong>'+esc(c.legal_entity)+'</strong></td><td>'+(c.opportunity_score??"—")+'</td><td>'+esc(c.opportunity_band||"—")+'</td><td><span class="status-badge '+scoreStatusClass(c)+'">'+esc(titleCase(sr.score_status||"UNKNOWN"))+'</span></td><td class="wrap-cell">'+esc(sr.next_action||"—")+'</td><td>'+(c.opportunities||[]).length+'</td><td>'+esc(c.evidence_confidence||"—")+'</td><td>'+esc(titleCase(eligibility(c)))+'</td></tr>';
        }))+
      '</section>'+
      '<div class="functional-card"><strong>Finale Score-Freigabe abgeschlossen:</strong> '+humanDone+' / '+all.length+'</div>';
    bindFunctionalCompanyRows();return;
  }

  if(view==="market"||view==="sectors"){
    const groups=aggregateBy(all,c=>view==="market"?sectorLabel(c):(c.nace_label||sectorLabel(c)));
    const rows=Array.from(groups.entries()).map(([name,list])=>({name,list,opps:list.reduce((s,c)=>s+(c.opportunities||[]).length,0),tasks:list.reduce((s,c)=>s+(c.research_tasks||[]).length,0),high:list.filter(c=>priority(c)==="A").length,pending:list.filter(c=>eligibility(c)==="ELIGIBILITY_PENDING").length})).sort((a,b)=>b.list.length-a.list.length);
    title.textContent=view==="market"?"Marktanalyse":"Branchen";
    sub.textContent=view==="market"?"Aggregierte Sicht nach SME-ETOI-Prozess-/Branchencluster.":"Branchenverteilung auf Basis der vorhandenen NACE-/Unternehmensdaten.";
    root.innerHTML=genericTable([view==="market"?"Cluster":"Branche","Unternehmen","Technisch A","Eligibility offen","Opportunity Signale","Research Tasks"],rows.map(r=>'<tr><td><strong>'+esc(r.name)+'</strong></td><td>'+r.list.length+'</td><td>'+r.high+'</td><td>'+r.pending+'</td><td>'+r.opps+'</td><td>'+r.tasks+'</td></tr>'));return;
  }

  if(view==="regions"){
    title.textContent="Regionen";
    sub.textContent="Verteilung und Opportunity-Dichte nach Bundesland.";
    const groups=aggregateBy(all,c=>c.state||"Unbekannt");
    const rows=Array.from(groups.entries()).map(([name,list])=>({name,list,opps:list.reduce((s,c)=>s+(c.opportunities||[]).length,0),tasks:list.reduce((s,c)=>s+(c.research_tasks||[]).length,0),high:list.filter(c=>priority(c)==="A").length})).sort((a,b)=>b.list.length-a.list.length);
    root.innerHTML=genericTable(["Region","Unternehmen","Technisch A","Opportunity Signale","Research Tasks"],rows.map(r=>'<tr><td><strong>'+esc(r.name)+'</strong></td><td>'+r.list.length+'</td><td>'+r.high+'</td><td>'+r.opps+'</td><td>'+r.tasks+'</td></tr>'));return;
  }

  if(view==="technologies"){
    title.textContent="Technologien";
    sub.textContent="Technologieportfolio aus den Opportunity-Engine-Ausgaben.";
    const allOpps=all.flatMap(c=>c.opportunities||[]);
    const groups=aggregateBy(allOpps,o=>o.opportunity_type);
    const rows=Array.from(groups.entries()).map(([name,list])=>({name,total:list.length,high:list.filter(o=>(o.opportunity_level||o.priority)==="HIGH").length,medium:list.filter(o=>(o.opportunity_level||o.priority)==="MEDIUM").length,research:list.filter(o=>o.commercial_status==="RESEARCH_REQUIRED").length})).sort((a,b)=>b.total-a.total);
    root.innerHTML=genericTable(["Technologie","Signale","High","Medium","Research Required"],rows.map(r=>'<tr><td><strong>'+esc(titleCase(r.name))+'</strong></td><td>'+r.total+'</td><td>'+r.high+'</td><td>'+r.medium+'</td><td>'+r.research+'</td></tr>'))+
      '<section class="functional-card"><h3>Technologiebibliothek · '+(state.data.reference_libraries?.technologies||[]).length+'</h3><p>Generische Referenzprofile. Ein Prozessfit ist kein Nachweis einer Anlage oder ihrer Wirtschaftlichkeit bei einer Firma; der dokumentierte Prüfstatus gilt je Profil.</p>'+genericTable(['Technologie / Status','Prozessfit / Signale','Standort- und Wirtschaftlichkeitsbedarf','Referenz'],(state.data.reference_libraries?.technologies||[]).map(t=>'<tr data-technology-id="'+esc(t.technology_id)+'"><td>'+esc(t.technology_name)+'<div class="source-meta">'+esc(t.technology_family)+' · '+esc(t.review_status)+' · Confidence-Cap '+esc(t.default_confidence_cap)+'</div></td><td class="wrap-cell">'+esc(t.process_fit_logic)+'<p>'+esc(t.public_evidence_signals)+'</p><div>'+esc(t.primary_energy_service)+'</div></td><td class="wrap-cell">'+esc(t.site_constraints_required)+'<p>'+esc(t.economic_inputs_required)+'</p></td><td class="wrap-cell">'+safeLink(t.generic_evidence_url,'Generischer Beleg')+'<p>'+esc(t.generic_evidence_note)+'</p></td></tr>'))+'</section>';return;
  }

  if(view==="methodology"){
    title.textContent="Methodik";
    sub.textContent="Die zentralen Forschungsregeln, die das SME-ETOI-System erzwingt.";
    root.innerHTML='<div class="functional-two-col">'+
      '<section class="functional-card"><h3>Technical Relevance Engine</h3><p>Bewertet, welche Energielösungen aufgrund öffentlich belegter Prozesssignale technisch relevant sind.</p></section>'+
      '<section class="functional-card"><h3>Commercial White Space</h3><p>Trennt technische Relevanz davon, was öffentlich bereits als implementiert belegt ist.</p></section>'+
      '<section class="functional-card"><h3>Research Queue</h3><p>Priorisiert fehlende Fakten nach erwartetem Entscheidungswert. SME-Eligibility-Gates stehen vor Deployment-Recherche.</p></section>'+
      '<section class="functional-card"><h3>Research Safeguard</h3><p><strong>UNKNOWN bleibt UNKNOWN.</strong> Fehlende öffentliche Evidenz ist kein Beweis für Nicht-Deployment oder White Space.</p></section>'+
      '<section class="functional-card"><h3>Finale Score-Freigabe</h3><p>Geprüfte Feldvorschläge haben einen eigenen Status. Ihre Übernahme in die endgültigen Scores braucht eine separate Freigabe.</p></section>'+
      '<section class="functional-card"><h3>Eligibility</h3><p>Technische Relevanz bleibt sichtbar, aber ungeklärte SME-/Gruppenstruktur blockiert die Actionability.</p></section>'+
    '</div>'+
      '<section class="functional-card"><h3>ETOI-Felder und Obergrenzen · '+esc(state.data.scoring_methodology?.maximum_total)+' Punkte</h3><p>Fünf Dimensionen, 15 Felder. Offene Werte bleiben UNKNOWN; generische Temperaturbereiche liefern keine firmenspezifischen Punkte. Technische Priorität A/B/C, Quellenconfidence und finale Scores sind getrennte Größen.</p>'+genericTable(['Dimension / Maximum','Feld','Maximum'],Object.entries(state.data.scoring_methodology?.dimensions||{}).flatMap(([d,fields])=>Object.entries(fields).map(([f,max])=>'<tr data-score-field="'+esc(f)+'"><td>'+esc(titleCase(d))+' · '+Object.values(fields).reduce((a,b)=>a+b,0)+'</td><td>'+esc(titleCase(f))+'</td><td>'+esc(max)+'</td></tr>')))+'<p>Dokumentiertes Investitionsfenster: 07.10.2021 bis 07.10.2026. Es verschiebt sich nicht automatisch mit dem Abrufdatum.</p></section>'+
      '<section class="functional-card"><h3>Prozessbibliothek · '+(state.data.reference_libraries?.processes||[]).length+'</h3><p>Generische Referenzbereiche; keine gemessenen Unternehmenswerte. Antrieb, Wärme, Kühlung, Flexibilität und Power Quality werden als Prozessmerkmale dokumentiert.</p>'+genericTable(['Prozess / Temperaturbereich','Energiedienste / Relevanz','Flexibilität / Betriebsweise','Prüfstatus / Referenz'],(state.data.reference_libraries?.processes||[]).map(p=>'<tr data-process-id="'+esc(p.process_id)+'"><td>'+esc(p.process_name)+'<div class="source-meta">'+esc(p.process_family)+' · '+esc(knownValue(p.typical_temperature_min_c))+' bis '+esc(knownValue(p.typical_temperature_max_c))+' °C</div></td><td class="wrap-cell">'+esc(p.dominant_energy_service)+'<div>Antrieb: '+esc(p.drive_relevance)+' · Wärme: '+esc(p.process_heat_relevance)+' · Kälte: '+esc(p.cooling_relevance)+'</div><div>Leistungselektronik: '+esc(p.power_electronics_relevance)+' · Power Quality: '+esc(p.power_quality_relevance)+'</div></td><td class="wrap-cell">'+esc(p.batch_continuous)+' · Planung: '+esc(p.schedulability)+' · Speicher / Trägheit: '+esc(p.thermal_inertia_storage)+'</td><td class="wrap-cell">'+esc(p.review_status)+'<div>'+safeLink(p.generic_evidence_url,'Generischer Beleg')+'</div><p>'+esc(p.generic_evidence_note)+'</p></td></tr>'))+'</section>'+
      '<section class="functional-card"><h3>Opportunity-Regeln · '+(state.data.reference_libraries?.opportunity_rules||[]).length+'</h3>'+genericTable(['Regel / Ergebnis','Benötigte Signale / Blocker','Begründung / Confidence'],(state.data.reference_libraries?.opportunity_rules||[]).map(r=>'<tr data-rule-id="'+esc(r.rule_id)+'"><td>'+esc(r.rule_id)+' · '+esc(titleCase(r.opportunity_type))+'<div>'+esc(r.output_level)+' · '+esc(r.rule_status)+'</div></td><td class="wrap-cell">Prozess: '+esc(r.required_process_signal)+'<div>Firma: '+esc(r.required_company_signal)+'</div><div>Blocker: '+esc(r.blocking_signal)+'</div></td><td class="wrap-cell">'+esc(r.reason_template)+'<div>Confidence-Cap: '+esc(r.confidence_cap)+'</div></td></tr>'))+'</section>';return;
  }

  if(view==="quality"){
    title.textContent="Qualitätssicherung";
    sub.textContent="Dokumentierte QA und unabhängige Zweitprüfung mit ihren tatsächlichen Grenzen.";
    const q=state.data.quality_assurance||{};
    const checks=q.company_checks||[];
    const reliability=q.reliability||[];
    const conflicts=q.double_code_conflicts||[];
    root.innerHTML='<section class="functional-card"><h3>QA-Protokolle · '+checks.length+'</h3><p>Eine dokumentarische QA ersetzt keine unabhängige Prüfung. Datum, Prüfmethode und verbleibende Grenzen werden je Firma gezeigt.</p>'+genericTable(['Firma / Datum','Identität / KMU','Prozess / Zertifikate / Quellen','Ergebnis / Einschränkung'],checks.map(r=>'<tr data-qa-company="'+esc(r.company_id)+'" data-company-id="'+esc(r.company_id)+'"><td>'+esc(r.legal_entity)+'<div>'+esc(r.qa_date)+' · '+esc(r.qa_reviewer)+'</div></td><td class="wrap-cell">'+esc(r.legal_entity_check)+'<div>'+esc(r.group_sme_check)+'</div></td><td class="wrap-cell">'+esc(r.process_check)+'<div>'+esc(r.certificate_check)+'</div><div>'+esc(r.evidence_traceability_check)+'</div></td><td class="wrap-cell">'+esc(r.qa_result)+'<p>'+esc(r.remaining_limitation)+'</p><div>Unabhängige Prüfung: '+esc(r.independent_human_review_status)+'</div></td></tr>'))+'</section>'+
      '<section class="functional-card"><h3>Unabhängige Zweitcodierung</h3><p>'+Object.entries(q.independent_review_status_counts||{}).map(([k,v])=>esc(k)+': '+esc(v)).join(' · ')+'</p><p>Ohne abgeschlossene unabhängige Vergleichspaare bleiben Übereinstimmung und Kappa UNKNOWN. Eine leere Konfliktliste bestätigt keine Übereinstimmung.</p>'+genericTable(['Feld','Abgeschlossene Paare','Übereinstimmung / Differenzen','Anteil / Kappa','Interpretation'],reliability.map(r=>'<tr data-reliability-field="'+esc(r.field)+'"><td>'+esc(r.field)+'</td><td>'+esc(r.completed_pairs)+'</td><td>'+esc(r.agreements)+' / '+esc(r.disagreements)+'</td><td>'+esc(knownValue(r.percent_agreement))+' / '+esc(knownValue(r.cohens_kappa))+'</td><td>'+esc(r.interpretation)+'</td></tr>'))+'<h4>Dokumentierte Konflikte · '+conflicts.length+'</h4>'+genericTable(['Firma / Feld','Werte','Prüfung / Auflösung'],conflicts.map(r=>'<tr><td>'+esc(r.company_id)+' · '+esc(r.field)+'</td><td>'+esc(knownValue(r.canonical_value))+' / '+esc(knownValue(r.reviewer_value))+'</td><td>'+esc(r.reviewer)+' · '+esc(r.review_date)+' · '+esc(r.resolution_status)+'</td></tr>'))+'</section>';
    bindFunctionalCompanyRows();return;
  }

  if(view==="documentation"){
    title.textContent="Dokumentation";
    sub.textContent="Projektunterlagen, Datenstand und Zugriff auf die private Weboberfläche.";
    root.innerHTML='<div class="functional-two-col">'+
      '<section class="functional-card"><h3>Webzugriff</h3><p>'+safeLink('https://sme-etoi.fairorbit8.chatgpt.site','Private SME-ETOI-Weboberfläche')+'</p><p>Im zugeordneten ChatGPT-Konto öffnen. Aktualisieren lädt den veröffentlichten Datenstand; neue Recherche wird nach Prüfung und Veröffentlichung sichtbar.</p></section>'+
      '<section class="functional-card"><h3>Aktuelles Sample</h3><p>'+esc(state.data.meta.company_count)+' Unternehmen · '+esc(state.data.meta.opportunity_count)+' Opportunity-Zeilen · '+esc(state.data.meta.research_task_count)+' Rechercheaufgaben · '+esc(state.data.meta.eligibility_gate_count)+' offene KMU-Gates</p><p>Stammdaten tragen ihr eigenes Prüfdatum. Spätere Quellen- und Feldprüfungen werden mit ihrem jeweiligen Datum angezeigt.</p></section>'+
      '<section class="functional-card"><h3>Projektunterlagen</h3>'+ (state.data.documentation_links||[]).map(d=>'<p>'+safeLink(d.url,d.path)+'</p>').join('')+'</section>'+
      '<section class="functional-card"><h3>Reproduzierbare Ausführung</h3><details class="audit-details"><summary>Lokaler Zugriff und Pipeline</summary><pre>python src/run_pipeline.py\npython src/run_pipeline.py --check-only\npython -m http.server 8000 --directory web</pre><p>Lokaler Browser: http://localhost:8000. Historische Snapshots und synthetische Demos werden in der Abdeckungsprüfung getrennt vom aktuellen Sample beschrieben.</p></details></section>'+
    '</div>';return;
  }
}
function showFunctional(view){
  $("#analyticsBand").hidden=true;
  $(".master-detail").hidden=true;
  $("#researchPage").hidden=true;
  $("#functionalPage").hidden=false;$("#evidenceOverview").hidden=true;
  renderFunctional(view);
  setPageChrome($("#functionalTitle").textContent,false);
}
function showNav(view){
  setActiveNav(view);
  if(view==="companies"||view==="dashboard"){
    if(view==="dashboard"){state.viewMode="analysis";$("#viewModeSelect").value="analysis";}
    if(state.scope==="research")state.scope="all";
    syncCompanyControls();
    setPageChrome(view==="dashboard"?"Dashboard":"Zielunternehmen",true);
    showCompanies();renderAll();if(view==="dashboard")$("#analyticsBand").scrollIntoView({behavior:"smooth"});return;
  }
  if(view==="research"){
    setPageChrome("Research Queue",false);showResearch();return;
  }
  showFunctional(view);
}
function renderAll(){renderEvidenceOverview();renderMetrics();renderRegionChart();renderPriority();renderTable();renderDetail();renderResearch()}
function showCompanies(){
  $("#functionalPage").hidden=true;$("#evidenceOverview").hidden=false;$("#analyticsBand").hidden=state.viewMode==="table";$(".master-detail").hidden=false;$("#researchPage").hidden=true;
}
function showResearch(){
  $("#functionalPage").hidden=true;$("#evidenceOverview").hidden=true;$("#analyticsBand").hidden=true;$(".master-detail").hidden=true;$("#researchPage").hidden=false;renderResearch();
}
function exportCsv(){
  const rows=companies(), header=["company_id","legal_entity","sector","region","score","technical_priority","confidence","kmu_einstufung","gepruefte_felder","offene_feldfragen","iso_50001_nachweis","iso_14001_nachweis","emas_nachweis"];
  const lines=[header.join(",")].concat(rows.map(c=>{
    const [status]=statusInfo(c);
    const fields=fieldProgress(c);
    return [c.company_id,c.legal_entity,sectorLabel(c),c.state,c.opportunity_score??"",priority(c),c.evidence_confidence,status,fields.checked,fields.open,certificateInfo(c.certifications?.iso_50001)[0],certificateInfo(c.certifications?.iso_14001)[0],certificateInfo(c.certifications?.emas)[0]].map(v=>'"'+String(v??"").replaceAll('"','""')+'"').join(",");
  }));
  const blob=new Blob([lines.join("\n")],{type:"text/csv;charset=utf-8"});
  const url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download="sme-etoi-zielunternehmen.csv";a.click();URL.revokeObjectURL(url);
}
function bind(){
  $("#refreshCommand").addEventListener("click",()=>location.reload());
  $("#waffleCommand").addEventListener("click",()=>$(".app").classList.toggle("nav-collapsed"));
  $(".nav-toggle").addEventListener("click",()=>$(".app").classList.toggle("nav-collapsed"));
  $("#alertsCommand").addEventListener("click",()=>showNav("tasks"));
  $("#createCommand").addEventListener("click",()=>showNav("notes"));
  $("#settingsCommand").addEventListener("click",()=>{document.body.classList.toggle("dense-mode");showToast(document.body.classList.contains("dense-mode")?"Kompakte Darstellung aktiviert.":"Normale Darstellung aktiviert.")});
  $("#helpCommand").addEventListener("click",()=>showNav("documentation"));
  $("#viewDocsCommand").addEventListener("click",()=>showNav("documentation"));
  $("#moreCommand").addEventListener("click",()=>showNav("documentation"));
  $("#filterButton").addEventListener("click",()=>{$("#focusFilter").focus();showToast("Fokusfilter geöffnet.")});
  $("#newViewCommand").addEventListener("click",()=>{state.query="";state.focus="";state.scope="all";state.page=1;showNav("companies");showToast("Ansicht zurückgesetzt")});
  $("#exportCommand").addEventListener("click",exportCsv);
  $("#chartsCommand").addEventListener("click",()=>{state.viewMode="analysis";$("#viewModeSelect").value="analysis";showNav("dashboard")});
  $("#methodCommand").addEventListener("click",()=>showNav("methodology"));
  $("#backCommand").addEventListener("click",()=>history.back());
  $("#viewModeSelect").addEventListener("change",e=>{state.viewMode=e.target.value;showNav("companies")});
  $("#focusFilter").addEventListener("change",e=>{state.focus=e.target.value;state.page=1;renderAll()});
  $("#tableSearch").addEventListener("input",e=>{state.query=e.target.value;$("#globalSearch").value=e.target.value;state.page=1;renderAll()});
  $("#globalSearch").addEventListener("input",e=>{state.query=e.target.value;state.page=1;showNav("companies")});
  $("#prevPage").addEventListener("click",()=>{if(state.page>1){state.page--;renderTable();renderDetail()}});
  $("#nextPage").addEventListener("click",()=>{state.page++;renderTable();renderDetail()});
  $("#researchSearch").addEventListener("input",e=>{state.researchQuery=e.target.value;renderResearch()});
  $$(".tab[data-scope]").forEach(b=>b.addEventListener("click",()=>{
    state.scope=b.dataset.scope;state.page=1;
    syncCompanyControls();
    if(state.scope==="research"){setActiveNav("research");showResearch()}else showNav("companies");
  }));
  $$("[data-nav]").forEach(b=>b.addEventListener("click",()=>showNav(b.dataset.nav)));
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
