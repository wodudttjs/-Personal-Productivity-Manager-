from typing import Dict

import psutil


def get_system_stats() -> Dict[str, float]:
    cpu = psutil.cpu_percent(interval=None)
    vm = psutil.virtual_memory()
    du = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    return {
        "cpu_percent": cpu,
        "mem_percent": vm.percent,
        "disk_percent": du.percent,
        "bytes_sent": float(net.bytes_sent),
        "bytes_recv": float(net.bytes_recv),
    }

