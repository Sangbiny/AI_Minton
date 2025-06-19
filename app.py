from flask import Flask, render_template, request, redirect, url_for
from db import init_db, save_match_record, load_all_records, load_record
from datetime import datetime
import os
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("start.html")

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "POST":
        total_game_count = int(request.form["total_game_count"])
        players = []
        idx = 1
        while f"name{idx}" in request.form:
            name = request.form.get(f"name{idx}")
            gender = request.form.get(f"gender{idx}")
            level = request.form.get(f"level{idx}")
            if name:
                players.append((name.strip(), gender, level))
            idx += 1

        # 저장 파일 이름을 yyyy-mm-dd 형식으로 변경
        timestamp = datetime.now().strftime("%Y-%m-%d")
        match_result, game_counts = run_match_algorithm(players, total_game_count)
        save_match_record(timestamp, match_result, game_counts)

        return render_template(
            "index.html",
            result=match_result,
            game_counts=game_counts,
            folder_name=timestamp,
        )

    # 🛠 GET 요청 처리 보완
    return render_template("index.html", result=None, game_counts={})

@app.route("/records")
def records():
    folders = load_all_records()
    return render_template("records.html", folders=folders)

@app.route("/record/<folder>")
def record_detail(folder):
    match_result, game_counts = load_record(folder)
    return render_template(
        "record_detail.html",
        match_result=match_result,
        game_counts=game_counts,
        folder_name=folder,
    )

def run_match_algorithm(players, total_game_count):
    # 간단한 매칭 알고리즘 placeholder
    result_lines = []
    game_counts = {}
    for i in range(total_game_count):
        match = [p[0] for p in players[i % len(players):i % len(players) + 4]]
        result_lines.append(" ".join(match))
        for name in match:
            game_counts[name] = game_counts.get(name, 0) + 1
    return "\n".join(result_lines), game_counts

# 🛠 Render 환경에서도 DB 초기화가 실행되도록 보장
with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)

