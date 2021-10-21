from pathlib import Path


PROJECT_DIR = (Path(__file__).parent / "../..").resolve()
DB_DIR = PROJECT_DIR / "db"
DB_BACKUPS_PATH = DB_DIR / "backups"
