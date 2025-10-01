import sqlite3
import os
from typing import Literal

VIDEO_PATH = "video"

FrameType = Literal['scene', 'move']

class DB:
    def __init__(self, id: str):
        self.path = f"{VIDEO_PATH}/{id}/data.db"

        if not os.path.exists(self.path):
            with sqlite3.connect(self.path) as conn:
                cur = conn.cursor()
                cur.executescript("""
CREATE TABLE IF NOT EXISTS stats (
    stat TEXT PRIMARY KEY,
    status TEXT
);

CREATE TABLE IF NOT EXISTS frames (
    keyframe INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL,
    frame_type TEXT,
    description TEXT
);       
                """)
                conn.commit()

    def update_stat(self, stat: str, state: str):
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute("""
INSERT INTO stats (stat, status)
VALUES (?, ?)
ON CONFLICT(stat) DO UPDATE SET
    stat=excluded.stat,
    status=excluded.status
            """, (stat, state))
            conn.commit()

    def add_keyframe(self, ts: float, frame_type: FrameType):
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute("""
INSERT INTO frames (ts, frame_type)
VALUES (?, ?)
            """, (ts, frame_type))
            conn.commit()

    def get_new_keyframe(self):
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            # fetch one frame without description
            cur.execute("SELECT keyframe, ts, frame_type FROM frames WHERE description IS NULL LIMIT 1")
            return cur.fetchone()

    def update_keyframe_description(self, keyframe: int, description: str):
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute("""
UPDATE frames SET description=? WHERE keyframe=?
            """, (description, keyframe))
            conn.commit()