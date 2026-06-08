#!/usr/bin/env python
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / ".." / "backend" / "src"))

from core.hardware_db import HardwareDatabase


def main():
    db = HardwareDatabase()
    print("Initialized hardware threat database at", db.db_path)


if __name__ == "__main__":
    main()
