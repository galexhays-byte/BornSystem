const API_BASE = "http://localhost:8000";
const output = document.getElementById("output");
const outputStatus = document.getElementById("outputStatus");
const workflowIdInput = document.getElementById("workflowId");
const workflowTargetInput = document.getElementById("workflowTarget");
const nodeActionInput = document.getElementById("nodeAction");
const nodeTargetInput = document.getElementById("nodeTarget");
const nodeNameInput = document.getElementById("nodeName");
const goalInput = document.getElementById("goalInput");
const toolSelect = document.getElementById("toolSelect");
const presetSelect = document.getElementById("presetSelect");
const toolDescription = document.getElementById("toolDescription");
const toolArgsInput = document.getElementById("toolArgsInput");
const historyList = document.getElementById("historyList");
const scanDataInput = document.getElementById("scanDataInput");
const useLastResultBtn = document.getElementById("useLastResultBtn");
let toolMetadata = {};
let lastResponse = null;

function setStatus(text, type = "ready") {
  outputStatus.textContent = text;
  outputStatus.className = `status-label ${type}`;
}

function formatJSON(data) {
  return JSON.stringify(data, null, 2);
}

function showOutput(data) {
  output.textContent = formatJSON(data);
  lastResponse = data;
}

async function requestJson(url, options = {}) {
  setStatus("Loading…", "loading");
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || data.error || "Request failed");
  }
  return data;
}

async function refreshTools() {
  try {
    const data = await requestJson(`${API_BASE}/api/automation/tools`);
    toolMetadata = data.tools || {};
    populateToolSelect(toolMetadata);
    showOutput(data);
    setStatus("Tools loaded", "success");
  } catch (err) {
    showOutput({ error: err.message });
    setStatus("Tool load failed", "error");
  }
}

function populateToolSelect(tools) {
  toolSelect.innerHTML = "";
  const entries = Object.entries(tools || {});
  if (entries.length === 0) {
    toolSelect.innerHTML = `<option value="">No tools available</option>`;
    toolDescription.textContent = "No automation tools were returned by the server.";
    presetSelect.innerHTML = `<option value="">No presets</option>`;
    presetSelect.disabled = true;
    return;
  }

  entries.forEach(([name]) => {
    const option = document.createElement("option");
    option.value = name;
    option.textContent = name;
    toolSelect.appendChild(option);
  });

  const firstToolName = entries[0][0];
  updateToolPanel(firstToolName);
}

function populatePresetSelect(presets) {
  presetSelect.innerHTML = "";
  const entries = Object.entries(presets || {});
  const defaultOption = document.createElement("option");
  defaultOption.value = "";
  defaultOption.textContent = entries.length ? "Select a preset" : "No presets available";
  presetSelect.appendChild(defaultOption);

  if (!entries.length) {
    presetSelect.disabled = true;
    return;
  }

  presetSelect.disabled = false;
  entries.forEach(([presetName]) => {
    const option = document.createElement("option");
    option.value = presetName;
    option.textContent = presetName;
    presetSelect.appendChild(option);
  });
}

function updateToolPanel(toolName) {
  const tool = toolMetadata[toolName];
  if (!tool) {
    toolDescription.textContent = "Select a tool to view its description.";
    populatePresetSelect({});
    return;
  }
  toolDescription.textContent = tool.description || "";
  populatePresetSelect(tool.presets || {});
  presetSelect.value = "";
  toolArgsInput.value = "";
}

function updateToolDescription() {
  const selected = toolSelect.value;
  if (!selected) {
    toolDescription.textContent = "Select a tool to view its description.";
    populatePresetSelect({});
    return;
  }
  updateToolPanel(selected);
}

function parseJsonArg(text) {
  if (!text.trim()) return {};
  return JSON.parse(text);
}

function applyPreset(presetName) {
  const selectedTool = toolSelect.value;
  if (!selectedTool || !presetName) {
    return;
  }

  const tool = toolMetadata[selectedTool];
  const presets = tool?.presets || {};
  const presetValue = presets[presetName];
  if (!presetValue) {
    return;
  }

  toolArgsInput.value = JSON.stringify(presetValue, null, 2);
  setStatus(`Loaded preset ${presetName}`, "success");
}

async function executeTool() {
  const toolName = toolSelect.value;
  if (!toolName) {
    showOutput({ error: "Please select a tool first." });
    setStatus("Validation error", "error");
    return;
  }

  let args;
  try {
    args = parseJsonArg(toolArgsInput.value);
  } catch (err) {
    showOutput({ error: "Tool arguments must be valid JSON." });
    setStatus("Validation error", "error");
    return;
  }

  try {
    const data = await requestJson(`${API_BASE}/api/automation/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tool_name: toolName, args }),
    });
    showOutput(data);
    setStatus("Tool executed", "success");
  } catch (err) {
    showOutput({ error: err.message });
    setStatus("Tool execution failed", "error");
  }
}

function useLastResult() {
  if (!lastResponse) {
    showOutput({ error: "No last response available to use." });
    setStatus("No response", "error");
    return;
  }
  scanDataInput.value = formatJSON(lastResponse);
  setStatus("Last result loaded into scan data", "success");
}

async function generateScript() {
  let scanData;
  try {
    scanData = parseJsonArg(scanDataInput.value);
  } catch (err) {
    showOutput({ error: "Scan data must be valid JSON." });
    setStatus("Validation error", "error");
    return;
  }
  if (!scanData || typeof scanData !== "object") {
    showOutput({ error: "Enter scan result JSON before generating a script." });
    setStatus("Validation error", "error");
    return;
  }

  try {
    const data = await requestJson(`${API_BASE}/api/automation/generate_script`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ scan_result: scanData }),
    });
    showOutput(data);
    setStatus("Generated follow-up script", "success");
  } catch (err) {
    showOutput({ error: err.message });
    setStatus("Script generation failed", "error");
  }
}

async function refreshHistory() {
  try {
    const data = await requestJson(`${API_BASE}/api/automation/history`);
    populateHistoryList(data.runs || []);
    setStatus("History refreshed", "success");
  } catch (err) {
    showOutput({ error: err.message });
    setStatus("History refresh failed", "error");
  }
}

function populateHistoryList(runs) {
  historyList.innerHTML = "";
  if (!Array.isArray(runs) || runs.length === 0) {
    const noRuns = document.createElement("li");
    noRuns.className = "history-item empty";
    noRuns.textContent = "No automation history available.";
    historyList.appendChild(noRuns);
    return;
  }

  runs.forEach((run) => {
    const item = document.createElement("li");
    item.className = "history-item";
    item.textContent = `${run.created_at} · ${run.goal || run.run_id} · ${run.status}`;
    item.dataset.runId = run.run_id;
    item.addEventListener("click", () => loadHistoryRun(run.run_id, item));
    historyList.appendChild(item);
  });
}

async function loadHistoryRun(runId, itemElement) {
  try {
    const data = await requestJson(`${API_BASE}/api/automation/history/${encodeURIComponent(runId)}`);
    showOutput(data);
    setStatus(`Loaded run ${runId}`, "success");
    document.querySelectorAll(".history-item.active").forEach((el) => el.classList.remove("active"));
    if (itemElement) itemElement.classList.add("active");
  } catch (err) {
    showOutput({ error: err.message });
    setStatus("Load run failed", "error");
  }
}

async function listNodes() {
  try {
    const data = await requestJson(`${API_BASE}/api/nodes/list`);
    showOutput(data);
    setStatus("Nodes listed", "success");
  } catch (err) {
    showOutput({ error: err.message });
    setStatus("Node listing failed", "error");
  }
}

async function listWorkflows() {
  try {
    const data = await requestJson(`${API_BASE}/api/workflows/list`);
    showOutput(data);
    setStatus("Workflows listed", "success");
  } catch (err) {
    showOutput({ error: err.message });
    setStatus("Workflow listing failed", "error");
  }
}

async function executeWorkflow() {
  const workflowId = workflowIdInput.value.trim();
  const target = workflowTargetInput.value.trim();
  if (!workflowId) {
    showOutput({ error: "Workflow ID is required." });
    setStatus("Validation error", "error");
    return;
  }

  try {
    const data = await requestJson(`${API_BASE}/api/workflows/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ workflow_id: workflowId, target: target || null }),
    });
    showOutput(data);
    setStatus("Workflow executed", "success");
  } catch (err) {
    showOutput({ error: err.message });
    setStatus("Workflow execution failed", "error");
  }
}

async function executeNodeAction() {
  const action = nodeActionInput.value.trim();
  const target = nodeTargetInput.value.trim();
  const nodeName = nodeNameInput.value.trim();
  if (!action || !target) {
    showOutput({ error: "Node action and target are required." });
    setStatus("Validation error", "error");
    return;
  }

  try {
    const data = await requestJson(`${API_BASE}/api/nodes/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action, target, node_name: nodeName || null }),
    });
    showOutput(data);
    setStatus("Node action executed", "success");
  } catch (err) {
    showOutput({ error: err.message });
    setStatus("Node execution failed", "error");
  }
}

async function generatePlan() {
  const goal = goalInput.value.trim();
  if (!goal) {
    showOutput({ error: "Automation goal is required." });
    setStatus("Validation error", "error");
    return;
  }

  try {
    const data = await requestJson(`${API_BASE}/api/automation/plan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goal }),
    });
    showOutput(data);
    setStatus("Plan generated", "success");
  } catch (err) {
    showOutput({ error: err.message });
    setStatus("Plan generation failed", "error");
  }
}

async function runAutomation() {
  const goal = goalInput.value.trim();
  if (!goal) {
    showOutput({ error: "Automation goal is required." });
    setStatus("Validation error", "error");
    return;
  }

  try {
    const data = await requestJson(`${API_BASE}/api/automation/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goal, node_name: null }),
    });
    showOutput(data);
    setStatus("Automation executed", "success");
  } catch (err) {
    showOutput({ error: err.message });
    setStatus("Automation failed", "error");
  }
}

function handleError(error) {
  showOutput({ error: error.message });
  setStatus("Request failed", "error");
}

document.getElementById("healthBtn").addEventListener("click", async () => {
  try {
    const data = await requestJson(`${API_BASE}/health`);
    showOutput(data);
    setStatus("Backend healthy", "success");
  } catch (err) {
    handleError(err);
  }
});

document.getElementById("listBtn").addEventListener("click", listNodes);
document.getElementById("listWorkflowsBtn").addEventListener("click", listWorkflows);
document.getElementById("refreshToolsBtn").addEventListener("click", refreshTools);
document.getElementById("refreshHistoryBtn").addEventListener("click", refreshHistory);
document.getElementById("executeWorkflowBtn").addEventListener("click", executeWorkflow);
document.getElementById("executeNodeBtn").addEventListener("click", executeNodeAction);
document.getElementById("executeToolBtn").addEventListener("click", executeTool);
document.getElementById("useLastResultBtn").addEventListener("click", useLastResult);
document.getElementById("generatePlanBtn").addEventListener("click", generatePlan);
document.getElementById("runAutomationBtn").addEventListener("click", runAutomation);
toolSelect.addEventListener("change", updateToolDescription);
presetSelect.addEventListener("change", (event) => applyPreset(event.target.value));
document.getElementById("generateScriptBtn").addEventListener("click", generateScript);

refreshTools();
refreshHistory();
