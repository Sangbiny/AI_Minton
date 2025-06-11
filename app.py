# app.py
from flask import Flask, render_template, request, redirect, url_for
from db import init_db, save_record, get_all_records, get_record_detail, delete_record
import subprocess
import os
import traceback

app = Flask(__name__)
init_db()

LOG_FILE = "log.txt"
MATCH_EXECUTABLE = "./match"
INPUT_FILE = "input.txt"
MATCH_RESULT_FILE = "result_of_match.txt"
GAME_COUNT_FILE = "games_per_member.txt"
DELETE_PASSWORD = "4568"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "GET":
        return render_template("index.html", players=[], result=None, game_counts={})

    try:
        total_game_count = request.form.get("total_game_count", "").strip()
        if not total_game_count.isdigit():
            raise ValueError("게임 수는 숫자여야 합니다.")

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

        with open(INPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"{total_game_count}\n")
            for p in players:
                f.write(f"{p['name']} {p['gender']} {p['level']}\n")

        subprocess.run([MATCH_EXECUTABLE], check=True)

        match_output = ""
        if os.path.exists(MATCH_RESULT_FILE):
            with open(MATCH_RESULT_FILE, "r", encoding="utf-8") as f:
                match_output = f.read()

        game_counts_output = ""
        game_counts_dict = {}
        if os.path.exists(GAME_COUNT_FILE):
            with open(GAME_COUNT_FILE, "r", encoding="utf-8") as f:
                game_counts_output = f.read()
                for line in game_counts_output.strip().split("\n"):
                    name, count = line.strip().split()
                    game_counts_dict[name] = count

        save_record(match_output, game_counts_output)

        return render_template("index.html", players=players, result=match_output, game_counts=game_counts_dict)

    except Exception as e:
        log(traceback.format_exc())
        return "서버 내부 오류가 발생했습니다. 로그를 확인하세요."

@app.route("/records")
def records():
    try:
        folders = get_all_records()
        return render_template("records.html", record_folders=folders)
    except Exception as e:
        log(traceback.format_exc())
        return "서버 내부 오류가 발생했습니다. 로그를 확인하세요."

@app.route("/records/<timestamp>")
def record_detail(timestamp):
    try:
        match_result, game_counts = get_record_detail(timestamp)
        return render_template("record_detail.html", folder_name=timestamp,
                               match_result=match_result, game_counts=game_counts)
    except Exception as e:
        log(traceback.format_exc())
        return "서버 내부 오류가 발생했습니다. 로그를 확인하세요."

@app.route("/delete/<timestamp>", methods=["POST"])
def delete(timestamp):
    try:
        password = request.form.get("password", "")
        if password == DELETE_PASSWORD:
            delete_record(timestamp)
            return redirect(url_for("records"))
        else:
            return "비밀번호가 틀렸습니다."
    except Exception as e:
        log(traceback.format_exc())
        return "서버 내부 오류가 발생했습니다. 로그를 확인하세요."

@app.route("/log")
def show_log():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except Exception as e:
        return f"로그 파일을 읽는 중 오류 발생: {e}"

if __name__ == "__main__":
    app.run(debug=True)

