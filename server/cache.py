import json
import hashlib
from typing import Any, Dict, List

def stable_hash(obj: Any) -> str:
    serialized = json.dumps(obj, sort_keys=True, separators=("," , ":")).encode('utf-8')
    return hashlib.sha256(serialized).hexdigest()

def make_cache_key(run_id:str, year: int, leader_id: str, state: Dict[str, Any], history: List[str]) -> str:
    key_components = {
        "run_id": run_id,
        "year": year,
        "leader_id": leader_id,
        "state_hash": state,
        "history_hash": history
    }
    return stable_hash(key_components)