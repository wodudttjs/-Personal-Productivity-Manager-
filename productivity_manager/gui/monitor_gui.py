import tkinter as tk
from tkinter import ttk

from modules.system_monitor import get_system_stats


def build_monitor_tab(parent):
    frame = ttk.Frame(parent)

    labels = {
        "cpu": tk.StringVar(value="CPU: 0%"),
        "mem": tk.StringVar(value="Memory: 0%"),
        "disk": tk.StringVar(value="Disk: 0%"),
        "net": tk.StringVar(value="Network: 0 B / 0 B"),
    }

    ttk.Label(frame, textvariable=labels["cpu"]).pack(anchor=tk.W, padx=12, pady=6)
    ttk.Label(frame, textvariable=labels["mem"]).pack(anchor=tk.W, padx=12, pady=6)
    ttk.Label(frame, textvariable=labels["disk"]).pack(anchor=tk.W, padx=12, pady=6)
    ttk.Label(frame, textvariable=labels["net"]).pack(anchor=tk.W, padx=12, pady=6)

    state = {"prev_sent": 0.0, "prev_recv": 0.0}

    def tick():
        stats = get_system_stats()
        labels["cpu"].set(f"CPU: {stats['cpu_percent']:.1f}%")
        labels["mem"].set(f"Memory: {stats['mem_percent']:.1f}%")
        labels["disk"].set(f"Disk: {stats['disk_percent']:.1f}%")
        sent = stats["bytes_sent"]
        recv = stats["bytes_recv"]
        ds = max(sent - state["prev_sent"], 0)
        dr = max(recv - state["prev_recv"], 0)
        state["prev_sent"], state["prev_recv"] = sent, recv
        labels["net"].set(f"Network: {human_bytes(ds)}/s up, {human_bytes(dr)}/s down")
        frame.after(1000, tick)

    def human_bytes(n: float) -> str:
        for unit in ["B", "KB", "MB", "GB"]:
            if n < 1024.0:
                return f"{n:.1f} {unit}"
            n /= 1024.0
        return f"{n:.1f} TB"

    frame.after(500, tick)
    return frame

