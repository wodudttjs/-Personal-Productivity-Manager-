import os
import time
import tempfile
import unittest

from database.db_manager import DBManager
from modules.time_tracker import Timer


class TestTimer(unittest.TestCase):
    def test_timer_basic(self):
        with tempfile.TemporaryDirectory() as td:
            db = DBManager(os.path.join(td, 'test.db'))
            db.initialize()
            t = Timer(db)
            t.start()
            time.sleep(0.05)
            entry_id = t.stop()
            self.assertTrue(entry_id > 0)
            rows = db.query("SELECT * FROM time_entries")
            self.assertEqual(len(rows), 1)
            self.assertTrue(rows[0]["duration_seconds"] >= 0)


if __name__ == '__main__':
    unittest.main()
