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
    ttk.Button(top, text="Browse", command=lambda: _choose_dir(path_var)).pack(side=tk.LEFT)

    actions = ttk.Frame(frame)
    actions.pack(fill=tk.X, padx=8)

    ttk.Button(actions, text="Organize", command=lambda: _run_log(output, organize_directory, path_var.get())).pack(side=tk.LEFT, padx=4)
    ttk.Button(actions, text="Find Duplicates", command=lambda: _list_duplicates(output, path_var.get())).pack(side=tk.LEFT, padx=4)
    ttk.Button(actions, text="Batch Rename", command=lambda: _batch_rename(output, path_var.get())).pack(side=tk.LEFT, padx=4)

    output = ScrolledText(frame, height=20)
    output.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

    return frame


def _choose_dir(path_var):
    p = filedialog.askdirectory()
    if p:
        path_var.set(p)


def _run_log(output: ScrolledText, func, *args):
    output.delete("1.0", tk.END)
    try:
        logs = func(*args)
        for line in logs:
            output.insert(tk.END, line + "\n")
    except Exception as e:
        output.insert(tk.END, f"Error: {e}\n")


def _list_duplicates(output: ScrolledText, directory: str):
    output.delete("1.0", tk.END)
    try:
        dups = find_duplicates(directory)
        if not dups:
            output.insert(tk.END, "No duplicates found.\n")
        for h, paths in dups:
            output.insert(tk.END, f"Hash {h[:10]}...\n")
            for p in paths:
                output.insert(tk.END, f"  - {p}\n")
    except Exception as e:
        output.insert(tk.END, f"Error: {e}\n")


def _batch_rename(output: ScrolledText, directory: str):
    output.delete("1.0", tk.END)
    try:
        logs = batch_rename(directory)
        for line in logs:
            output.insert(tk.END, line + "\n")
    except Exception as e:
        output.insert(tk.END, f"Error: {e}\n")

