import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional

from modules.todo_manager import TodoManager


def build_todo_tab(parent, todo_manager: TodoManager):
    frame = ttk.Frame(parent)

    # Controls
    controls = ttk.Frame(frame)
    controls.pack(fill=tk.X, padx=8, pady=8)

    btn_add = ttk.Button(controls, text="Add", command=lambda: _add_task(frame, todo_manager, tree))
    btn_add.pack(side=tk.LEFT, padx=4)
    btn_edit = ttk.Button(controls, text="Edit", command=lambda: _edit_task(frame, todo_manager, tree))
    btn_edit.pack(side=tk.LEFT, padx=4)
    btn_del = ttk.Button(controls, text="Delete", command=lambda: _delete_task(todo_manager, tree))
    btn_del.pack(side=tk.LEFT, padx=4)
    btn_toggle = ttk.Button(controls, text="Toggle Complete", command=lambda: _toggle_complete(todo_manager, tree))
    btn_toggle.pack(side=tk.LEFT, padx=4)

    # Treeview for tasks
    columns = ("id", "title", "priority", "category", "due_date", "completed")
    tree = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.column("title", width=240)

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8,0), pady=(0,8))
    vsb.pack(side=tk.LEFT, fill=tk.Y, pady=(0,8))

    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        for row in todo_manager.list_todos():
            tree.insert('', tk.END, values=(row['id'], row['title'], row['priority'], row['category'], row['due_date'] or '', 'Yes' if row['completed'] else 'No'))

    frame.refresh = refresh  # type: ignore
    refresh()
    return frame


def _selected_id(tree: ttk.Treeview) -> Optional[int]:
    sel = tree.selection()
    if not sel:
        return None
    vals = tree.item(sel[0], 'values')
    return int(vals[0]) if vals else None


def _add_task(root, todo_manager: TodoManager, tree: ttk.Treeview):
    title = simpledialog.askstring("New Task", "Title:", parent=root)
    if not title:
        return
    description = simpledialog.askstring("New Task", "Description:", parent=root) or ""
    priority = simpledialog.askstring("New Task", "Priority (High/Medium/Low):", parent=root) or "Medium"
    category = simpledialog.askstring("New Task", "Category:", parent=root) or "General"
    due_date = simpledialog.askstring("New Task", "Due date (YYYY-MM-DD) or blank:", parent=root) or None
    todo_manager.add_todo(title, description, priority, category, due_date)
    root.refresh()  # type: ignore


def _edit_task(root, todo_manager: TodoManager, tree: ttk.Treeview):
    tid = _selected_id(tree)
    if not tid:
        messagebox.showinfo("Edit", "Select a task first.")
        return
    todo = todo_manager.get_todo(tid)
    if not todo:
        return
    title = simpledialog.askstring("Edit Task", "Title:", initialvalue=todo['title'], parent=root)
    if not title:
        return
    description = simpledialog.askstring("Edit Task", "Description:", initialvalue=todo.get('description',''), parent=root) or ""
    priority = simpledialog.askstring("Edit Task", "Priority (High/Medium/Low):", initialvalue=todo.get('priority','Medium'), parent=root) or "Medium"
    category = simpledialog.askstring("Edit Task", "Category:", initialvalue=todo.get('category','General'), parent=root) or "General"
    due_date = simpledialog.askstring("Edit Task", "Due date (YYYY-MM-DD) or blank:", initialvalue=todo.get('due_date') or '', parent=root) or None
    todo_manager.update_todo(tid, title=title, description=description, priority=priority, category=category, due_date=due_date)
    root.refresh()  # type: ignore


def _delete_task(todo_manager: TodoManager, tree: ttk.Treeview):
    tid = _selected_id(tree)
    if not tid:
        return
    todo_manager.delete_todo(tid)
    tree.master.refresh()  # type: ignore


def _toggle_complete(todo_manager: TodoManager, tree: ttk.Treeview):
    tid = _selected_id(tree)
    if not tid:
        return
    todo = todo_manager.get_todo(tid)
    if not todo:
        return
    todo_manager.set_completed(tid, not bool(todo['completed']))
    tree.master.refresh()  # type: ignore

