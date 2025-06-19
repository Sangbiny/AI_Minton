# app.py
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
from db import init_db, save_match_record, load_all_records, load_record
import subprocess

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    return render_template("index.html", result=None)

@app.route("/match", methods=["POST"])
def match():
    total_game_count = int(request.form.get("total_game_count", 20))
    players = []

    i = 1
    while True:
        name = request.form.get(f"name{i}")
        gender = request.form.get(f"gender{i}")
        level = request.form.get(f"level{i}")
        if not name:
            break
        players.append((name.strip(), gender.strip(), level.strip()))
        i += 1

    input_lines = [f"{len(players)} {total_game_count}"]
    for p in players:
        input_lines.append(" ".join(p))

    input_text = "\n".join(input_lines)

    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(input_text)

    subprocess.run(["./match"], check=True)

    with open("result_of_match.txt", "r", encoding="utf-8") as f:
        result = f.read()

    with open("count.txt", "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")
        game_counts = {line.split()[0]: int(line.split()[1]) for line in lines if line.strip()}

    # 저장 이름 생성: yyyy-mm-dd 혹은 yyyy-mm-dd (2) 등 중복 방지
    base_date = datetime.now().strftime("%Y-%m-%d")
    existing_names = [record["folder_name"] for record in load_all_records() if record["folder_name"].startswith(base_date)]
    if base_date not in existing_names:
        folder_name = base_date
    else:
        i = 2
        while f"{base_date} ({i})" in existing_names:
            i += 1
        folder_name = f"{base_date} ({i})"

    save_match_record(folder_name, result, game_counts)
    return render_template("index.html", result=result, game_counts=game_counts, folder_name=folder_name)

@app.route("/records")
def records():
    all_records = load_all_records()
    return render_template("records.html", records=all_records)

@app.route("/records/<folder_name>")
def record_detail(folder_name):
    match_result, game_counts = load_record(folder_name)
    return render_template("record_detail.html", match_result=match_result, game_counts=game_counts, folder_name=folder_name)

if __name__ == "__main__":
    app.run(debug=True)

