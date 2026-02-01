import { fetchRoot, fetchNext } from "./api.js";
import { getState, applyEffects, resetState, snapshotState } from "./state.js";

const el = (id) => document.getElementById(id);

const ui = {
    level: el("node-level"),
    prompt: el("node-prompt"),
    context: el("node-context"),
    choices: el("node-choices"),
    worldstate: el("world-state"),
    reset: el("node-reset"),
    leader: el("node-leader"),
    year: el("node-year"),
    loadingOverlay: el("loading-overlay"),
};

function showLoading() {
    ui.loadingOverlay?.classList.remove("hidden");
}

function hideLoading() {
    ui.loadingOverlay?.classList.add("hidden");
}

let level = 1;
let runId = 1;
let year = -213; 
let history = [];
let leader = { name: "Leader" };
let context = "";

const WORLD_STATE_LABELS = {
    centralized_power: "Centralized Power",
    military_professionalism: "Military Professionalism",
    ideological_unity: "Ideological Unity",
    infromation_control: "Information Control",
    economic_scale: "Economic Scale",
    technological_innovation: "Technological Innovation",
};

function interpretValue(value) {
    if (value >= 2) return "strong";
    if (value === 1) return "improving";
    if (value === 0) return "stable";
    if (value === -1) return "declining";
    return "weak";

}

function renderState() {
    const state = getState();
    ui.worldstate.innerHTML = "";

    for (const [key, value] of Object.entries(state)) {
        const label = WORLD_STATE_LABELS[key] ?? key;
        const meaning = interpretValue(value);

        const line = document.createElement("p");
        line.className = "world-state-line";
        line.textContent = `${label}: ${meaning}`;

        ui.worldstate.appendChild(line);
    }
}

function renderNode(payload) {
    runId = payload.run_id;
    year = payload.year;
    leader = payload.leader;
    context = payload.node.context;
    level = leader.id;

    ui.leader.textContent = leader.name;
    ui.year.textContent = year;
    ui.prompt.textContent = payload.node.prompt;
    ui.context.textContent = context;

    ui.choices.innerHTML = "";
    const slots = [
        { class: "choice choice-1"},
        { class: "choice choice-2"},
        { class: "choice choice-3"},
        { class: "choice choice-4"},
    ];
    slots.forEach((slot, index) => {
        const choiceData = payload.node.choices?.[index];
        if (!choiceData) {
            return;
        }

        const a = document.createElement("a");
        a.className = slot.class;
        a.href = "results.html";
        a.textContent = choiceData.text;    

        a.addEventListener("click", (e) => {
            e.preventDefault();
            onChoose(choiceData);
        });

        ui.choices.appendChild(a);
    });
    /*
    constChoices.forEach((choiceEl, index) => {
        const choiceData = payload.node.choices[index];
        if (choiceData) {
            const a = document.createElement("a");
            a.className = choiceEl.class;
            a.href = choiceEl.href;
            a.textContent = choiceData.text;

            ui.choices.appendChild(a);
        }
    });
    */

    renderState();
}

function loadTimeLine() {
    try {
        const raw = localStorage.getItem("timeline");
        return raw ? JSON.parse(raw) : [];
    } catch (e){
        console.warn("invalid timeline data in localStorage, resetting.", e);
        localStorage.removeItem("timeline");
        return [];
    }
}

function saveTimeLine(entries) {
    localStorage.setItem('timeline', JSON.stringify(entries.slice(-20)));
}

async function onChoose(choice) {
  try {
    /* Save “current decision” so result.html can display it
    localStorage.setItem("last_result", JSON.stringify({
      year,
      leader: leader.name,
      prompt: ui.prompt.textContent,
      choice: choice.text,
      context: ui.context.textContent,
    }));

    */
    const entries = loadTimeLine();
    entries.push({
      year,
      leader: leader.name,
      prompt: ui.prompt.textContent,
      choice: choice.text,
    });
    saveTimeLine(entries);
    showLoading();

    // OPTIONAL: if you want the next node ready when returning to timeline.html
    // const nextPayload = await fetchNext({
    //   run_id: runId,
    //   year: year,
    //   leader_id: leader.id,
    //   choice_id: choice.id,
    //   history: [...history, choice.id],
    //   state: snapshotState(),
    // });

    // console.log("Fetched next payload:", nextPayload);

    // // Save next payload so timeline.html can instantly render it later (optional)
    // localStorage.setItem("next_payload", JSON.stringify(nextPayload));

    // ✅ Redirect
    window.location.href = "result.html";
  } finally {
    hideLoading();
  }
}


async function startNewRun() {
    showLoading();
    resetState();
    history = [];

    const rootPayload = await fetchRoot();
    renderNode(rootPayload);
    console.log("Starting new run...");
    hideLoading();
}

// Don't initialize app until redirected to timeline.html and we are not redirecting from result.html
if (window.location.pathname.endsWith("timeline.html")) {
    await startNewRun();
}
