import os
import sqlite3
from typing import Iterable, Optional


class DBManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def initialize(self) -> None:
        cur = self.conn.cursor()
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
        self.conn.commit()

    def execute(self, sql: str, params: Iterable = ()):  # for writes
        cur = self.conn.cursor()
        cur.execute(sql, tuple(params))
        self.conn.commit()
        return cur

    def query(self, sql: str, params: Iterable = ()) -> Iterable[sqlite3.Row]:  # for reads
        cur = self.conn.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchall()

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass

