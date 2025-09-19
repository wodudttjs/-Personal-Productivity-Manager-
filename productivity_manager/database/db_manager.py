import os
import sqlite3
from types import SimpleNamespace
from typing import Iterable, Optional


class DBManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self) -> None:
        conn = self._connect()
        cur = conn.cursor()
        # Todos table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT CHECK(priority IN ('High','Medium','Low')) DEFAULT 'Medium',
                category TEXT,
                due_date TEXT,
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            )
            """
        )

        # Time entries table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS time_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                start_time TEXT,
                end_time TEXT,
                duration_seconds INTEGER,
                notes TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY(task_id) REFERENCES todos(id) ON DELETE SET NULL
            )
            """
        )

        # Indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_todos_completed ON todos(completed)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_time_task ON time_entries(task_id)")
        conn.commit()
        conn.close()

    def execute(self, sql: str, params: Iterable = ()):  # for writes
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        conn.commit()
        lastrowid = cur.lastrowid
        conn.close()
        # Return a lightweight object exposing lastrowid for compatibility
        return SimpleNamespace(lastrowid=lastrowid)

    def query(self, sql: str, params: Iterable = ()) -> Iterable[sqlite3.Row]:  # for reads
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        conn.close()
        return rows

    def close(self):
        # No persistent connection kept; nothing to close.
        return None

    # Ensure connections are not left open (helps on Windows file locks)
    def __del__(self):  # pragma: no cover - destructor behavior
        # Connections are per-operation now; nothing to do.
        pass
