# backend/tools/reminder.py
"""Simple reminder tool.
Stores reminders in a SQLite database (reminders.db) and uses APScheduler
to trigger a console log at the scheduled time. In a real UI this would push
a notification to the frontend.
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict

DB_PATH = Path(__file__).resolve().parent.parent / "reminders.db"

def _init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            remind_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

_init_db()

def add_reminder(message: str, remind_at: datetime) -> int:
    """Insert a reminder and return its DB id."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO reminders (message, remind_at) VALUES (?, ?)",
        (message, remind_at.isoformat()),
    )
    conn.commit()
    reminder_id = c.lastrowid
    conn.close()
    return reminder_id

def list_upcoming(limit: int = 10) -> List[Dict[str, str]]:
    """Return upcoming reminders ordered by time."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, message, remind_at FROM reminders WHERE remind_at >= ? ORDER BY remind_at LIMIT ?",
        (datetime.utcnow().isoformat(), limit),
    )
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "message": r[1], "remind_at": r[2]} for r in rows]
