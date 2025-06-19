from flask import Flask, render_template, request, redirect, url_for
from db import (
    init_db,
    save_match_record,
    load_all_records,
    load_record,
    rename_record_db,
    delete_record_db,
)
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("start.html")

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "POST":
        total_game_count = int(request.form.get("total_game_count", 20))
        players = []
        idx = 1
        while f"name{idx}" in request.form:
            name = request.form.get(f"name{idx}", "").strip()
            gender = request.form.get(f"gender{idx}", "")
            level = request.form.get(f"level{idx}", "")
            if name:
                players.append((name, gender, level))
            idx += 1

        if len(players) < 4:
            return "선수가 4명 이상 필요합니다."

        # timestamp → yyyy-mm-dd 형식 (중복 방지용 인덱스 붙이기)
        base_timestamp = datetime.now().strftime("%Y-%m-%d")
        timestamp = base_timestamp
        suffix = 2
        while timestamp in load_all_records():
            timestamp = f"{base_timestamp} ({suffix})"
            suffix += 1

        match_result, game_counts = run_match_algorithm(players, total_game_count)
        save_match_record(timestamp, match_result, game_counts)

        return render_template(
            "index.html",
            match_result=match_result,
            game_counts=game_counts,
            folder_name=timestamp
        )

    return render_template("index.html", match_result=None)

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

@app.route("/rename_record", methods=["POST"])
def rename_record():
    old_name = request.form["old_name"]
    new_name = request.form["new_name"]
    if new_name and new_name not in load_all_records():
        rename_record_db(old_name, new_name)
    return redirect(url_for("records"))

@app.route("/delete_record", methods=["POST"])
def delete_record():
    folder = request.form["folder"]
    delete_record_db(folder)
    return redirect(url_for("records"))

def run_match_algorithm(players, total_game_count):
    result_lines = []
    game_counts = {}

    num_players = len(players)
    if num_players < 4:
        return "", {}

    idx = 0
    for i in range(total_game_count):
        match = []
        for j in range(4):
            match.append(players[(idx + j) % num_players][0])  # 이름만 추출
        idx += 1  # 슬라이딩 윈도우 방식
        result_lines.append(" ".join(match))
        for name in match:
            game_counts[name] = game_counts.get(name, 0) + 1

    return "\n".join(result_lines), game_counts

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

