import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText

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
    output.delete("1.0", tk.END)
    try:
        prog.start(10)
        root.update_idletasks()
        result = func(*args)
        # Support both list-returning and specialized helpers
        if isinstance(result, list):
            for line in result:
                output.insert(tk.END, str(line) + "\n")
        else:
            # If func is a wrapper like _list_duplicates/_batch_rename, it already wrote output
            pass
    except Exception as e:
        output.insert(tk.END, f"오류: {e}\n")
    finally:
        prog.stop()


def _list_duplicates(output: ScrolledText, directory: str):
    output.delete("1.0", tk.END)
    try:
        dups = find_duplicates(directory)
        if not dups:
            output.insert(tk.END, "중복 파일이 없습니다.\n")
        for h, paths in dups:
            output.insert(tk.END, f"해시 {h[:10]}...\n")
            for p in paths:
                output.insert(tk.END, f"  - {p}\n")
    except Exception as e:
        output.insert(tk.END, f"오류: {e}\n")


def _batch_rename(output: ScrolledText, directory: str):
    output.delete("1.0", tk.END)
    try:
        logs = batch_rename(directory)
        for line in logs:
            output.insert(tk.END, line + "\n")
    except Exception as e:
        output.insert(tk.END, f"오류: {e}\n")
