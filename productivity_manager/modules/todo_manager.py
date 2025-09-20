from typing import List, Optional, Dict, Any

from ..database.db_manager import DBManager


class TodoManager:
    def __init__(self, db: DBManager):
        self.db = db

    def add_todo(self, title: str, description: str = "", priority: str = "Medium", category: str = "General", due_date: Optional[str] = None) -> int:
        cur = self.db.execute(
            """
            INSERT INTO todos (title, description, priority, category, due_date, completed)
            VALUES (?, ?, ?, ?, ?, 0)
            """,
            (title, description, priority, category, due_date)
        )
        return int(cur.lastrowid)

    def update_todo(self, todo_id: int, **fields) -> None:
        if not fields:
            return
        cols = []
        vals = []
        for k, v in fields.items():
            cols.append(f"{k} = ?")
            vals.append(v)
        vals.append(todo_id)
        sql = f"UPDATE todos SET {', '.join(cols)}, updated_at = datetime('now') WHERE id = ?"
        self.db.execute(sql, vals)

    def delete_todo(self, todo_id: int) -> None:
        self.db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))

    def set_completed(self, todo_id: int, completed: bool) -> None:
        self.db.execute("UPDATE todos SET completed = ?, updated_at = datetime('now') WHERE id = ?", (1 if completed else 0, todo_id))

    def get_todo(self, todo_id: int) -> Optional[Dict[str, Any]]:
        rows = self.db.query("SELECT * FROM todos WHERE id = ?", (todo_id,))
        if not rows:
            return None
        return dict(rows[0])

    def list_todos(self, include_completed: bool = True, category: Optional[str] = None) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM todos"
        params: List[Any] = []
        clauses = []
        if not include_completed:
            clauses.append("completed = 0")
        if category:
            clauses.append("category = ?")
            params.append(category)
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY completed ASC, priority DESC, due_date IS NULL, due_date ASC, created_at DESC"
        rows = self.db.query(sql, params)
        return [dict(r) for r in rows]
