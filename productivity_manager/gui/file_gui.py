import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText

import threading

from modules.file_organizer import organize_directory, find_duplicates, batch_rename


def build_file_tab(parent):
    frame = ttk.Frame(parent)

    top = ttk.Frame(frame)
    top.pack(fill=tk.X, padx=8, pady=8)

    path_var = tk.StringVar(value=os.path.expanduser("~"))
    ttk.Entry(top, textvariable=path_var, width=80).pack(side=tk.LEFT, padx=4)
    ttk.Button(top, text="찾아보기", command=lambda: _choose_dir(path_var)).pack(side=tk.LEFT)

    actions = ttk.Frame(frame)
    actions.pack(fill=tk.X, padx=8)

    output = ScrolledText(frame, height=20)
    output.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 4))

    prog = ttk.Progressbar(frame, mode="indeterminate")
    prog.pack(fill=tk.X, padx=8, pady=(0, 8))

    ttk.Button(
        actions,
        text="정리",
        command=lambda: _busy_run(frame, output, prog, organize_directory, path_var.get()),
    ).pack(side=tk.LEFT, padx=4)
    ttk.Button(
        actions,
        text="중복 찾기",
        command=lambda: _busy_run(frame, output, prog, _list_duplicates, path_var.get()),
    ).pack(side=tk.LEFT, padx=4)
    ttk.Button(
        actions,
        text="일괄 이름변경",
        command=lambda: _busy_run(frame, output, prog, _batch_rename, path_var.get()),
    ).pack(side=tk.LEFT, padx=4)
    ttk.Button(
        actions,
        text="지우기",
        command=lambda: output.delete("1.0", tk.END),
    ).pack(side=tk.LEFT, padx=4)

    return frame


def _choose_dir(path_var):
    p = filedialog.askdirectory()
    if p:
        path_var.set(p)


def _busy_run(root: tk.Misc, output: ScrolledText, prog: ttk.Progressbar, func, *args):
    """Run potentially long operation in a background thread and update UI when done."""
    output.delete("1.0", tk.END)
    prog.start(10)
    root.update_idletasks()

    def _worker():
        try:
            result = func(*args)
            err = None
        except Exception as e:  # pragma: no cover - UI path
            result = None
            err = e

        def _done():
            try:
                if err is not None:
                    output.insert(tk.END, f"오류: {err}\n")
                else:
                    if isinstance(result, list):
                        for line in result:
                            output.insert(tk.END, str(line) + "\n")
                    elif result is not None:
                        output.insert(tk.END, str(result) + "\n")
            finally:
                prog.stop()

        root.after(0, _done)

    t = threading.Thread(target=_worker, daemon=True)
    t.start()


def _list_duplicates(directory: str):
    """Return lines describing duplicates rather than touching UI directly."""
    lines = []
    dups = find_duplicates(directory)
    if not dups:
        lines.append("중복 파일이 없습니다.")
        return lines
    for h, paths in dups:
        lines.append(f"해시 {h[:10]}...")
        for p in paths:
            lines.append(f"  - {p}")
    return lines


def _batch_rename(directory: str):
    return batch_rename(directory)
