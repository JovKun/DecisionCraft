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

function renderState() {
    ui.worldstate.textContent = JSON.stringify(getState(), null, 2);
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

    // Loop through choices and choice elements together
    const constChoices = [
        {text: "Choice 1", class: "choice choice-1", href: "result.html"},
        {text: "Choice 2", class: "choice choice-2", href: "result.html"},
        {text: "Choice 3", class: "choice choice-3", href: "result.html"},
        {text: "Choice 4", class: "choice choice-4", href: "result.html"}
    ]

    ui.choices.innerHTML = "";
    constChoices.forEach((choiceEl, index) => {
        const choiceData = payload.node.choices[index];
        if (choiceData) {
            const a = document.createElement("a");
            a.className = choiceEl.class;
            a.href = choiceEl.href;
            a.textContent = choiceEl.text;

            ui.choices.appendChild(a);
        }
    });

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
