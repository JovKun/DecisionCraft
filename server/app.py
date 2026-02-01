from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import secrets

from website.generate import generate_node

app = Flask(__name__, static_folder="/website", static_url_path="")
CORS(app)

current_leader = {
    "id": 0,
    "name" : "Hannibal Barca",
    "run_id": 1
}

@app.get("/api/root")
async def api_root():
    run_id = secrets.token_hex(4)
    cur_node = await generate_node(1, run_id)
    current_leader["id"] = 1
    current_leader["name"] = cur_node["leader"]["name"]
    current_leader["run_id"] = run_id
    return jsonify(cur_node)

@app.get("/api/next")
async def api_next():
    leader_id = int(current_leader["id"]) + 1

    out = await generate_node(leader_id, current_leader["run_id"])
    current_leader["id"] = leader_id
    current_leader["name"] = out["leader"]["name"]
    return jsonify(out)

@app.post("/api/reset")
async def api_reset():
    current_leader["id"] = 0
    current_leader["name"] = "Hannibal Barca"
    current_leader["run_id"] = 1
    return jsonify({"status": "reset"})

@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)