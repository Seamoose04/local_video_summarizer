import sqlite3
import os

VIDEO_PATH = "video"

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
    frame INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL,
    description TEXT,
    embedding_path TEXT
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

    def upload_frame(self, ts: float, description: str):
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute("""
INSERT INTO frames (ts, description, embedding_path)
VALUES (?, ?, "")
            """, (ts, description))