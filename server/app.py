from flask import Flask, jsonify, request
import secrets

from website.generate import generate_node

app = Flask(__name__)

DEFAULT_STATE = {
    "centralized_power" : 0,
    "military_professionalism" : 0,
    "ideological_unity" : 0,
    "information_control" : 0,
    "economic_scale" : 0,
    "technological_innovation" : 0
}

START = {
    "year" : -216,
    "leader" : {"id": "1", "name" : "Hannibal Barca"}
}

@app.get("/api/root")
async def api_root():
    run_id = secrets.token_hex(4)
    cur_node = await generate_node(1, run_id)
    return jsonify(cur_node)

@app.post("/api/next")
async def api_next():
    payload = request.get_json(silent=True) or {}

    run_id = payload.get("run_id")
    if not run_id:
        return jsonify({"error": "Missing run_id"}), 400

    leader_id = int(payload.get("leader_id", START["leader"]["id"]))

    out = await generate_node(leader_id, run_id)
    return jsonify(out)

if __name__ == "__main__":
    app.run(debug=True)