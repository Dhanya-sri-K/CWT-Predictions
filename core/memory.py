import sqlite3
import json
import os
from loguru import logger

class PersistentMemory:
    def __init__(self, db_path="data/memory.db"):
        self.db_path = db_path
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT,
                role TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS state (
                agent_name TEXT PRIMARY KEY,
                state_data TEXT
            )
            """)

    def add_message(self, agent_name, role, content):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO messages (agent_name, role, content) VALUES (?, ?, ?)", (agent_name, role, content))

    def get_history(self, agent_name, limit=10):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT role, content FROM messages WHERE agent_name = ? ORDER BY timestamp DESC LIMIT ?", (agent_name, limit))
            rows = cursor.fetchall()
            return [{"role": row[0], "content": row[1]} for row in reversed(rows)]

    def save_state(self, agent_name, state_data):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO state (agent_name, state_data) VALUES (?, ?)", (agent_name, json.dumps(state_data)))

    def load_state(self, agent_name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT state_data FROM state WHERE agent_name = ?", (agent_name,))
            row = cursor.fetchone()
            return json.loads(row[0]) if row else {}
