import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "fieldtasker.db"
SCHEMA_SQL = Path(__file__).resolve().parent / "schema.sql"


def init_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_SQL.read_text())
    print(f"Initialized database at {DB_PATH}")


def main():
    init_database()


if __name__ == "__main__":
    main()
