const promptEl = document.getElementById("prompt");
const submitBtn = document.getElementById("submitBtn");
const clearBtn = document.getElementById("clearBtn");
const statusEl = document.getElementById("status");

const analysisEl = document.getElementById("analysis");
const modeBadgeEl = document.getElementById("modeBadge");
const validityBadgeEl = document.getElementById("validityBadge");
const sourceBadgeEl = document.getElementById("sourceBadge");
const taskSystemEl = document.getElementById("taskSystem");
const activeFormsEl = document.getElementById("activeForms");
const canonicalSetupEl = document.getElementById("canonicalSetup");
const structuralCommitmentsEl = document.getElementById("structuralCommitments");
const validationGatesEl = document.getElementById("validationGates");
const fullJsonEl = document.getElementById("fullJson");

function clearPromptBox() {
  document.querySelectorAll("textarea").forEach((el) => {
    el.value = "";
    el.textContent = "";
  });
  const first = document.querySelector("textarea");
  if (first) first.focus();
}

const API_URL = "http://127.0.0.1:8003/chat";
let previousMessage = "";
let sessionId = localStorage.getItem("epra_session_id") || null;

function pretty(value) {
  return JSON.stringify(value, null, 2);
}

function setStatus(text, mode = "idle") {
  statusEl.textContent = text;
  statusEl.className = `status ${mode}`;
}

function setBadge(el, text, kind) {
  el.textContent = text;
  el.className = `badge ${kind || "neutral"}`;
}

function validityKind(label) {
  if (!label) return "neutral";
  const key = label.toLowerCase();
  if (key.includes("valid")) return "valid";
  if (key.includes("drifted")) return "drifted";
  if (key.includes("weak")) return "weak";
  if (key.includes("pseudo")) return "pseudo";
  if (key.includes("error")) return "error";
  return "neutral";
}

function clearOutput() {
  analysisEl.textContent = "Submit a prompt to see the EPRA output.";
  analysisEl.classList.add("empty");

  setBadge(modeBadgeEl, "mode: —", "neutral");
  setBadge(validityBadgeEl, "No result", "neutral");
  setBadge(sourceBadgeEl, "validation: —", "neutral");

  taskSystemEl.textContent = "—";
  activeFormsEl.textContent = "—";
  canonicalSetupEl.textContent = "—";
  structuralCommitmentsEl.textContent = "—";
  validationGatesEl.textContent = "—";
  fullJsonEl.textContent = "—";
}

async function runAnalysis() {
  const message = promptEl.value.trim();
  if (!message) {
    setStatus("Enter a prompt first.", "warn");
    return;
  }

  submitBtn.disabled = true;
  setStatus("Running EPRA analysis...", "loading");

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    const data = await res.json();
    const metadata = data.metadata || {};
    const mode = metadata.mode || metadata.routing?.task_type || "UNKNOWN";
    const validity = metadata.validity || {};
    const canonical = metadata.canonical_setup || {};
    const commitments = canonical.structural_commitments || {};

    analysisEl.textContent = data.analysis || "(no analysis returned)";
    analysisEl.classList.remove("empty");

    const validityText = data.validity_status || validity.label || "Unknown";
    setBadge(modeBadgeEl, `mode: ${mode}`, "neutral");
    setBadge(validityBadgeEl, validityText, validityKind(validityText));

    const source = validity.validation_source || "—";
    setBadge(sourceBadgeEl, `validation: ${source}`, source === "canonical" ? "valid" : "neutral");

    taskSystemEl.textContent = metadata.task_system || "—";
    activeFormsEl.textContent = (metadata.active_forms || []).join(", ") || "—";

    canonicalSetupEl.textContent = pretty(canonical);
    structuralCommitmentsEl.textContent = pretty(commitments);
    validationGatesEl.textContent = pretty(validity.gates || {});
    fullJsonEl.textContent = pretty(data);

    setStatus("Analysis complete.", "done");
  } catch (err) {
    clearOutput();
    setBadge(validityBadgeEl, "Error", "error");
    setBadge(sourceBadgeEl, "validation: —", "neutral");
    analysisEl.textContent = `Request failed.\n\n${err.message}`;
    analysisEl.classList.remove("empty");
    setStatus("Request failed.", "error");
  } finally {
    submitBtn.disabled = false;
  }
}

document.querySelectorAll(".example-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    promptEl.value = btn.dataset.example || "";
    promptEl.focus();
  });
});

submitBtn.addEventListener("click", runAnalysis);

clearBtn.addEventListener("click", () => {
  promptEl.value = "";
  clearOutput();
  setStatus("Ready", "idle");
});

promptEl.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
    runAnalysis();
  }
});

clearOutput();

// EPRA v5 UI hard clear patch
(function () {
  function hardClearPromptBox() {
    document.querySelectorAll("textarea, input[type='text'], [contenteditable='true']").forEach((el) => {
      el.value = "";
      el.textContent = "";
      el.innerText = "";
      el.dispatchEvent(new Event("input", { bubbles: true }));
      el.dispatchEvent(new Event("change", { bubbles: true }));
    });

    const box = document.querySelector("textarea") || document.querySelector("input[type='text']") || document.querySelector("[contenteditable='true']");
    if (box) box.focus();
  }

  document.addEventListener("click", function (ev) {
    const target = ev.target;
    const text = (target && target.innerText ? target.innerText : "").toLowerCase();

    if (text.includes("run ep analysis")) {
      setTimeout(hardClearPromptBox, 0);
      setTimeout(hardClearPromptBox, 100);
      setTimeout(hardClearPromptBox, 500);
      setTimeout(hardClearPromptBox, 1200);
    }
  }, false);

  window.epraHardClearPromptBox = hardClearPromptBox;
})();

// EPRA v5 hard UI continuity patch
(function () {
  const SESSION_KEY = "epra_session_id";

  function clearAllPromptBoxes() {
    document.querySelectorAll("textarea, input[type='text'], [contenteditable='true']").forEach((el) => {
      if ("value" in el) el.value = "";
      el.textContent = "";
      el.innerText = "";
      el.dispatchEvent(new Event("input", { bubbles: true }));
      el.dispatchEvent(new Event("change", { bubbles: true }));
    });
    const box = document.querySelector("textarea") || document.querySelector("input[type='text']");
    if (box) box.focus();
  }

  const originalFetch = window.fetch.bind(window);

  window.fetch = async function(input, init = {}) {
    const url = typeof input === "string" ? input : input?.url || "";

    if (url.includes("/chat") && init && init.body) {
      try {
        const payload = JSON.parse(init.body);
        const sid = localStorage.getItem(SESSION_KEY);
        if (sid && !payload.session_id) payload.session_id = sid;
        init.body = JSON.stringify(payload);
        clearAllPromptBoxes();
      } catch (e) {}
    }

    const response = await originalFetch(input, init);

    if (url.includes("/chat")) {
      try {
        const cloned = response.clone();
        cloned.json().then((data) => {
          const sid = data?.metadata?.session?.session_id;
          if (sid) localStorage.setItem(SESSION_KEY, sid);
          clearAllPromptBoxes();
        }).catch(() => {});
      } catch (e) {}
    }

    return response;
  };

  window.epraClear = clearAllPromptBoxes;
})();
