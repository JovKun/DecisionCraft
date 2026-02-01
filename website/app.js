import { fetchRoot, fetchNext } from "./api.js";
import { getState, applyEffects, resetState, snapshotState } from "./state.js";

const el = (id) => document.getElementById(id);

const ui = {
    prompt: el("node-prompt"),
    choices: el("choices"),
    context: el("context-title"),
    worldstate: el("world-state"),
    reset: el("node-reset"),
    leader: el("figure-name"),
    year: el("node-subtitle"),
    loadingOverlay: el("loading-overlay"),
};

function showLoading() {
    ui.loadingOverlay?.classList.remove("hidden");
}

function hideLoading() {
    ui.loadingOverlay?.classList.add("hidden");
}

let runId = 1;
let year = -213; 
let history = [];
let leader = { name: "Leader" };
let context = "";

function renderState() {
    ui.worldstate.textContent = JSON.stringify(getState(), null, 2);
}

function renderNode(payload) {
    runId = payload.run_id;
    year = payload.year;
    leader = payload.leader;
    context = payload.node.context;

    ui.leader.textContent = leader.name;
    ui.year.textContent = `Year: ${year}`;
    ui.prompt.textContent = payload.node.prompt;
    ui.context.textContent = context;

    //Choice Buttons
    ui.choices.innerHTML = "";
    for (const choice of payload.node.choices || []) {
        const btn = document.createElement("button");
        btn.textContent = choice.text;
        btn.onclick = () => onChoose(choice);
        ui.choices.appendChild(btn);
    }

    renderState();
}

async function onChoose(choice) {
    applyEffects(choice.effects);
    history.push(choice.id);
    renderState();
    showLoading();

    const nextPayload = await fetchNext({
        run_id: runId,
        year: year,
        leader: leader,
        history: history,
        choice_id: choice.id,
        state: snapshotState(),
        history: history,
    });

    renderNode(nextPayload);
    hideLoading();
}

async function startNewRun() {
    showLoading();
    resetState();
    history = [];

    const rootPayload = await fetchRoot();
    renderNode(rootPayload);
    hideLoading();
}

// Don't initialize app until redirected to timeline.html
if (window.location.pathname.endsWith("timeline.html")) {
    startNewRun();
}
