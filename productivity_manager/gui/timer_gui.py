import tkinter as tk
from tkinter import ttk, messagebox

from modules.time_tracker import Timer
from modules.todo_manager import TodoManager


def build_timer_tab(parent, timer: Timer, todo_manager: TodoManager):
    frame = ttk.Frame(parent)

    top = ttk.Frame(frame)
    top.pack(fill=tk.X, padx=8, pady=8)

    ttk.Label(top, text="Task:").pack(side=tk.LEFT)
    tasks = todo_manager.list_todos()
    task_choices = [f"{t['id']}: {t['title']}" for t in tasks]
    selected = tk.StringVar(value=task_choices[0] if task_choices else "")
    cb = ttk.Combobox(top, values=task_choices, textvariable=selected, width=60, state="readonly")
    cb.pack(side=tk.LEFT, padx=6)

    elapsed_var = tk.StringVar(value="00:00:00")
    lbl_elapsed = ttk.Label(top, textvariable=elapsed_var)
    lbl_elapsed.pack(side=tk.RIGHT)
    try:
        lbl_elapsed.configure(font=("Segoe UI", 24, "bold"))
    except Exception:
        pass

    ttk.Separator(frame, orient="horizontal").pack(fill=tk.X, padx=8, pady=(0, 8))

    buttons = ttk.Frame(frame)
    buttons.pack(fill=tk.X, padx=8)

    running = {"flag": False}

    def update_elapsed():
        secs = timer.elapsed_seconds()
        h = secs // 3600
        m = (secs % 3600) // 60
        s = secs % 60
        elapsed_var.set(f"{h:02}:{m:02}:{s:02}")
        if running["flag"]:
            frame.after(500, update_elapsed)

    def on_start():
        val = selected.get()
        if not val:
            messagebox.showinfo("Start Timer", "Please select a task to track.")
            return
        if ":" in val:
            tid = int(val.split(":", 1)[0])
            timer.task_id = tid
        timer.start()
        running["flag"] = True
        update_elapsed()

    def on_stop():
        entry_id = timer.stop()
        running["flag"] = False
        messagebox.showinfo("Time Tracked", f"Saved time entry #{entry_id}")

    def on_reset():
        timer.reset()
        running["flag"] = False
        elapsed_var.set("00:00:00")

    ttk.Button(buttons, text="Start", command=on_start).pack(side=tk.LEFT, padx=4)
    ttk.Button(buttons, text="Stop", command=on_stop).pack(side=tk.LEFT, padx=4)
    ttk.Button(buttons, text="Reset", command=on_reset).pack(side=tk.LEFT, padx=4)

    # Space toggles start/stop
    def _toggle_space(event=None):
        if running["flag"]:
            on_stop()
        else:
            on_start()
    frame.bind_all("<space>", _toggle_space)

    return frame
