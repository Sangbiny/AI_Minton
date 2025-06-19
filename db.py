# db.py
import sqlite3
import json
import os

DB_FILE = "/tmp/match_records.db"  # Render 무료 플랜에 맞춰 변경

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            match_result TEXT NOT NULL,
            game_counts TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_match_record(timestamp, match_result, game_counts):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO records (timestamp, match_result, game_counts) VALUES (?, ?, ?)",
        (timestamp, match_result, json.dumps(game_counts))
    )
    conn.commit()
    cur.close()
    conn.close()

def load_all_records():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT timestamp FROM records ORDER BY timestamp DESC")
    folders = [row["timestamp"] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return folders

def load_record(timestamp):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT match_result, game_counts FROM records WHERE timestamp = ?", (timestamp,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return row["match_result"], json.loads(row["game_counts"])
    return None, None

