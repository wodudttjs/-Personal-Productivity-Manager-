import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional, List, Dict

from modules.todo_manager import TodoManager


def build_todo_tab(parent, todo_manager: TodoManager):
    frame = ttk.Frame(parent)

    # Controls
    controls = ttk.Frame(frame)
    controls.pack(fill=tk.X, padx=8, pady=(8, 4))

    btn_add = ttk.Button(controls, text="추가", command=lambda: _add_task(frame, todo_manager, tree))
    btn_add.pack(side=tk.LEFT, padx=4)
    btn_edit = ttk.Button(controls, text="수정", command=lambda: _edit_task(frame, todo_manager, tree))
    btn_edit.pack(side=tk.LEFT, padx=4)
    btn_del = ttk.Button(controls, text="삭제", command=lambda: _delete_task(todo_manager, tree))
    btn_del.pack(side=tk.LEFT, padx=4)
    btn_toggle = ttk.Button(controls, text="완료 전환", command=lambda: _toggle_complete(todo_manager, tree))
    btn_toggle.pack(side=tk.LEFT, padx=4)

    # Filters
    filters = ttk.Frame(frame)
    filters.pack(fill=tk.X, padx=8, pady=(0, 8))
    search_var = tk.StringVar()
    ttk.Label(filters, text="검색:").pack(side=tk.LEFT)
    ent = ttk.Entry(filters, textvariable=search_var, width=30)
    ent.pack(side=tk.LEFT, padx=6)

    priority_var = tk.StringVar(value="전체")
    ttk.Label(filters, text="우선순위:").pack(side=tk.LEFT, padx=(12, 0))
    cb_pri = ttk.Combobox(filters, values=["전체", "높음", "보통", "낮음"], textvariable=priority_var, width=10, state="readonly")
    cb_pri.pack(side=tk.LEFT, padx=4)

    category_var = tk.StringVar(value="전체")
    ttk.Label(filters, text="카테고리:").pack(side=tk.LEFT, padx=(12, 0))
    cb_cat = ttk.Combobox(filters, values=["전체"], textvariable=category_var, width=16, state="readonly")
    cb_cat.pack(side=tk.LEFT, padx=4)

    show_completed = tk.BooleanVar(value=True)
    ttk.Checkbutton(filters, text="완료 항목 표시", variable=show_completed, command=lambda: refresh()).pack(side=tk.RIGHT)

    # Treeview for tasks
    columns = ("id", "title", "priority", "category", "due_date", "completed")
    tree = ttk.Treeview(frame, columns=columns, show='headings', selectmode='browse')

    headings = {
        "id": "ID",
        "title": "제목",
        "priority": "우선순위",
        "category": "카테고리",
        "due_date": "마감",
        "completed": "완료",
    }
    for col in columns:
        tree.heading(col, text=headings[col])
        tree.column(col, width=100, anchor=(tk.E if col in ("priority", "completed") else tk.W))
    tree.column("title", width=280, anchor=tk.W)
    tree.column("id", width=60, anchor=tk.E)

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0), pady=(0, 8))
    vsb.pack(side=tk.LEFT, fill=tk.Y, pady=(0, 8))

    sort_state: Dict[str, bool] = {}

    def _sort_by(col: str):
        reverse = sort_state.get(col, False)
        data = []
        for iid in tree.get_children(""):
            vals = tree.item(iid, "values")
            data.append((iid, vals))

        def keyfunc(item):
            vals = item[1]
            idx = columns.index(col)
            v = vals[idx]
            if col == "id":
                try:
                    return int(v)
                except Exception:
                    return 0
            if col == "completed":
                return 0 if v == "완료" else 1
            return (v or "").lower()

        data.sort(key=keyfunc, reverse=reverse)
        for index, (iid, _vals) in enumerate(data):
            tree.move(iid, "", index)
        sort_state[col] = not reverse

    for col in columns:
        tree.heading(col, text=headings[col], command=lambda c=col: _sort_by(c))

    # Tag styles
    tree.tag_configure("completed", foreground="#808080")
    tree.tag_configure("odd", background="")
    tree.tag_configure("even", background="")

    def _categories_from(rows: List[dict]) -> List[str]:
        cats = sorted({(r.get("category") or "General") for r in rows})
        return ["전체"] + cats

    def refresh():
        # Preserve selection id
        current_sel = _selected_id(tree)
        for i in tree.get_children(""):
            tree.delete(i)
        rows = todo_manager.list_todos()
        # Update category choices
        cb_cat.configure(values=_categories_from(rows))

        q = (search_var.get() or "").strip().lower()
        pri_display = priority_var.get()
        cat = category_var.get()
        show = show_completed.get()

        def _match(row):
            if q:
                if q not in (row.get('title') or '').lower() and q not in (row.get('description') or '').lower():
                    return False
            if pri_display and pri_display != "전체":
                pri_map = {"높음": "high", "보통": "medium", "낮음": "low"}
                pri_canon = pri_map.get(pri_display, pri_display).lower()
                if (row.get('priority') or "").lower() != pri_canon:
                    return False
            if cat and cat != "전체" and (row.get('category') or "General") != cat:
                return False
            if not show and row.get('completed'):
                return False
            return True

        filtered = [r for r in rows if _match(r)]
        for idx, row in enumerate(filtered):
            done = bool(row.get('completed'))
            tags = []
            if done:
                tags.append("completed")
            tags.append("even" if idx % 2 == 0 else "odd")
            tree.insert(
                '',
                tk.END,
                values=(
                    row['id'],
                    row['title'],
                    row.get('priority') or '',
                    row.get('category') or 'General',
                    row.get('due_date') or '',
                    '완료' if done else ''
                ),
                tags=tuple(tags),
            )

        # Restore selection if possible
        if current_sel is not None:
            for iid in tree.get_children(""):
                vals = tree.item(iid, 'values')
                try:
                    if int(vals[0]) == current_sel:
                        tree.selection_set(iid)
                        tree.see(iid)
                        break
                except Exception:
                    pass

    # Filter events
    ent.bind("<KeyRelease>", lambda e: refresh())
    cb_pri.bind("<<ComboboxSelected>>", lambda e: refresh())
    cb_cat.bind("<<ComboboxSelected>>", lambda e: refresh())

    # Interactions
    tree.bind("<Double-1>", lambda e: _edit_task(frame, todo_manager, tree))
    frame.bind_all("<Control-n>", lambda e: _add_task(frame, todo_manager, tree))
    frame.bind_all("<Delete>", lambda e: _delete_task(todo_manager, tree))

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
    title = simpledialog.askstring("새 작업", "제목:", parent=root)
    if not title:
        return
    description = simpledialog.askstring("새 작업", "설명:", parent=root) or ""
    priority = simpledialog.askstring("새 작업", "우선순위 (높음/보통/낮음):", parent=root) or "Medium"
    category = simpledialog.askstring("새 작업", "카테고리:", parent=root) or "General"
    due_date = simpledialog.askstring("새 작업", "마감일 (YYYY-MM-DD) 또는 공란:", parent=root) or None
    pri_norm = {"높음": "High", "보통": "Medium", "낮음": "Low"}.get(priority, priority)
    todo_manager.add_todo(title, description, pri_norm, category, due_date)
    root.refresh()  # type: ignore


def _edit_task(root, todo_manager: TodoManager, tree: ttk.Treeview):
    tid = _selected_id(tree)
    if not tid:
        messagebox.showinfo("수정", "먼저 작업을 선택하세요.")
        return
    todo = todo_manager.get_todo(tid)
    if not todo:
        return
    title = simpledialog.askstring("작업 수정", "제목:", initialvalue=todo['title'], parent=root)
    if not title:
        return
    description = simpledialog.askstring("작업 수정", "설명:", initialvalue=todo.get('description',''), parent=root) or ""
    priority = simpledialog.askstring("작업 수정", "우선순위 (높음/보통/낮음):", initialvalue=todo.get('priority','Medium'), parent=root) or "Medium"
    category = simpledialog.askstring("작업 수정", "카테고리:", initialvalue=todo.get('category','General'), parent=root) or "General"
    due_date = simpledialog.askstring("작업 수정", "마감일 (YYYY-MM-DD) 또는 공란:", initialvalue=todo.get('due_date') or '', parent=root) or None
    pri_norm = {"높음": "High", "보통": "Medium", "낮음": "Low"}.get(priority, priority)
    todo_manager.update_todo(tid, title=title, description=description, priority=pri_norm, category=category, due_date=due_date)
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

