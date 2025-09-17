from datetime import datetime


def now_iso() -> str:
    return datetime.now().isoformat(timespec='seconds')


def safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default

