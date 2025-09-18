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

    # CPU
    ttk.Label(frame, textvariable=labels["cpu"]).pack(anchor=tk.W, padx=12, pady=(10, 4))
    cpu_pb = ttk.Progressbar(frame, orient="horizontal", mode="determinate", maximum=100)
    cpu_pb.pack(fill=tk.X, padx=12)

    # Memory
    ttk.Label(frame, textvariable=labels["mem"]).pack(anchor=tk.W, padx=12, pady=(12, 4))
    mem_pb = ttk.Progressbar(frame, orient="horizontal", mode="determinate", maximum=100)
    mem_pb.pack(fill=tk.X, padx=12)

    # Disk
    ttk.Label(frame, textvariable=labels["disk"]).pack(anchor=tk.W, padx=12, pady=(12, 4))
    disk_pb = ttk.Progressbar(frame, orient="horizontal", mode="determinate", maximum=100)
    disk_pb.pack(fill=tk.X, padx=12)

    # Network
    ttk.Label(frame, textvariable=labels["net"]).pack(anchor=tk.W, padx=12, pady=12)

    state = {"prev_sent": 0.0, "prev_recv": 0.0}

    def tick():
        stats = get_system_stats()
        cpu = float(stats.get('cpu_percent', 0.0))
        mem = float(stats.get('mem_percent', 0.0))
        dsk = float(stats.get('disk_percent', 0.0))

        labels["cpu"].set(f"CPU: {cpu:.1f}%")
        labels["mem"].set(f"Memory: {mem:.1f}%")
        labels["disk"].set(f"Disk: {dsk:.1f}%")

        cpu_pb['value'] = cpu
        mem_pb['value'] = mem
        disk_pb['value'] = dsk

        sent = stats.get("bytes_sent", 0.0)
        recv = stats.get("bytes_recv", 0.0)
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
