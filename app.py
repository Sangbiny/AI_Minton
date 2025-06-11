from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os
import sqlite3
from datetime import datetime
from db import init_db

app = Flask(__name__)

DB_FILE = "match_web.db"
MATCH_EXECUTABLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "match")

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "GET":
        return render_template("index.html", result=None)

    total_game_count = request.form.get("total_game_count", "").strip()
    if not total_game_count.isdigit():
        return "게임 수는 숫자여야 합니다."

    players = []
    i = 1
    while True:
        name = request.form.get(f"name{i}")
        gender = request.form.get(f"gender{i}")
        level = request.form.get(f"level{i}")
        if not name:
            break
        players.append({"name": name.strip(), "gender": gender, "level": level})
        i += 1

    input_text = f"{total_game_count}\n" + "\n".join(f"{p['name']} {p['gender']} {p['level']}" for p in players)
    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(input_text)

    subprocess.run([MATCH_EXECUTABLE], check=True)

    with open("result_of_match.txt", "r", encoding="utf-8") as f:
        result_lines = [line.strip() for line in f if line.strip()]

    with open("games_per_member.txt", "r", encoding="utf-8") as f:
        count_lines = [line.strip().split() for line in f if line.strip()]
        game_counts = {name: count for name, count in count_lines}

    folder = datetime.now().strftime("%Y%m%d_%H%M%S")
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO match_records (folder) VALUES (?)", (folder,))
    record_id = c.lastrowid

    for idx, line in enumerate(result_lines):
        parts = line.split()
        c.execute("""INSERT INTO match_result (record_id, match_order, player1, player2, player3, player4)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (record_id, idx + 1, *parts[:4]))

    for name, count in game_counts.items():
        c.execute("INSERT INTO game_counts (record_id, name, count) VALUES (?, ?, ?)",
                  (record_id, name, int(count)))

    conn.commit()
    conn.close()

    result = "\n".join(result_lines)
    return render_template("index.html", players=players, result=result, game_counts=game_counts)

@app.route("/records")
def show_records():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, folder FROM match_records ORDER BY created_at DESC")
    folders = c.fetchall()
    conn.close()
    return render_template("records.html", record_folders=folders)

@app.route("/records/<folder>")
def record_detail(folder):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT id FROM match_records WHERE folder = ?", (folder,))
    row = c.fetchone()
    if not row:
        return "기록을 찾을 수 없습니다."
    record_id = row[0]

    c.execute("SELECT match_order, player1, player2, player3, player4 FROM match_result WHERE record_id = ? ORDER BY match_order", (record_id,))
    result_lines = [f"{row[1]} {row[2]} {row[3]} {row[4]}" for row in c.fetchall()]

    c.execute("SELECT name, count FROM game_counts WHERE record_id = ?", (record_id,))
    game_counts = {name: count for name, count in c.fetchall()}

    conn.close()
    match_result = "\n".join(result_lines)

    return render_template("record_detail.html", folder_name=folder, match_result=match_result, game_counts=game_counts)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5050)

