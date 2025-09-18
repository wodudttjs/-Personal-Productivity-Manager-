import os
import tkinter as tk
from tkinter import ttk, messagebox

from database.db_manager import DBManager
from modules.todo_manager import TodoManager
from modules.time_tracker import Timer
from utils.config import load_config, save_config
from .theme import apply_theme

from .todo_gui import build_todo_tab
from .timer_gui import build_timer_tab
from .file_gui import build_file_tab
from .scraper_gui import build_scraper_tab
from .monitor_gui import build_monitor_tab


def run_app(base_dir: str, db: DBManager) -> None:
    cfg = load_config(base_dir)

    root = tk.Tk()
    root.title("개인 생산성 관리자")
    try:
        root.geometry(cfg.get("ui", {}).get("window_size", "1000x700"))
    except Exception:
        pass

    # Theme
    ui_mode = cfg.get("ui", {}).get("theme", "light")
    apply_theme(root, ui_mode)

    # Menubar and theme toggle
    _setup_menubar(root, cfg, base_dir)

    # Main content
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Status bar
    status_var = tk.StringVar(value="준비됨")
    status_bar = ttk.Label(root, textvariable=status_var, anchor="w")
    status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    # Managers
    todo_manager = TodoManager(db)
    timer = Timer(db)

    # Tabs
    tabs = {
        "할 일": build_todo_tab(notebook, todo_manager),
        "타이머": build_timer_tab(notebook, timer, todo_manager),
        "파일": build_file_tab(notebook),
        "스크레이퍼": build_scraper_tab(notebook, base_dir),
        "모니터": build_monitor_tab(notebook),
    }

    for name, frame in tabs.items():
        notebook.add(frame, text=name)

    def on_tab_changed(event=None):
        try:
            idx = notebook.index(notebook.select())
            text = notebook.tab(idx, 'text')
            status_var.set(f"활성 탭: {text}")
        except Exception:
            status_var.set("준비됨")

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)
    on_tab_changed()

    def on_close():
        try:
            geo = root.winfo_geometry().split('+', 1)[0]
            cfg.setdefault("ui", {})["window_size"] = geo
            save_config(base_dir, cfg)
        except Exception:
            pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()


def _setup_menubar(root: tk.Misc, cfg: dict, base_dir: str) -> None:
    menubar = tk.Menu(root)

    file_menu = tk.Menu(menubar, tearoff=False)
    file_menu.add_command(label="종료", command=root.destroy, accelerator="Alt+F4")
    menubar.add_cascade(label="파일", menu=file_menu)

    view_menu = tk.Menu(menubar, tearoff=False)
    theme_var = tk.StringVar(value=cfg.get("ui", {}).get("theme", "light"))

    def _set_theme(mode: str):
        apply_theme(root, mode)
        cfg.setdefault("ui", {})["theme"] = mode
        save_config(base_dir, cfg)

    view_menu.add_radiobutton(label="라이트", value="light", variable=theme_var, command=lambda: _set_theme("light"))
    view_menu.add_radiobutton(label="다크", value="dark", variable=theme_var, command=lambda: _set_theme("dark"))
    menubar.add_cascade(label="보기", menu=view_menu)

    help_menu = tk.Menu(menubar, tearoff=False)
    help_menu.add_command(
        label="정보",
        command=lambda: messagebox.showinfo(
            "정보",
            "개인 생산성 관리자\nTkinter로 만든 간단하고 직관적인 UI.",
        ),
    )
    menubar.add_cascade(label="도움말", menu=help_menu)

    root.configure(menu=menubar)
