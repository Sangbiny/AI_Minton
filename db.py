# db.py
import sqlite3
from datetime import datetime

DB_PATH = "records.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS match_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_name TEXT UNIQUE,
            result_text TEXT,
            games_per_user TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_record(folder_name, result_text, games_per_user_json):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO match_records (folder_name, result_text, games_per_user, created_at)
        VALUES (?, ?, ?, ?)
    ''', (folder_name, result_text, games_per_user_json, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_all_records():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT folder_name, created_at FROM match_records ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def get_record_by_folder(folder_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT result_text, games_per_user FROM match_records WHERE folder_name = ?', (folder_name,))
    row = c.fetchone()
    conn.close()
    return row

def delete_record_by_folder(folder_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM match_records WHERE folder_name = ?', (folder_name,))
    conn.commit()
    conn.close()

