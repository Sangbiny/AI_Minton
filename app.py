# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess
import json
from datetime import datetime
from db import init_db, insert_record, get_all_records, get_record_by_folder, delete_record_by_folder

app = Flask(__name__)
app.secret_key = "secret"
MATCH_EXECUTABLE = "./match"

init_db()

@app.route("/")
def home():
    return render_template("start.html")

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "GET":
        return render_template("index.html", players=[], result="", game_counts={})

    # POST
    total_game_count = int(request.form.get("total_game_count", 0))
    players = []
    i = 1
    while f"name{i}" in request.form:
        name = request.form[f"name{i}"]
        gender = request.form.get(f"gender{i}")
        level = request.form.get(f"level{i}")
        if name:
            players.append(f"{name} {gender} {level}")
        i += 1

    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(f"{total_game_count}\n")
        f.write(f"{len(players)}\n")
        for p in players:
            f.write(p + "\n")

    subprocess.run([MATCH_EXECUTABLE], check=True)

    with open("result_of_match.txt", "r", encoding="utf-8") as f:
        match_result = f.read()

    game_counts = {}
    with open("games_per_member.txt", "r", encoding="utf-8") as f:
        for line in f:
            name, count = line.strip().split()
            game_counts[name] = count

    folder_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    insert_record(folder_name, match_result, json.dumps(game_counts))

    return render_template("index.html", players=players, result=match_result, game_counts=game_counts)

@app.route("/records")
def show_records():
    records = get_all_records()
    return render_template("records.html", record_folders=records)

@app.route("/records/<folder>")
def record_detail(folder):
    data = get_record_by_folder(folder)
    if not data:
        return f"기록 {folder}를 찾을 수 없습니다.", 404

    result_text, game_counts_json = data
    game_counts = json.loads(game_counts_json)

    return render_template("record_detail.html", folder_name=folder, match_result=result_text, game_counts=game_counts)

@app.route("/delete_record", methods=["POST"])
def delete_record():
    folder = request.form.get("folder")
    password = request.form.get("password")
    if password == "4568":
        delete_record_by_folder(folder)
        flash("기록이 삭제되었습니다.")
    else:
        flash("비밀번호가 틀렸습니다.")
    return redirect(url_for("show_records"))

