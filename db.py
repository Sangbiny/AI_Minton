# db.py
import os
import psycopg2
import json

DB_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DB_URL)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id SERIAL PRIMARY KEY,
            timestamp TEXT UNIQUE NOT NULL,
            match_result TEXT NOT NULL,
            game_counts JSON NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_match_record(timestamp, match_result, game_counts):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO records (timestamp, match_result, game_counts) VALUES (%s, %s, %s)",
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
    return [row[0] for row in rows]

def load_record(timestamp):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT match_result, game_counts FROM records WHERE timestamp = %s", (timestamp,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return row[0], json.loads(row[1])
    return None, None

def rename_record_db(old_name, new_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE records SET timestamp = %s WHERE timestamp = %s", (new_name, old_name))
    conn.commit()
    cur.close()
    conn.close()

def delete_record_db(timestamp):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM records WHERE timestamp = %s", (timestamp,))
    conn.commit()
    cur.close()
    conn.close()

