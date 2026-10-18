# backend/tools/wellness.py
"""Simple wellness logging tool.
Stores daily wellness metrics in a SQLite DB (wellness.db).
Supported fields: water_intake (glasses), sleep_hours, exercise_minutes,
    mood (1-5), steps, weight_kg.
Provides functions to add a log entry and to summarise the last N days.
"""
import sqlite3
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List

DB_PATH = Path(__file__).resolve().parent.parent / "wellness.db"

def _init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS wellness (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date TEXT NOT NULL,
            water_intake INTEGER,
            sleep_hours REAL,
            exercise_minutes INTEGER,
            mood INTEGER,
            steps INTEGER,
            weight_kg REAL
        )
        """
    )
    conn.commit()
    conn.close()

_init_db()

def add_log(
    water_intake: int | None = None,
    sleep_hours: float | None = None,
    exercise_minutes: int | None = None,
    mood: int | None = None,
    steps: int | None = None,
    weight_kg: float | None = None,
) -> int:
    """Insert a daily wellness entry. Returns the row id."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO wellness (
            log_date, water_intake, sleep_hours, exercise_minutes,
            mood, steps, weight_kg
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            date.today().isoformat(),
            water_intake,
            sleep_hours,
            exercise_minutes,
            mood,
            steps,
            weight_kg,
        ),
    )
    conn.commit()
    row_id = c.lastrowid
    conn.close()
    return row_id

def summary_last_days(days: int = 7) -> Dict[str, float]:
    """Return average values for the last *days* days (including today)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        SELECT water_intake, sleep_hours, exercise_minutes, mood, steps, weight_kg
        FROM wellness
        WHERE log_date >= date('now', ?)
        """,
        (f"-{days - 1} day",),
    )
    rows = c.fetchall()
    conn.close()
    if not rows:
        return {}
    # Compute column-wise averages ignoring NULLs
    sums = [0.0] * 6
    counts = [0] * 6
    for r in rows:
        for i, val in enumerate(r):
            if val is not None:
                sums[i] += float(val)
                counts[i] += 1
    averages = {
        "water_intake": sums[0] / counts[0] if counts[0] else 0,
        "sleep_hours": sums[1] / counts[1] if counts[1] else 0,
        "exercise_minutes": sums[2] / counts[2] if counts[2] else 0,
        "mood": sums[3] / counts[3] if counts[3] else 0,
        "steps": sums[4] / counts[4] if counts[4] else 0,
        "weight_kg": sums[5] / counts[5] if counts[5] else 0,
    }
    return averages
