# create_db.py
from db import get_db_connection

conn = get_db_connection()
conn.close()
print("✅ DB 연결 및 테이블 생성 완료")

