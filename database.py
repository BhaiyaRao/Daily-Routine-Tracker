"""
database.py - SQLite Database Handler for Daily Routine Tracker
Author: College Project
Description: Handles all local SQLite database operations, including table creation,
CRUD for routines, and daily completion logs.
"""

import sqlite3
from datetime import datetime, date
from pathlib import Path

DB_FILE = Path(__file__).parent / "routine_tracker.db"

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables and seed default routines if empty."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table 1: Routines
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS routines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'General',
            time_slot TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Medium',
            frequency TEXT NOT NULL DEFAULT 'Daily',
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table 2: Daily Logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            routine_id INTEGER NOT NULL,
            log_date DATE NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            completion_time TIMESTAMP,
            notes TEXT DEFAULT '',
            FOREIGN KEY (routine_id) REFERENCES routines(id) ON DELETE CASCADE,
            UNIQUE(routine_id, log_date)
        )
    """)
    conn.commit()

    # Check if empty, seed with sample routines
    cursor.execute("SELECT COUNT(*) as count FROM routines")
    if cursor.fetchone()["count"] == 0:
        sample_routines = [
            ("Morning Exercise / Workout", "Fitness", "06:30 AM", "High", "Daily"),
            ("College Classes / Lectures", "Study", "09:00 AM", "High", "Weekdays"),
            ("Programming & Project Practice", "Productivity", "04:00 PM", "High", "Daily"),
            ("Evening Walk / Break", "Personal", "06:30 PM", "Medium", "Daily"),
            ("Revise College Notes & Assignments", "Study", "08:30 PM", "Medium", "Daily"),
            ("Daily Review & Plan Tomorrow", "Personal", "10:30 PM", "Low", "Daily")
        ]
        cursor.executemany("""
            INSERT INTO routines (title, category, time_slot, priority, frequency)
            VALUES (?, ?, ?, ?, ?)
        """, sample_routines)
        conn.commit()

        # Mark some sample routines as completed for today to showcase initial stats
        today_str = date.today().isoformat()
        cursor.execute("SELECT id FROM routines LIMIT 3")
        rows = cursor.fetchall()
        for r in rows:
            cursor.execute("""
                INSERT OR REPLACE INTO daily_logs (routine_id, log_date, completed, completion_time, notes)
                VALUES (?, ?, 1, CURRENT_TIMESTAMP, 'Completed on time!')
            """, (r["id"], today_str))
        conn.commit()

    conn.close()

def get_all_routines(active_only=True):
    """Fetch all routines from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM routines"
    if active_only:
        query += " WHERE is_active = 1"
    query += " ORDER BY time_slot ASC"
    cursor.execute(query)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_routine(title, category, time_slot, priority="Medium", frequency="Daily"):
    """Add a new routine to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO routines (title, category, time_slot, priority, frequency)
        VALUES (?, ?, ?, ?, ?)
    """, (title.strip(), category, time_slot, priority, frequency))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_routine(routine_id, title, category, time_slot, priority, frequency):
    """Update an existing routine."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE routines
        SET title = ?, category = ?, time_slot = ?, priority = ?, frequency = ?
        WHERE id = ?
    """, (title.strip(), category, time_slot, priority, frequency, routine_id))
    conn.commit()
    conn.close()

def delete_routine(routine_id):
    """Delete a routine and its logs."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM daily_logs WHERE routine_id = ?", (routine_id,))
    cursor.execute("DELETE FROM routines WHERE id = ?", (routine_id,))
    conn.commit()
    conn.close()

def get_routines_with_status(target_date):
    """
    Get all routines along with their completion status for a specific date (YYYY-MM-DD).
    """
    target_date_str = str(target_date)
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT 
            r.id,
            r.title,
            r.category,
            r.time_slot,
            r.priority,
            r.frequency,
            COALESCE(l.completed, 0) AS completed,
            l.completion_time,
            COALESCE(l.notes, '') AS notes
        FROM routines r
        LEFT JOIN daily_logs l 
            ON r.id = l.routine_id AND l.log_date = ?
        WHERE r.is_active = 1
        ORDER BY r.time_slot ASC
    """
    cursor.execute(query, (target_date_str,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def set_routine_status(routine_id, target_date, completed, notes=""):
    """Mark a routine as completed or pending for a given date."""
    target_date_str = str(target_date)
    conn = get_connection()
    cursor = conn.cursor()
    comp_val = 1 if completed else 0
    comp_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if completed else None

    cursor.execute("""
        INSERT INTO daily_logs (routine_id, log_date, completed, completion_time, notes)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(routine_id, log_date) DO UPDATE SET
            completed = excluded.completed,
            completion_time = excluded.completion_time,
            notes = excluded.notes
    """, (routine_id, target_date_str, comp_val, comp_time, notes))
    conn.commit()
    conn.close()

def get_all_logs_data():
    """Retrieve all logs joined with routines for analytics."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT 
            l.log_date,
            l.routine_id,
            r.title,
            r.category,
            r.priority,
            l.completed,
            l.completion_time
        FROM daily_logs l
        JOIN routines r ON l.routine_id = r.id
        ORDER BY l.log_date ASC
    """
    cursor.execute(query)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
