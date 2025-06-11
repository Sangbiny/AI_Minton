# db.py
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "records.db")

# DB 초기화 함수
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            match_result TEXT NOT NULL,
            game_counts TEXT NOT NULL
        )
        """)
        conn.commit()

# 기록 저장 함수
def save_record(match_result, game_counts):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        c.execute("INSERT INTO records (timestamp, match_result, game_counts) VALUES (?, ?, ?)",
                  (timestamp, match_result, game_counts))
        conn.commit()

# 전체 기록 가져오기
def get_all_records():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id, timestamp FROM records ORDER BY id DESC")
        return [row[1] for row in c.fetchall()]

# 특정 기록 상세 조회
def get_record_detail(timestamp):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT match_result, game_counts FROM records WHERE timestamp = ?", (timestamp,))
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

# 기록 삭제 함수
def delete_record(timestamp):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM records WHERE timestamp = ?", (timestamp,))
        conn.commit()

