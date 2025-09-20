import os
import tempfile
import unittest

from productivity_manager.database.db_manager import DBManager
from productivity_manager.modules.todo_manager import TodoManager


class TestTodoCRUD(unittest.TestCase):
    def test_todo_crud(self):
        with tempfile.TemporaryDirectory() as td:
            db = DBManager(os.path.join(td, 'test.db'))
            db.initialize()
            tm = TodoManager(db)

            tid = tm.add_todo("Test", "Desc", priority="High", category="Work")
            self.assertTrue(tid > 0)

            todo = tm.get_todo(tid)
            self.assertTrue(todo and todo['title'] == 'Test')

            tm.update_todo(tid, title="Updated")
            todo = tm.get_todo(tid)
            self.assertTrue(todo and todo['title'] == 'Updated')

            tm.set_completed(tid, True)
            todo = tm.get_todo(tid)
            self.assertTrue(todo and todo['completed'] == 1)

            tm.delete_todo(tid)
            self.assertIsNone(tm.get_todo(tid))


if __name__ == '__main__':
    unittest.main()
