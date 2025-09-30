from pathlib import Path
import json
import hashlib
from db_functions import DB

def update_stage(id: str, stage: str):
    db = DB(id)
    db.update_stat("stage", stage)

def url_to_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:12]  # short but unique