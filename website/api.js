export async function fetchRoot() {
    console.log("Fetching root node...");
    const res = await fetch('http://localhost:5000/api/root');
    console.log(res);
    if (!res.ok) {
        throw new Error(`Failed to fetch root node: ${res.statusText}`);
    }
    return await res.json();
}

export async function fetchNext(payload) {
    const res = await fetch("http://localhost:5000/api/next", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });
    if (!res.ok) {
        throw new Error(`Failed to fetch next node: ${res.statusText}`);
    }
    return await res.json();
}