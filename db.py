import sqlite3

def init_db():
    conn = sqlite3.connect("match_web.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS match_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    folder TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS match_result (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_id INTEGER,
                    match_order INTEGER,
                    player1 TEXT, player2 TEXT, player3 TEXT, player4 TEXT,
                    FOREIGN KEY (record_id) REFERENCES match_records(id)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS game_counts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_id INTEGER,
                    name TEXT,
                    count INTEGER,
                    FOREIGN KEY (record_id) REFERENCES match_records(id)
                )''')

    conn.commit()
    conn.close()
