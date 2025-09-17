import os
import sys

from utils.config import ensure_app_dirs, load_config
from database.db_manager import DBManager
from gui.main_window import run_app


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ensure_app_dirs(base_dir)

    # Load config (creates default if missing)
    _ = load_config(base_dir)

    # Initialize database and tables
    db_path = os.path.join(base_dir, 'data', 'productivity.db')
    db = DBManager(db_path)
    db.initialize()

    # Launch GUI
    run_app(base_dir, db)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

