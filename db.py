# db.py
import sqlite3
from datetime import datetime

DB_PATH = "match_records.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    result TEXT,
                    games TEXT
                )''')
    conn.commit()
    conn.close()

def save_record(result_text, games_text):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    c.execute("INSERT INTO records (timestamp, result, games) VALUES (?, ?, ?)", (now, result_text, games_text))
    conn.commit()
    conn.close()

def get_all_records():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, timestamp FROM records ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_record_detail(record_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, result, games FROM records WHERE id = ?", (record_id,))
    row = c.fetchone()
    conn.close()
    return row

def delete_record(record_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

