import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "memory.db"


def init_db() -> None:
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def save_message(customer_id: str, role: str, message: str) -> None:
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (customer_id, role, message, timestamp) VALUES (?, ?, ?, ?)",
        (customer_id, role, message, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_history(customer_id: str) -> list[dict]:
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, message, timestamp FROM conversations WHERE customer_id = ? ORDER BY id ASC",
        (customer_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r[0], "message": r[1], "timestamp": r[2]} for r in rows]


def format_history_for_prompt(history: list[dict]) -> str:
    if not history:
        return "No previous conversations found."
    lines: list[str] = []
    for entry in history:
        ts = str(entry.get("timestamp", ""))[:10]
        role = str(entry.get("role", "")).upper()
        msg = str(entry.get("message", ""))
        lines.append(f"[{ts}] {role}: {msg}")
    return "\n".join(lines)

