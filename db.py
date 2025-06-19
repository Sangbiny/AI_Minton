import sqlite3
import json

DB_FILE = "match_records.db"

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
            timestamp TEXT NOT NULL UNIQUE,
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
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [row["timestamp"] for row in rows]

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

def rename_record_db(old_name, new_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE records SET timestamp = ? WHERE timestamp = ?", (new_name, old_name))
    conn.commit()
    cur.close()
    conn.close()

def delete_record_db(timestamp):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM records WHERE timestamp = ?", (timestamp,))
    conn.commit()
    cur.close()
    conn.close()

