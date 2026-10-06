const state = {
  data: null,
  activeView: "overview",
  companyQuery: "",
  stratum: "",
  eligibility: "",
  confidence: "",
  researchQuery: "",
  researchPriority: "",
  researchStatus: ""
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

function esc(value) {
  return String(value == null ? "" : value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function titleCase(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatNumber(value) {
  if (value === null || value === undefined || value === "") return "—";
  return new Intl.NumberFormat("en-US").format(value);
}

function formatMoney(value) {
  if (value === null || value === undefined || value === "") return "—";
  return "€" + new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(value) + "m";
}

function eligibilityFromCompany(company) {
  const opportunity = company.opportunities && company.opportunities.length ? company.opportunities[0] : null;
  return {
    status: opportunity ? opportunity.sample_eligibility_status : "PROVISIONAL_PASS",
    actionability: opportunity ? opportunity.actionability_status : "PROVISIONAL"
  };
}

function badgeClass(value) {
  const text = String(value || "").toUpperCase();
  if (text.includes("CONFIRMED") || text === "ACTIONABLE" || text === "RESOLVED" || text === "VALID" || text === "A") return "green";
  if (text.includes("PENDING") || text.includes("PROVISIONAL") || text === "RESEARCH_REQUIRED" || text === "RECHECK_DUE" || text === "B") return "amber";
  if (text.includes("BLOCKED") || text.includes("EXCLUDED") || text === "EXPIRED" || text === "C") return "red";
  if (text === "HIGH") return "violet";
  if (text === "MEDIUM") return "blue";
  return "gray";
}

function badge(value, label) {
  return '<span class="badge ' + badgeClass(value) + '">' + esc(label || titleCase(value)) + "</span>";
}

function setView(view) {
  state.activeView = view;
  $$(".nav-item").forEach((button) => button.classList.toggle("active", button.dataset.view === view));
  $$(".view").forEach((section) => section.classList.remove("active"));
  const target = $("#" + view + "View");
  if (target) target.classList.add("active");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderMetrics() {
  const meta = state.data.meta;
  const cards = [
    ["Companies", meta.company_count, "balanced industrial SME pilot"],
    ["Opportunity signals", meta.opportunity_count, "process- and evidence-derived rows"],
    ["Research tasks", meta.research_task_count, "ranked by expected decision impact"],
    ["Eligibility gates", meta.eligibility_gate_count, meta.eligibility_blocked_company_count + " companies need SME/group clarification"]
  ];
  $("#metricGrid").innerHTML = cards.map((card) =>
    '<article class="metric-card">' +
      '<div class="metric-label">' + esc(card[0]) + '</div>' +
      '<div class="metric-value">' + formatNumber(card[1]) + '</div>' +
      '<div class="metric-foot">' + esc(card[2]) + '</div>' +
    '</article>'
  ).join("");
}

function renderOpportunityBars() {
  const values = state.data.opportunity_types || [];
  const max = Math.max.apply(null, values.map((item) => item.count).concat([1]));
  $("#opportunityBars").innerHTML = values.map((item) =>
    '<div class="bar-item">' +
      '<div class="bar-label">' + esc(titleCase(item.opportunity_type)) + '</div>' +
      '<div class="bar-track" aria-hidden="true"><div class="bar-fill" style="width:' + Math.max(5, (item.count / max) * 100) + '%"></div></div>' +
      '<div class="bar-value">' + formatNumber(item.count) + '</div>' +
    '</div>'
  ).join("");
}

function renderResearchSummary() {
  const statusCounts = state.data.research_summary.task_status_counts || {};
  const priorityCounts = state.data.research_summary.priority_counts || {};
  const rows = [
    ["High-priority tasks", priorityCounts.HIGH || 0],
    ["Open tasks", statusCounts.OPEN || 0],
    ["Recheck due", statusCounts.RECHECK_DUE || 0],
    ["Awaiting review", statusCounts.AWAITING_REVIEW || 0],
    ["Awaiting canonical update", statusCounts.AWAITING_CANONICAL_UPDATE || 0]
  ];
  $("#researchSummary").innerHTML = rows.map((row) =>
    '<div class="status-row"><strong>' + esc(row[0]) + '</strong><span>' + formatNumber(row[1]) + '</span></div>'
  ).join("");
}

function populateFilters() {
  const strata = Array.from(new Set(state.data.companies.map((c) => c.process_stratum).filter(Boolean))).sort();
  $("#stratumFilter").innerHTML = '<option value="">All process strata</option>' +
    strata.map((value) => '<option value="' + esc(value) + '">' + esc(titleCase(value)) + '</option>').join("");

  const eligibilityStates = Array.from(new Set(state.data.companies.map((c) => eligibilityFromCompany(c).status).filter(Boolean))).sort();
  $("#eligibilityFilter").innerHTML = '<option value="">All eligibility states</option>' +
    eligibilityStates.map((value) => '<option value="' + esc(value) + '">' + esc(titleCase(value)) + '</option>').join("");

  const taskStatuses = Array.from(new Set(
    state.data.companies.flatMap((company) => (company.research_tasks || []).map((task) => task.task_status || "OPEN"))
  )).sort();
  $("#researchStatusFilter").innerHTML = '<option value="">All task states</option>' +
    taskStatuses.map((value) => '<option value="' + esc(value) + '">' + esc(titleCase(value)) + '</option>').join("");
}

function filteredCompanies() {
  const query = state.companyQuery.trim().toLowerCase();
  return state.data.companies.filter((company) => {
    const eligibility = eligibilityFromCompany(company).status;
    const processText = (company.processes || []).map((process) => process.process_name + " " + process.process_name_raw).join(" ");
    const haystack = [
      company.legal_entity, company.company_id, company.city, company.state,
      company.nace_label, company.process_stratum, processText
    ].join(" ").toLowerCase();

    return (!query || haystack.includes(query)) &&
      (!state.stratum || company.process_stratum === state.stratum) &&
      (!state.eligibility || eligibility === state.eligibility) &&
      (!state.confidence || company.evidence_confidence === state.confidence);
  });
}

function renderCompanies() {
  const companies = filteredCompanies();
  $("#companyCountLabel").textContent = companies.length + (companies.length === 1 ? " company" : " companies");

  const html = companies.map((company) => {
    const eligibility = eligibilityFromCompany(company);
    const processes = Array.from(new Set((company.processes || []).map((process) => process.process_name).filter(Boolean)));
    return '<div class="company-row data-row" role="row" tabindex="0" data-company-id="' + esc(company.company_id) + '">' +
      '<div class="company-primary">' +
        '<div class="company-name">' + esc(company.legal_entity) + '</div>' +
        '<div class="company-location">' + esc([company.city, company.state].filter(Boolean).join(", ")) + '</div>' +
      '</div>' +
      '<div class="process-text">' + esc(processes.map(titleCase).join(", ") || titleCase(company.process_stratum)) + '</div>' +
      '<div>' + badge(eligibility.status) + '</div>' +
      '<div><span class="confidence ' + esc((company.evidence_confidence || "C").toLowerCase()) + '">' + esc(company.evidence_confidence || "?") + '</span></div>' +
      '<div class="opportunity-count">' + formatNumber((company.opportunities || []).length) + '</div>' +
    '</div>';
  }).join("");

  $("#companyRows").innerHTML = html || '<div class="empty-state">No companies match these filters.</div>';

  $$("#companyRows .data-row").forEach((row) => {
    const open = () => openCompany(row.dataset.companyId);
    row.addEventListener("click", open);
    row.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        open();
      }
    });
  });
}

function researchTasks() {
  return state.data.companies.flatMap((company) =>
    (company.research_tasks || []).map((task) => Object.assign({}, task, {
      company_id: company.company_id,
      legal_entity: company.legal_entity
    }))
  ).sort((a, b) => (a.research_rank || 999999) - (b.research_rank || 999999));
}

function renderResearch() {
  const query = state.researchQuery.trim().toLowerCase();
  const tasks = researchTasks().filter((task) => {
    const haystack = [task.legal_entity, task.company_id, task.opportunity_type, task.research_question, task.missing_fact].join(" ").toLowerCase();
    return (!query || haystack.includes(query)) &&
      (!state.researchPriority || task.research_priority === state.researchPriority) &&
      (!state.researchStatus || (task.task_status || "OPEN") === state.researchStatus);
  });

  $("#researchCards").innerHTML = tasks.map((task) =>
    '<article class="research-card">' +
      '<div class="rank">#' + esc(task.research_rank == null ? "—" : task.research_rank) + '</div>' +
      '<div><div class="research-company">' + esc(task.legal_entity) + '</div><div class="research-type">' + esc(titleCase(task.opportunity_type)) + '</div></div>' +
      '<div><div class="research-question">' + esc(task.research_question) + '</div><div class="research-meta">' +
        badge(task.research_priority, titleCase(task.research_priority) + " priority") +
        badge(task.decision_impact, titleCase(task.decision_impact) + " impact") +
        badge(task.task_status || "OPEN") +
      '</div></div>' +
      '<div><button class="nav-item research-open" data-company-id="' + esc(task.company_id) + '">Open company</button></div>' +
    '</article>'
  ).join("") || '<div class="empty-state">No research tasks match these filters.</div>';

  $$(".research-open").forEach((button) => button.addEventListener("click", () => openCompany(button.dataset.companyId)));
}

function opportunityCard(opportunity) {
  return '<article class="opportunity-card">' +
    '<div class="card-topline"><div class="card-title">' + esc(titleCase(opportunity.opportunity_type)) + '</div>' + badge(opportunity.opportunity_level) + '</div>' +
    '<div class="research-meta">' +
      badge(opportunity.commercial_status) +
      badge(opportunity.actionability_status) +
      badge(opportunity.confidence, "Confidence " + (opportunity.confidence || "?")) +
    '</div>' +
    '<div class="card-body" style="margin-top:10px"><strong>Why now:</strong> ' + esc(opportunity.why_now || "No additional urgency signal documented.") +
      '<br><br><strong>Next action:</strong> ' + esc(opportunity.next_action || "—") +
    '</div>' +
  '</article>';
}

function taskCard(task) {
  return '<article class="task-card">' +
    '<div class="card-topline"><div class="card-title">#' + esc(task.research_rank == null ? "—" : task.research_rank) + ' · ' + esc(titleCase(task.opportunity_type)) + '</div>' + badge(task.task_status || "OPEN") + '</div>' +
    '<div class="card-body">' + esc(task.research_question) +
      (task.last_finding ? '<br><br><strong>Latest finding:</strong> ' + esc(task.last_finding) : "") +
    '</div>' +
  '</article>';
}

function sourceCard(source) {
  return '<article class="source-card">' +
    '<div class="card-title">' + esc(source.document_title || source.publisher || source.source_id) + '</div>' +
    '<div class="source-meta">' + esc([source.source_id, titleCase(source.source_type), source.publisher].filter(Boolean).join(" · ")) + '</div>' +
    (source.evidence_fact ? '<div class="source-meta">' + esc(source.evidence_fact) + '</div>' : "") +
    (source.final_url ? '<div style="margin-top:8px"><a href="' + esc(source.final_url) + '" target="_blank" rel="noopener noreferrer">Open source ↗</a></div>' : "") +
  '</article>';
}

function openCompany(companyId) {
  const company = state.data.companies.find((item) => item.company_id === companyId);
  if (!company) return;

  const eligibility = eligibilityFromCompany(company);
  const processNames = Array.from(new Set((company.processes || []).map((process) => process.process_name).filter(Boolean)));
  const certs = company.certifications || {};

  $("#drawerContent").innerHTML =
    '<div class="eyebrow">' + esc(company.company_id) + ' · ' + esc(titleCase(company.process_stratum)) + '</div>' +
    '<h2>' + esc(company.legal_entity) + '</h2>' +
    '<div class="drawer-subtitle">' + esc([company.city, company.state].filter(Boolean).join(", ")) + '</div>' +
    '<div class="drawer-status-line">' +
      badge(eligibility.status) +
      badge(eligibility.actionability) +
      badge(company.evidence_confidence, "Evidence confidence " + (company.evidence_confidence || "?")) +
    '</div>' +

    '<section class="drawer-section"><h3>Company intelligence</h3><div class="fact-grid">' +
      '<div class="fact"><div class="fact-label">Employees</div><div class="fact-value">' + formatNumber(company.employees) + '</div></div>' +
      '<div class="fact"><div class="fact-label">Revenue</div><div class="fact-value">' + formatMoney(company.revenue_eur_m) + '</div></div>' +
      '<div class="fact"><div class="fact-label">Balance sheet</div><div class="fact-value">' + formatMoney(company.balance_sheet_eur_m) + '</div></div>' +
      '<div class="fact"><div class="fact-label">Group check</div><div class="fact-value">' + esc(titleCase(company.group_check)) + '</div></div>' +
      '<div class="fact"><div class="fact-label">ISO 50001</div><div class="fact-value">' + esc(titleCase(certs.iso_50001)) + '</div></div>' +
      '<div class="fact"><div class="fact-label">Last verified</div><div class="fact-value">' + esc(company.last_verified_date || "—") + '</div></div>' +
    '</div>' +
    (company.website ? '<div style="margin-top:14px"><a href="' + esc(company.website) + '" target="_blank" rel="noopener noreferrer">Company website ↗</a></div>' : "") +
    '</section>' +

    '<section class="drawer-section"><h3>Mapped processes</h3><div class="chip-row">' +
      (processNames.length ? processNames.map((name) => '<span class="chip">' + esc(titleCase(name)) + '</span>').join("") : '<span class="chip">No process label</span>') +
    '</div></section>' +

    '<section class="drawer-section"><h3>Opportunity signals · ' + formatNumber((company.opportunities || []).length) + '</h3>' +
      ((company.opportunities || []).length ? company.opportunities.map(opportunityCard).join("") : '<div class="empty-state">No opportunity rows.</div>') +
    '</section>' +

    '<section class="drawer-section"><h3>Research tasks · ' + formatNumber((company.research_tasks || []).length) + '</h3>' +
      ((company.research_tasks || []).length ? company.research_tasks.map(taskCard).join("") : '<div class="empty-state">No unresolved research tasks.</div>') +
    '</section>' +

    '<section class="drawer-section"><h3>Evidence trail · ' + formatNumber((company.sources || []).length) + ' sources</h3>' +
      ((company.sources || []).length ? company.sources.map(sourceCard).join("") : '<div class="empty-state">No source-register rows available.</div>') +
    '</section>';

  $("#drawerBackdrop").hidden = false;
  $("#companyDrawer").classList.add("open");
  $("#companyDrawer").setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function closeDrawer() {
  $("#companyDrawer").classList.remove("open");
  $("#companyDrawer").setAttribute("aria-hidden", "true");
  $("#drawerBackdrop").hidden = true;
  document.body.style.overflow = "";
}

function bindEvents() {
  $$(".nav-item[data-view]").forEach((button) => button.addEventListener("click", () => setView(button.dataset.view)));

  $("#companySearch").addEventListener("input", (event) => { state.companyQuery = event.target.value; renderCompanies(); });
  $("#stratumFilter").addEventListener("change", (event) => { state.stratum = event.target.value; renderCompanies(); });
  $("#eligibilityFilter").addEventListener("change", (event) => { state.eligibility = event.target.value; renderCompanies(); });
  $("#confidenceFilter").addEventListener("change", (event) => { state.confidence = event.target.value; renderCompanies(); });

  $("#researchSearch").addEventListener("input", (event) => { state.researchQuery = event.target.value; renderResearch(); });
  $("#researchPriorityFilter").addEventListener("change", (event) => { state.researchPriority = event.target.value; renderResearch(); });
  $("#researchStatusFilter").addEventListener("change", (event) => { state.researchStatus = event.target.value; renderResearch(); });

  $("#drawerClose").addEventListener("click", closeDrawer);
  $("#drawerBackdrop").addEventListener("click", closeDrawer);
  document.addEventListener("keydown", (event) => { if (event.key === "Escape") closeDrawer(); });
}

async function init() {
  bindEvents();
  try {
    const response = await fetch("data/sme_etoi.json", { cache: "no-store" });
    if (!response.ok) throw new Error("HTTP " + response.status);
    state.data = await response.json();

    $("#snapshotLabel").textContent = "Public-data snapshot · " + (state.data.meta.source_snapshot_date || "current repository state");
    renderMetrics();
    renderOpportunityBars();
    renderResearchSummary();
    populateFilters();
    renderCompanies();
    renderResearch();
  } catch (error) {
    console.error("Failed to load SME-ETOI web data", error);
    $("#errorState").hidden = false;
  }
}

init();
