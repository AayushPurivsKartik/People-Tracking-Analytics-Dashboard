# database.py
import sqlite3
from datetime import datetime
import os

DB_NAME = "analytics.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT,
            end_time TEXT,
            total_entries INTEGER DEFAULT 0,
            total_exits INTEGER DEFAULT 0,
            peak_people INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id INTEGER,
            entry_time TEXT,
            exit_time TEXT,
            dwell_time_seconds REAL,
            session_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def get_current_session():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM sessions ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def start_session():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO sessions (start_time) VALUES (?)", (now,))
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id

def end_session(session_id, entries, exits, peak):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""UPDATE sessions SET end_time=?, total_entries=?, total_exits=?, peak_people=?
              WHERE id=?""", (now, entries, exits, peak, session_id))
    conn.commit()
    conn.close()

def log_track(track_id, entry_time=None, exit_time=None, dwell=None, session_id=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if entry_time:
        c.execute("INSERT INTO tracks (track_id, entry_time, session_id) VALUES (?, ?, ?)",
                  (track_id, entry_time, session_id))
    if exit_time:
        c.execute("""UPDATE tracks SET exit_time=?, dwell_time_seconds=?
                  WHERE track_id=? AND session_id=? AND exit_time IS NULL""",
                  (exit_time, dwell, track_id, session_id))
    conn.commit()
    conn.close()