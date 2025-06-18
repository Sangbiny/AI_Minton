# db.py
import os
import psycopg2
from datetime import datetime

DB_URL = os.environ.get("DATABASE_URL")

def init_db():
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as c:
                c.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    id SERIAL PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    match_result TEXT NOT NULL,
                    game_counts TEXT NOT NULL
                )
                """)
                try:
                    c.execute("ALTER TABLE records ADD COLUMN display_name TEXT")
                except:
                    pass  # 컬럼이 이미 있으면 무시
                conn.commit()
    except Exception as e:
        print(f"[DB Error - init_db] {e}")

def save_record(match_result, game_counts):
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as c:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                display_name = generate_display_name(c, timestamp)
                c.execute("INSERT INTO records (timestamp, match_result, game_counts, display_name) VALUES (%s, %s, %s, %s)",
                          (timestamp, match_result, game_counts, display_name))
                conn.commit()
    except Exception as e:
        print(f"[DB Error - save_record] {e}")

def generate_display_name(cursor, timestamp):
    date_part = timestamp.split("_")[0]
    cursor.execute("SELECT display_name FROM records WHERE display_name LIKE %s", (f"{date_part} 운동%",))
    existing = [row[0] for row in cursor.fetchall()]
    count = 1
    base_name = f"{date_part} 운동"
    new_name = base_name
    while new_name in existing:
        count += 1
        new_name = f"{base_name}({count})"
    return new_name

def get_all_records():
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as c:
                c.execute("SELECT timestamp, display_name FROM records ORDER BY id DESC")
                return [
                    {"timestamp": row[0], "display_name": row[1] or row[0]} for row in c.fetchall()
                ]
    except Exception as e:
        print(f"[DB Error - get_all_records] {e}")
        return []

def get_record_detail(folder):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT match_result, game_counts FROM records WHERE timestamp = %s", (folder,))
        row = cur.fetchone()
        conn.close()
        if row:
            return row[0], json.loads(row[1])
        else:
            return None, None
    except Exception as e:
        print(f"[DB Error - get_record_detail] {e}")
        return None, None

def delete_record(timestamp):
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as c:
                c.execute("DELETE FROM records WHERE timestamp = %s", (timestamp,))
                conn.commit()
    except Exception as e:
        print(f"[DB Error - delete_record] {e}")

def update_display_name(timestamp, new_name):
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as c:
                c.execute("UPDATE records SET display_name = %s WHERE timestamp = %s", (new_name, timestamp))
                conn.commit()
    except Exception as e:
        print(f"[DB Error - update_display_name] {e}")

