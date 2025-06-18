# db.py
import os
import psycopg2
from datetime import datetime

def get_db_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')


def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id SERIAL PRIMARY KEY,
                timestamp TEXT NOT NULL,
                match_result TEXT,
                game_counts TEXT,
                display_name TEXT
            );
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB Error - init_db] {e}")


def save_record(match_result, game_counts):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        date = timestamp.split("_")[0]

        # 중복 확인 및 display_name 생성
        cur.execute("SELECT display_name FROM records WHERE display_name LIKE %s", (f"{date} 운동%",))
        existing_names = [row[0] for row in cur.fetchall()]
        if f"{date} 운동" not in existing_names:
            display_name = f"{date} 운동"
        else:
            i = 2
            while f"{date} 운동({i})" in existing_names:
                i += 1
            display_name = f"{date} 운동({i})"

        cur.execute("""
            INSERT INTO records (timestamp, match_result, game_counts, display_name)
            VALUES (%s, %s, %s, %s);
        """, (timestamp, match_result, game_counts, display_name))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB Error - save_record] {e}")


def get_all_records():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, display_name FROM records ORDER BY id DESC;")
        result = cur.fetchall()
        conn.close()
        return result
    except Exception as e:
        print(f"[DB Error - get_all_records] {e}")
        return []


def get_record_detail(record_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT match_result, game_counts FROM records WHERE id = %s;", (record_id,))
        row = cur.fetchone()
        conn.close()

        if row:
            match_result = row[0] or ""
            game_counts_text = row[1] or ""
            game_counts = {
                line.split()[0]: line.split()[1]
                for line in game_counts_text.strip().splitlines()
                if len(line.strip().split()) == 2
            }
            return match_result, game_counts
        else:
            return "", {}
    except Exception as e:
        print(f"[DB Error - get_record_detail] {e}")
        return "", {}


def delete_record(record_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM records WHERE id = %s;", (record_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB Error - delete_record] {e}")

