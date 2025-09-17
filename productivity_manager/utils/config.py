import json
import os
from typing import Any, Dict

from .constants import CONFIG_FILE


def ensure_app_dirs(base_dir: str) -> None:
    """Ensure required directories exist."""
    for sub in ("modules", "gui", "database", "utils", "tests", "assets/icons", "assets/themes", "data/logs"):
        os.makedirs(os.path.join(base_dir, sub), exist_ok=True)


def config_path(base_dir: str) -> str:
    return os.path.join(base_dir, "data", CONFIG_FILE)


DEFAULT_CONFIG: Dict[str, Any] = {
    "version": 1,
    "ui": {
        "theme": "light",
        "window_size": "1000x700",
    },
    "web": {
        "weather_provider": "wttr.in",  # or 'openweathermap'
        "weather_city": "Seoul",
        "weather_api_key": "",  # if using openweathermap
        "rss_feeds": [
            "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
        ],
        "exchange_base": "USD",
    },
    "file_organizer": {
        "downloads_path": os.path.join(os.path.expanduser("~"), "Downloads"),
        "create_category_folders": True,
    },
    "notifications": {
        "todo_due_alert_minutes": 60
    }
}


def load_config(base_dir: str) -> Dict[str, Any]:
    path = config_path(base_dir)
    if not os.path.exists(path):
        save_config(base_dir, DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # On error, back up and reset
        try:
            os.replace(path, path + ".bak")
        except Exception:
            pass
        save_config(base_dir, DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def save_config(base_dir: str, cfg: Dict[str, Any]) -> None:
    path = config_path(base_dir)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

