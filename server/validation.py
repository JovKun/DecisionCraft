from typing import Any, Dict, List, Optional, Tuple

ALLOWED_EFFECT_KEYS = {
    "centralized_ power",
    "military_proessionalism",
    "ideological_unity",
    "economic_scale",
    "technological_innovation",
}

EFFECT_MIN = -5
EFFECT_MAX = 5

def _is_str_list(x: any) -> bool:
    return isinstance(x, list) and all(isinstance(i, str) for i in x)

def validate_node_payload(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    # Check payload is a dictionary
    if not isinstance(payload, dict):
        return False, ["Payload must be a dictionary."]
    
    # Validate 'run_id' field
    if not isinstance(payload.get("run_id"), (str, int)):
        errors.append("Field 'run_id' must be a string or integer.")

    # Validate 'year' field
    if not isinstance(payload.get("year"), int):
        errors.append("Field 'year' must be an integer.")

    # Leader
    leader = payload.get("leader")
    if not isinstance(leader, dict):
        errors.append("Field 'leader' must be a dictionary.")
    else:
        if not isinstance(leader.get("id"), int) or not leader["id"]:
            errors.append("missing/invalid 'leader.id' field.")

        if not isinstance(leader.get("name"), str) or not leader["name"]:
            errors.append("missing/invalid 'leader.name' field.")
    
    # node
    node = payload.get("node")
    if not isinstance(node, dict):
        errors.append("Field 'node' must be a dictionary.")
        return False, errors
    
    # prompt
    if not isinstance(node.get("prompt"), str) or not node["prompt"].strip():
        errors.append("missing/invalid 'node.prompt' field.")

    #context
    context = node.get("context")
    if context is None:
        errors.append("missing 'node.context'") 
    elif not isinstance(context, str):
        errors.append("Field 'node.context' must be a string.")
        return False, errors
    
    #choices
    choices = node.get("choices")
    if not isinstance(choices, list) or len(choices)<2 or len(choices)>4:
        errors.append("Field 'node.choices' must be a list with 2-4 items.")
        return False, errors
    
    for i, choice in enumerate(choices):
        if not isinstance(choice, dict):
            errors.append(f"Choice at index {i} must be a dictionary.")
            continue
        
        if not isinstance(choice.get("id"), str) or not choice["id"]:
            errors.append(f"missing/invalid 'node.choices[{i}].id' field.")

        if not isinstance(choice.get("label"), str) or not choice["label"].strip():
            errors.append(f"missing/invalid 'node.choices[{i}].label' field.")

        effects = choice.get("effects")
        if not isinstance(effects, dict):
            errors.append(f"Field 'node.choices[{i}].effects' must be a dictionary.")
            continue

        for key, value in effects.items():
            if key not in ALLOWED_EFFECT_KEYS:
                errors.append(f"Invalid effect key '{key}' in 'node.choices[{i}].effects'.")
            if not isinstance(value, int) or not (EFFECT_MIN <= value <= EFFECT_MAX):
                errors.append(f"Effect '{key}' in 'node.choices[{i}].effects' must be an integer between {EFFECT_MIN} and {EFFECT_MAX}.")
            
            else:
                if value < EFFECT_MIN or value > EFFECT_MAX:
                    errors.append(f"Effect '{key}' in 'node.choices[{i}].effects' must be between {EFFECT_MIN} and {EFFECT_MAX}.")
    
    return len(errors) == 0, errors

if __name__ == "__main__":
    sample_payload = { 
        "run_id": 1,
        "year": -334,
        "leader": {
            "id": 1,
            "name": "Alexander the Great"
        },
        "node": {
            "id": 1,
            "prompt": "You are Alexander the Great in 334 BCE. You have just crossed into Asia Minor with your army, beginning your campaign against the Persian Empire. What will you do next?",
            "context": "In 334 BCE, Alexander the Great, newly crowned King of Macedon, leads his army across the Hellespont into Asia Minor, launching his campaign against the Persian Empire.",
            "choices": [
            {
                "id": "choice_1",
                "text": "1. Launch a campaign to invade Persia, seeking to fulfill your father's ambitions and expand your empire."
            },
            {
                "id": "choice_2",
                "text": "2. Strengthen your position in Greece through diplomacy, forging alliances and consolidating power before engaging in further military campaigns."
            },
            {
                "id": "choice_3",
                "text": "3. Focus on internal reforms within Macedon to stabilize your rule and improve administration, delaying any plans for foreign conquest."       
            }
            ]
        }
    }
    
    res = validate_node_payload(sample_payload)
    print(res);