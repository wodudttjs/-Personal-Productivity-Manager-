import json
import os
from typing import Any, Dict

from platformdirs import user_data_dir
from typing import Optional

from .constants import CONFIG_FILE, APP_NAME


def data_dir(_base_dir: Optional[str] = None) -> str:
    """Return the user-writable data dir for the app.

    Ignores the package install directory and uses a proper per-user location.
    """
    return user_data_dir(APP_NAME, roaming=True)


def ensure_app_dirs(_base_dir: str) -> None:
    """Ensure required directories exist in the user data dir."""
    root = data_dir(_base_dir)
    for sub in ("assets/icons", "assets/themes", "logs"):
        os.makedirs(os.path.join(root, sub), exist_ok=True)


def config_path(_base_dir: str) -> str:
    return os.path.join(data_dir(_base_dir), CONFIG_FILE)


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
        # Ensure the data directory exists before writing
        os.makedirs(os.path.dirname(path), exist_ok=True)
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
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
