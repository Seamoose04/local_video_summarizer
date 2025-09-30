from pathlib import Path
import json
import hashlib

def update_json_stage(json_path: str | Path, stage: str):
    json_path = Path(json_path)
    
    # Load existing data
    if not json_path.exists():
        raise FileNotFoundError(f"{json_path} does not exist")
    
    with open(json_path, "r") as f:
        data = json.load(f)

    # Update and write back
    data["stage"] = stage
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

def url_to_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:12]  # short but unique