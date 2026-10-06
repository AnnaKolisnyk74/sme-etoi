const state = {
  data: null,
  activeView: "overview",
  filters: {
    stratum: "",
    state: "",
    confidence: "",
    eligibility: "",
    opportunity: ""
  },
  overviewSearch: "",
  companySearch: "",
  researchSearch: "",
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
  return new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(value);
}

function eligibilityFromCompany(company) {
  const opportunity = company.opportunities && company.opportunities.length
    ? company.opportunities[0]
    : null;
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

function confidencePill(value) {
  const grade = String(value || "?").toUpperCase();
  return '<span class="confidence-pill ' + esc(grade.toLowerCase()) + '">' + esc(grade) + "</span>";
}

function setView(view) {
  state.activeView = view;
  $$(".page-tab").forEach((button) => button.classList.toggle("active", button.dataset.view === view));
  $$(".bi-view").forEach((section) => section.classList.remove("active"));
  const target = $("#" + view + "View");
  if (target) target.classList.add("active");
}

function companyMatchesGlobalFilters(company, options = {}) {
  const ignore = new Set(options.ignore || []);
  const eligibility = eligibilityFromCompany(company).status;

  if (!ignore.has("stratum") && state.filters.stratum && company.process_stratum !== state.filters.stratum) return false;
  if (!ignore.has("state") && state.filters.state && company.state !== state.filters.state) return false;
  if (!ignore.has("confidence") && state.filters.confidence && company.evidence_confidence !== state.filters.confidence) return false;
  if (!ignore.has("eligibility") && state.filters.eligibility && eligibility !== state.filters.eligibility) return false;

  if (!ignore.has("opportunity") && state.filters.opportunity) {
    const hasOpportunity = (company.opportunities || []).some(
      (opportunity) => opportunity.opportunity_type === state.filters.opportunity
    );
    if (!hasOpportunity) return false;
  }
  return true;
}

function filteredCompanies(options = {}) {
  return state.data.companies.filter((company) => companyMatchesGlobalFilters(company, options));
}

function opportunitiesForCompanies(companies, options = {}) {
  const respectOpportunityFilter = options.respectOpportunityFilter !== false;
  const rows = companies.flatMap((company) =>
    (company.opportunities || []).map((opportunity) => ({
      ...opportunity,
      company_id: company.company_id,
      legal_entity: company.legal_entity
    }))
  );
  if (respectOpportunityFilter && state.filters.opportunity) {
    return rows.filter((row) => row.opportunity_type === state.filters.opportunity);
  }
  return rows;
}

function tasksForCompanies(companies) {
  return companies.flatMap((company) =>
    (company.research_tasks || []).map((task) => ({
      ...task,
      company_id: company.company_id,
      legal_entity: company.legal_entity,
      process_stratum: company.process_stratum,
      state: company.state,
      evidence_confidence: company.evidence_confidence
    }))
  ).sort((a, b) => (a.research_rank || 999999) - (b.research_rank || 999999));
}

function updateFilterResultLabel() {
  const companies = filteredCompanies();
  $("#filterResultLabel").textContent =
    companies.length + (companies.length === 1 ? " company" : " companies");
}

function renderKpis() {
  const companies = filteredCompanies();
  const opportunities = opportunitiesForCompanies(companies);
  const tasks = tasksForCompanies(companies);
  const blocked = companies.filter((company) => eligibilityFromCompany(company).actionability === "ELIGIBILITY_BLOCKED").length;
  const strongEvidence = companies.filter((company) => ["A", "B"].includes(company.evidence_confidence)).length;
  const evidenceShare = companies.length ? Math.round((strongEvidence / companies.length) * 100) : 0;

  const cards = [
    ["Companies", companies.length, "selected pilot companies"],
    ["Opportunity signals", opportunities.length, state.filters.opportunity ? titleCase(state.filters.opportunity) : "all technology types"],
    ["Research tasks", tasks.length, "open or recheckable facts"],
    ["Eligibility blocked", blocked, "companies requiring SME/group resolution"],
    ["A/B evidence", evidenceShare + "%", strongEvidence + " of " + companies.length + " companies"]
  ];

  $("#kpiGrid").innerHTML = cards.map((card) =>
    '<article class="kpi-card">' +
      '<div class="kpi-label">' + esc(card[0]) + '</div>' +
      '<div class="kpi-value">' + esc(card[1]) + '</div>' +
      '<div class="kpi-foot">' + esc(card[2]) + '</div>' +
    '</article>'
  ).join("");
}

function renderOpportunityChart() {
  const companies = filteredCompanies({ ignore: ["opportunity"] });
  const opportunities = opportunitiesForCompanies(companies, { respectOpportunityFilter: false });
  const counts = new Map();
  opportunities.forEach((row) => {
    counts.set(row.opportunity_type, (counts.get(row.opportunity_type) || 0) + 1);
  });

  const rows = Array.from(counts.entries())
    .map(([type, count]) => ({ type, count }))
    .sort((a, b) => b.count - a.count || a.type.localeCompare(b.type));

  const max = Math.max(...rows.map((row) => row.count), 1);
  $("#opportunityChart").innerHTML = rows.map((row) =>
    '<div class="hbar-row' + (state.filters.opportunity === row.type ? ' selected' : '') + '" data-opportunity="' + esc(row.type) + '">' +
      '<div class="hbar-label">' + esc(titleCase(row.type)) + '</div>' +
      '<div class="hbar-track"><div class="hbar-fill" style="width:' + ((row.count / max) * 100).toFixed(2) + '%"></div></div>' +
      '<div class="hbar-value">' + formatNumber(row.count) + '</div>' +
    '</div>'
  ).join("") || '<div class="empty-state">No opportunity signals for this selection.</div>';

  $$("#opportunityChart .hbar-row").forEach((row) => {
    row.addEventListener("click", () => {
      const value = row.dataset.opportunity;
      state.filters.opportunity = state.filters.opportunity === value ? "" : value;
      $("#globalOpportunityFilter").value = state.filters.opportunity;
      renderAll();
    });
  });
}

function eligibilityColor(status) {
  const map = {
    ELIGIBILITY_PENDING: "#d37a26",
    PROVISIONAL_PASS: "#4a78d0",
    CONFIRMED: "#2f9360",
    EXCLUDED: "#c84b43"
  };
  return map[status] || "#98a2b3";
}

function renderEligibilityVisual() {
  const companies = filteredCompanies({ ignore: ["eligibility"] });
  const counts = new Map();
  companies.forEach((company) => {
    const status = eligibilityFromCompany(company).status;
    counts.set(status, (counts.get(status) || 0) + 1);
  });

  const rows = Array.from(counts.entries()).sort((a, b) => b[1] - a[1]);
  const total = rows.reduce((sum, row) => sum + row[1], 0);

  let cursor = 0;
  const stops = rows.map(([status, count]) => {
    const start = total ? (cursor / total) * 100 : 0;
    cursor += count;
    const end = total ? (cursor / total) * 100 : 0;
    return eligibilityColor(status) + " " + start.toFixed(2) + "% " + end.toFixed(2) + "%";
  });

  const legend = rows.map(([status, count]) =>
    '<div class="legend-row" data-eligibility="' + esc(status) + '">' +
      '<span class="legend-dot" style="background:' + eligibilityColor(status) + '"></span>' +
      '<span>' + esc(titleCase(status)) + '</span>' +
      '<span class="legend-value">' + formatNumber(count) + '</span>' +
    '</div>'
  ).join("");

  $("#eligibilityVisual").innerHTML =
    '<div class="donut" style="background:conic-gradient(' + (stops.join(",") || "#e5e7eb 0 100%") + ')">' +
      '<div class="donut-center"><strong>' + formatNumber(total) + '</strong><span>companies</span></div>' +
    '</div>' +
    '<div class="legend-list">' + legend + '</div>';

  $$("#eligibilityVisual .legend-row").forEach((row) => {
    row.style.cursor = "pointer";
    row.addEventListener("click", () => {
      const value = row.dataset.eligibility;
      state.filters.eligibility = state.filters.eligibility === value ? "" : value;
      $("#globalEligibilityFilter").value = state.filters.eligibility;
      renderAll();
    });
  });
}

function renderConfidenceVisual() {
  const companies = filteredCompanies({ ignore: ["confidence"] });
  const grades = ["A", "B", "C"];
  const counts = Object.fromEntries(grades.map((grade) => [grade, 0]));
  companies.forEach((company) => {
    if (counts[company.evidence_confidence] !== undefined) counts[company.evidence_confidence] += 1;
  });
  const max = Math.max(...Object.values(counts), 1);

  $("#confidenceVisual").innerHTML = grades.map((grade) =>
    '<div class="column" data-confidence="' + grade + '" style="cursor:pointer">' +
      '<div class="column-value">' + counts[grade] + '</div>' +
      '<div class="column-bar-wrap"><div class="column-bar" style="height:' + ((counts[grade] / max) * 100).toFixed(2) + '%;opacity:' + (state.filters.confidence && state.filters.confidence !== grade ? '.28' : '1') + '"></div></div>' +
      '<div class="column-label">' + grade + '</div>' +
    '</div>'
  ).join("");

  $$("#confidenceVisual .column").forEach((column) => {
    column.addEventListener("click", () => {
      const value = column.dataset.confidence;
      state.filters.confidence = state.filters.confidence === value ? "" : value;
      $("#globalConfidenceFilter").value = state.filters.confidence;
      renderAll();
    });
  });
}

function renderOverviewMatrix() {
  const query = state.overviewSearch.trim().toLowerCase();
  const companies = filteredCompanies()
    .filter((company) => !query || [company.legal_entity, company.city, company.state].join(" ").toLowerCase().includes(query))
    .sort((a, b) =>
      (b.opportunities || []).length - (a.opportunities || []).length ||
      a.legal_entity.localeCompare(b.legal_entity)
    );

  $("#overviewMatrixBody").innerHTML = companies.map((company) => {
    const eligibility = eligibilityFromCompany(company).status;
    const opportunityCount = state.filters.opportunity
      ? (company.opportunities || []).filter((o) => o.opportunity_type === state.filters.opportunity).length
      : (company.opportunities || []).length;
    return '<tr data-company-id="' + esc(company.company_id) + '">' +
      '<td class="table-company">' + esc(company.legal_entity) + '</td>' +
      '<td>' + esc(titleCase(company.process_stratum)) + '</td>' +
      '<td class="table-muted">' + esc(company.state || "—") + '</td>' +
      '<td>' + confidencePill(company.evidence_confidence) + '</td>' +
      '<td>' + badge(eligibility) + '</td>' +
      '<td class="num">' + formatNumber(opportunityCount) + '</td>' +
      '<td class="num">' + formatNumber((company.research_tasks || []).length) + '</td>' +
    '</tr>';
  }).join("") || '<tr><td colspan="7" class="empty-state">No companies match this selection.</td></tr>';

  $$("#overviewMatrixBody tr[data-company-id]").forEach((row) => {
    row.addEventListener("click", () => openCompany(row.dataset.companyId));
  });
}

function renderResearchStateVisual() {
  const companies = filteredCompanies();
  const tasks = tasksForCompanies(companies);
  const counts = new Map();
  tasks.forEach((task) => {
    const status = task.task_status || "OPEN";
    counts.set(status, (counts.get(status) || 0) + 1);
  });
  const rows = Array.from(counts.entries()).sort((a, b) => b[1] - a[1]);
  const max = Math.max(...rows.map((row) => row[1]), 1);

  $("#researchStateVisual").innerHTML = rows.map(([status, count]) =>
    '<div class="state-row">' +
      '<div class="state-label">' + esc(titleCase(status)) + '</div>' +
      '<div class="state-value">' + formatNumber(count) + '</div>' +
      '<div class="state-track"><div class="state-fill" style="width:' + ((count / max) * 100).toFixed(2) + '%"></div></div>' +
    '</div>'
  ).join("") || '<div class="empty-state">No research tasks.</div>';
}

function renderCompanyExplorer() {
  const query = state.companySearch.trim().toLowerCase();
  const companies = filteredCompanies().filter((company) => {
    const processText = (company.processes || []).map((process) => process.process_name + " " + process.process_name_raw).join(" ");
    const haystack = [company.legal_entity, company.city, company.state, company.nace_label, processText].join(" ").toLowerCase();
    return !query || haystack.includes(query);
  });

  $("#companyCountLabel").textContent = companies.length + (companies.length === 1 ? " company" : " companies");

  $("#companyTableBody").innerHTML = companies.map((company) => {
    const processNames = Array.from(new Set((company.processes || []).map((process) => process.process_name).filter(Boolean)));
    const eligibility = eligibilityFromCompany(company).status;
    const opportunityCount = state.filters.opportunity
      ? (company.opportunities || []).filter((o) => o.opportunity_type === state.filters.opportunity).length
      : (company.opportunities || []).length;
    return '<tr data-company-id="' + esc(company.company_id) + '">' +
      '<td class="table-company">' + esc(company.legal_entity) + '</td>' +
      '<td>' + esc(company.city || "—") + '</td>' +
      '<td>' + esc(processNames.map(titleCase).join(", ") || titleCase(company.process_stratum)) + '</td>' +
      '<td class="num">' + formatNumber(company.employees) + '</td>' +
      '<td class="num">' + formatMoney(company.revenue_eur_m) + '</td>' +
      '<td>' + badge(eligibility) + '</td>' +
      '<td>' + confidencePill(company.evidence_confidence) + '</td>' +
      '<td class="num">' + formatNumber(opportunityCount) + '</td>' +
      '<td class="num">' + formatNumber((company.research_tasks || []).length) + '</td>' +
    '</tr>';
  }).join("") || '<tr><td colspan="9" class="empty-state">No companies match this selection.</td></tr>';

  $$("#companyTableBody tr[data-company-id]").forEach((row) => {
    row.addEventListener("click", () => openCompany(row.dataset.companyId));
  });
}

function filteredResearchTasks() {
  const query = state.researchSearch.trim().toLowerCase();
  const companies = filteredCompanies();
  return tasksForCompanies(companies).filter((task) => {
    const haystack = [task.legal_entity, task.company_id, task.opportunity_type, task.research_question, task.missing_fact].join(" ").toLowerCase();
    return (!query || haystack.includes(query)) &&
      (!state.researchPriority || task.research_priority === state.researchPriority) &&
      (!state.researchStatus || (task.task_status || "OPEN") === state.researchStatus);
  });
}

function renderResearchKpis() {
  const tasks = filteredResearchTasks();
  const high = tasks.filter((task) => task.research_priority === "HIGH").length;
  const gates = tasks.filter((task) => task.opportunity_type === "sme_eligibility").length;
  const recheck = tasks.filter((task) => task.task_status === "RECHECK_DUE").length;
  const cards = [
    ["Visible tasks", tasks.length, "after all filters"],
    ["High priority", high, "decision-critical checks"],
    ["SME eligibility", gates, "sample gates"],
    ["Recheck due", recheck, "partial or unresolved evidence"]
  ];
  $("#researchKpis").innerHTML = cards.map((card) =>
    '<article class="kpi-card">' +
      '<div class="kpi-label">' + esc(card[0]) + '</div>' +
      '<div class="kpi-value">' + esc(card[1]) + '</div>' +
      '<div class="kpi-foot">' + esc(card[2]) + '</div>' +
    '</article>'
  ).join("");
}

function renderResearchTable() {
  const tasks = filteredResearchTasks();
  $("#researchTableBody").innerHTML = tasks.map((task) =>
    '<tr data-company-id="' + esc(task.company_id) + '">' +
      '<td class="num">' + formatNumber(task.research_rank) + '</td>' +
      '<td class="table-company">' + esc(task.legal_entity) + '</td>' +
      '<td>' + esc(titleCase(task.opportunity_type)) + '</td>' +
      '<td class="research-question-cell">' + esc(task.research_question) + '</td>' +
      '<td>' + badge(task.research_priority) + '</td>' +
      '<td>' + badge(task.decision_impact) + '</td>' +
      '<td>' + badge(task.task_status || "OPEN") + '</td>' +
    '</tr>'
  ).join("") || '<tr><td colspan="7" class="empty-state">No research tasks match this selection.</td></tr>';

  $$("#researchTableBody tr[data-company-id]").forEach((row) => {
    row.addEventListener("click", () => openCompany(row.dataset.companyId));
  });
}

function opportunityCard(opportunity) {
  return '<article class="opportunity-card">' +
    '<div class="card-topline"><div class="card-title">' + esc(titleCase(opportunity.opportunity_type)) + '</div>' + badge(opportunity.opportunity_level) + '</div>' +
    '<div class="research-meta">' +
      badge(opportunity.commercial_status) +
      badge(opportunity.actionability_status) +
      badge(opportunity.confidence, "Confidence " + (opportunity.confidence || "?")) +
    '</div>' +
    '<div class="card-body" style="margin-top:8px"><strong>Why now:</strong> ' + esc(opportunity.why_now || "No additional urgency signal documented.") +
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
    (source.final_url ? '<div style="margin-top:6px"><a href="' + esc(source.final_url) + '" target="_blank" rel="noopener noreferrer">Open source ↗</a></div>' : "") +
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
      '<div class="fact"><div class="fact-label">Revenue</div><div class="fact-value">' + (company.revenue_eur_m == null ? "—" : "€" + formatMoney(company.revenue_eur_m) + "m") + '</div></div>' +
      '<div class="fact"><div class="fact-label">Balance sheet</div><div class="fact-value">' + (company.balance_sheet_eur_m == null ? "—" : "€" + formatMoney(company.balance_sheet_eur_m) + "m") + '</div></div>' +
      '<div class="fact"><div class="fact-label">Group check</div><div class="fact-value">' + esc(titleCase(company.group_check)) + '</div></div>' +
      '<div class="fact"><div class="fact-label">ISO 50001</div><div class="fact-value">' + esc(titleCase(certs.iso_50001)) + '</div></div>' +
      '<div class="fact"><div class="fact-label">Last verified</div><div class="fact-value">' + esc(company.last_verified_date || "—") + '</div></div>' +
    '</div>' +
    (company.website ? '<div style="margin-top:10px"><a href="' + esc(company.website) + '" target="_blank" rel="noopener noreferrer">Company website ↗</a></div>' : "") +
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

function populateGlobalFilters() {
  const companies = state.data.companies;
  const strata = Array.from(new Set(companies.map((company) => company.process_stratum).filter(Boolean))).sort();
  const states = Array.from(new Set(companies.map((company) => company.state).filter(Boolean))).sort();
  const eligibilityStates = Array.from(new Set(companies.map((company) => eligibilityFromCompany(company).status).filter(Boolean))).sort();
  const opportunityTypes = Array.from(new Set(companies.flatMap((company) => (company.opportunities || []).map((opportunity) => opportunity.opportunity_type)))).sort();

  $("#globalStratumFilter").innerHTML = '<option value="">All</option>' + strata.map((value) => '<option value="' + esc(value) + '">' + esc(titleCase(value)) + '</option>').join("");
  $("#globalStateFilter").innerHTML = '<option value="">All</option>' + states.map((value) => '<option value="' + esc(value) + '">' + esc(value) + '</option>').join("");
  $("#globalEligibilityFilter").innerHTML = '<option value="">All</option>' + eligibilityStates.map((value) => '<option value="' + esc(value) + '">' + esc(titleCase(value)) + '</option>').join("");
  $("#globalOpportunityFilter").innerHTML = '<option value="">All</option>' + opportunityTypes.map((value) => '<option value="' + esc(value) + '">' + esc(titleCase(value)) + '</option>').join("");

  const taskStatuses = Array.from(new Set(companies.flatMap((company) => (company.research_tasks || []).map((task) => task.task_status || "OPEN")))).sort();
  $("#researchStatusFilter").innerHTML = '<option value="">All task states</option>' + taskStatuses.map((value) => '<option value="' + esc(value) + '">' + esc(titleCase(value)) + '</option>').join("");
}

function renderAll() {
  updateFilterResultLabel();
  renderKpis();
  renderOpportunityChart();
  renderEligibilityVisual();
  renderConfidenceVisual();
  renderOverviewMatrix();
  renderResearchStateVisual();
  renderCompanyExplorer();
  renderResearchKpis();
  renderResearchTable();
}

function clearGlobalFilters() {
  state.filters = {
    stratum: "",
    state: "",
    confidence: "",
    eligibility: "",
    opportunity: ""
  };
  $("#globalStratumFilter").value = "";
  $("#globalStateFilter").value = "";
  $("#globalConfidenceFilter").value = "";
  $("#globalEligibilityFilter").value = "";
  $("#globalOpportunityFilter").value = "";
  renderAll();
}

function bindEvents() {
  $$(".page-tab").forEach((button) => {
    button.addEventListener("click", () => setView(button.dataset.view));
  });

  [
    ["globalStratumFilter", "stratum"],
    ["globalStateFilter", "state"],
    ["globalConfidenceFilter", "confidence"],
    ["globalEligibilityFilter", "eligibility"],
    ["globalOpportunityFilter", "opportunity"]
  ].forEach(([id, key]) => {
    $("#" + id).addEventListener("change", (event) => {
      state.filters[key] = event.target.value;
      renderAll();
    });
  });

  $("#clearFilters").addEventListener("click", clearGlobalFilters);

  $("#overviewCompanySearch").addEventListener("input", (event) => {
    state.overviewSearch = event.target.value;
    renderOverviewMatrix();
  });

  $("#companySearch").addEventListener("input", (event) => {
    state.companySearch = event.target.value;
    renderCompanyExplorer();
  });

  $("#researchSearch").addEventListener("input", (event) => {
    state.researchSearch = event.target.value;
    renderResearchKpis();
    renderResearchTable();
  });

  $("#researchPriorityFilter").addEventListener("change", (event) => {
    state.researchPriority = event.target.value;
    renderResearchKpis();
    renderResearchTable();
  });

  $("#researchStatusFilter").addEventListener("change", (event) => {
    state.researchStatus = event.target.value;
    renderResearchKpis();
    renderResearchTable();
  });

  $("#drawerClose").addEventListener("click", closeDrawer);
  $("#drawerBackdrop").addEventListener("click", closeDrawer);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeDrawer();
  });
}

async function init() {
  bindEvents();
  try {
    const response = await fetch("data/sme_etoi.json", { cache: "no-store" });
    if (!response.ok) throw new Error("HTTP " + response.status);
    state.data = await response.json();

    $("#snapshotLabel").textContent =
      "Snapshot · " + (state.data.meta.source_snapshot_date || "current repository state");

    populateGlobalFilters();
    renderAll();
  } catch (error) {
    console.error("Failed to load SME-ETOI web data", error);
    $("#errorState").hidden = false;
  }
}

init();
