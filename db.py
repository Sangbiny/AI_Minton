# db.py
import os
import psycopg2
from datetime import datetime

DB_URL = os.environ.get("DATABASE_URL")

# DB 초기화 함수
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
                conn.commit()
    except Exception as e:
        print(f"[DB Error - init_db] {e}")

# 기록 저장 함수
def save_record(match_result, game_counts):
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as c:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                c.execute("INSERT INTO records (timestamp, match_result, game_counts) VALUES (%s, %s, %s)",
                          (timestamp, match_result, game_counts))
                conn.commit()
    except Exception as e:
        print(f"[DB Error - save_record] {e}")

# 전체 기록 가져오기
def get_all_records():
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as c:
                c.execute("SELECT timestamp FROM records ORDER BY id DESC")
                return [row[0] for row in c.fetchall()]
    except Exception as e:
        print(f"[DB Error - get_all_records] {e}")
        return []

# 특정 기록 상세 조회
def get_record_detail(timestamp):
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as c:
                c.execute("SELECT match_result, game_counts FROM records WHERE timestamp = %s", (timestamp,))
                row = c.fetchone()
                if row:
                    match_result, game_counts_str = row
                    game_counts = {}
                    for line in game_counts_str.strip().split("\n"):
                        name, count = line.strip().split()
                        game_counts[name] = count
                    return match_result, game_counts
                else:
                    return "", {}
    except Exception as e:
        print(f"[DB Error - get_record_detail] {e}")
        return "", {}

# 기록 삭제 함수
def delete_record(timestamp):
    try:
        with psycopg2.connect(DB_URL) as conn:
            with conn.cursor() as c:
                c.execute("DELETE FROM records WHERE timestamp = %s", (timestamp,))
                conn.commit()
    except Exception as e:
        print(f"[DB Error - delete_record] {e}")

