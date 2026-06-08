import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).resolve().parents[2] / "fieldtasker.db"

class HardwareDatabase:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        schema_path = Path(__file__).resolve().parents[2] / "database" / "schema.sql"
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(schema_path.read_text())

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add_rf_signal(self, identifier: str, frequency: str, type_: str, vendor: str, description: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO rf_signals (identifier, frequency, type, vendor, description) VALUES (?, ?, ?, ?, ?)",
                (identifier, frequency, type_, vendor, description),
            )
            conn.commit()

    def add_firmware_fingerprint(self, device_type: str, vendor: str, model: str, firmware_hash: str, fingerprint_source: str, threat_level: str, description: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO firmware_fingerprints (device_type, vendor, model, firmware_hash, fingerprint_source, threat_level, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (device_type, vendor, model, firmware_hash, fingerprint_source, threat_level, description),
            )
            conn.commit()

    def log_discovered_hardware(self, location: str, device_type: str, identifier: str, firmware_hash: str, match_status: str, notes: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO discovered_hardware_log (location, device_type, identifier, firmware_hash, match_status, notes) VALUES (?, ?, ?, ?, ?, ?)",
                (location, device_type, identifier, firmware_hash, match_status, notes),
            )
            conn.commit()

    def query_rf_signals(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM rf_signals")
            return [dict(row) for row in cursor.fetchall()]

    def query_firmware_fingerprints(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM firmware_fingerprints")
            return [dict(row) for row in cursor.fetchall()]

    def query_discovered_hardware(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM discovered_hardware_log")
            return [dict(row) for row in cursor.fetchall()]

if __name__ == "__main__":
    db = HardwareDatabase()
    db.add_rf_signal("BLE Beacon A", "2.4GHz", "BLE", "Unknown Vendor", "Sample beacon signature")
    db.add_firmware_fingerprint("Bluetooth Speaker", "Roku", "Model X", "deadbeef...", "sample corpus", "high", "Malicious firmware fingerprint")
    db.log_discovered_hardware("Field Base", "Bluetooth Speaker", "BLE Beacon A", "deadbeef...", "malicious", "Sample detection")
    print("Initialized hardware threat database and inserted sample data.")
