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

const lineE1 = document.getElementById('timeline');
const figureE1 = document.getElementById('h-figure');
const choiceEl = document.getElementById('h-choice');
const effectE1 = document.getElementById('h-effect');

function setHighLight(entry) {
    figureE1.textContent = entry?.leader ?? "This is the present.";
    choiceEl.textContent = entry?.choice ?? "This is the present.";
    effectE1.textContent = entry?.prompt ?? "This is the present.";
}

function renderTimeLine(entries) {
    lineE1.innerHTML = "";
    if (!entries.length) {
        const b = document.createElement('button');
        b.className = "node end active";
        b.setAttribute("aria-label", "No history yet");
        b.title = "No decision yet"
        lineE1.appendChild(b);
        setHighLight(null);
        return;
    }
    
    entries.forEach((entry, index) => {
        const b = document.createElement("button");

        // Past nodes are filled
        b.className = "node visited";

        // Most recent node is active (gold)
        if (index === entries.length - 1) {
            b.classList.add("active");
        }

        b.setAttribute("aria-label", `Node ${index + 1}: ${entry.choice}`);
        b.title = entry.choice;

        b.addEventListener("click", () => {
            document.querySelectorAll(".node").forEach(n => n.classList.remove("active"));
            b.classList.add("active");
            setHighLight(entry);
        });

        lineE1.appendChild(b);
    });


    const end = document.createElement('button');
    end.className = "node end";
    end.setAttribute("aria-label", "Current timeline");
    end.title = "Current decision point"
    end.addEventListener('click', () => {
        document.querySelectorAll('.node').forEach(n => n.classList.remove('active'));
        end.classList.add('active');
        setHighLight(null);
    });
    lineE1.appendChild(end);
    setHighLight(entries[entries.length - 1]);
}

renderTimeLine(loadTimeLine());
