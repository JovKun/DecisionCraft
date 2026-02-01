from typing import Dict, Any

def fallback_payload(run_id: str, year: int, leader_id: str, leader_name: str) -> Dict[str, Any]:
    return {
        "run_id": run_id,
        "year": year,
        "leader": {"id": leader_id, "name": leader_name},
        "node": {
            "id": "fallback",
            "prompt": "Uncertainty clouds the court and camp. A cautious course is needed to preserve stability.",
            "context": [
                "Information is incomplete; acting rashly may backfire.",
                "Resources and loyalty must be maintained to survive the next season.",
                "A measured response can prevent avoidable collapse."
            ],
            "choices": [
                {
                    "id": "fallback_consolidate",
                    "label": "Consolidate authority and resources",
                    "effects": {"centralized_power": 1, "economic_scale": 1}
                },
                {
                    "id": "fallback_deescalate",
                    "label": "De-escalate and seek temporary stability",
                    "effects": {"ideological_unity": 1, "information_control": -1}
                }
            ]
        }
    }