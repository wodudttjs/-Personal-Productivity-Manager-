import time
from datetime import datetime
from typing import Optional

from database.db_manager import DBManager


class Timer:
    def __init__(self, db: DBManager, task_id: Optional[int] = None):
        self.db = db
        self.task_id = task_id
        self._start_ts: Optional[float] = None
        self._elapsed: float = 0.0

    def start(self):
        if self._start_ts is None:
            self._start_ts = time.time()

    def stop(self, notes: str = "") -> int:
        if self._start_ts is None:
            return 0
        now = time.time()
        self._elapsed += now - self._start_ts
        self._start_ts = None
        seconds = int(self._elapsed)
        # persist entry
        start_iso = datetime.fromtimestamp(now - self._elapsed).isoformat(timespec='seconds')
        end_iso = datetime.fromtimestamp(now).isoformat(timespec='seconds')
        cur = self.db.execute(
            """
            INSERT INTO time_entries (task_id, start_time, end_time, duration_seconds, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (self.task_id, start_iso, end_iso, seconds, notes),
        )
        self._elapsed = 0.0
        return int(cur.lastrowid)

    def reset(self):
        self._start_ts = None
        self._elapsed = 0.0

    def elapsed_seconds(self) -> int:
        if self._start_ts is None:
            return int(self._elapsed)
        return int(self._elapsed + (time.time() - self._start_ts))

