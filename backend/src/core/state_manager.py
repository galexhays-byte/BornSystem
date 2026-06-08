import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional

class StateManager:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = Path(db_path) if db_path else Path(__file__).resolve().parents[2] / "state.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self.state = self._load_state()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
            )
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, payload TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
            )
            conn.commit()

    def _load_state(self) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM state")
            rows = cursor.fetchall()
            return {key: json.loads(value) for key, value in rows}

    def update(self, key: str, value: Any) -> None:
        self.state[key] = value
        payload = json.dumps(value)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO state (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP",
                (key, payload),
            )
            conn.commit()

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)

    def all(self) -> Dict[str, Any]:
        return dict(self.state)

    def save_run(self, run_id: str, payload: Any) -> None:
        payload_json = json.dumps(payload)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO runs (run_id, payload) VALUES (?, ?)",
                (run_id, payload_json),
            )
            conn.commit()

    def get_run(self, run_id: str) -> Optional[Any]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT payload FROM runs WHERE run_id = ?", (run_id,))
            row = cursor.fetchone()
            return json.loads(row[0]) if row else None

    def list_runs(self, limit: int = 50) -> list[dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT run_id, payload, created_at FROM runs ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            rows = cursor.fetchall()

        runs = []
        for run_id, payload_json, created_at in rows:
            payload = json.loads(payload_json)
            runs.append(
                {
                    "run_id": run_id,
                    "created_at": created_at,
                    "goal": payload.get("goal"),
                    "status": "completed" if payload.get("results") else "pending",
                }
            )
        return runs
