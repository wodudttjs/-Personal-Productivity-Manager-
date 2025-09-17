import os
import tkinter as tk
from tkinter import ttk

from database.db_manager import DBManager
from modules.todo_manager import TodoManager
from modules.time_tracker import Timer
from utils.config import load_config

from .todo_gui import build_todo_tab
from .timer_gui import build_timer_tab
from .file_gui import build_file_tab
from .scraper_gui import build_scraper_tab
from .monitor_gui import build_monitor_tab


def run_app(base_dir: str, db: DBManager) -> None:
    cfg = load_config(base_dir)

    root = tk.Tk()
    root.title("Personal Productivity Manager")
    try:
        root.geometry(cfg.get("ui", {}).get("window_size", "1000x700"))
    except Exception:
        pass

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Managers
    todo_manager = TodoManager(db)
    timer = Timer(db)

    # Tabs
    tabs = {
        "Todo": build_todo_tab(notebook, todo_manager),
        "Timer": build_timer_tab(notebook, timer, todo_manager),
        "Files": build_file_tab(notebook),
        "Scraper": build_scraper_tab(notebook, base_dir),
        "Monitor": build_monitor_tab(notebook),
    }

    for name, frame in tabs.items():
        notebook.add(frame, text=name)

    root.mainloop()

