from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os
import traceback
from db import init_db, save_record, get_all_records, get_record_detail, delete_record

app = Flask(__name__)

INPUT_FILE = "input.txt"
MATCH_EXECUTABLE = "./match"
LOG_FILE = "log.txt"

# 서버 시작 시 DB 초기화
init_db()

def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message)

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/match", methods=["GET"])
def match_input():
    return render_template("index.html", result=None)

@app.route("/match", methods=["POST"])
def run_match():
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
        game_counts = {}
        if os.path.exists("result_of_match.txt"):
            with open("result_of_match.txt", "r", encoding="utf-8") as f:
                match_output = f.read()

        if os.path.exists("games_per_member.txt"):
            with open("games_per_member.txt", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        name, count = parts
                        game_counts[name] = count

        game_counts_str = "\n".join([f"{k} {v}" for k, v in game_counts.items()])
        save_record(match_output, game_counts_str)

        return render_template("index.html", players=players, result=match_output, game_counts=game_counts)

    except Exception as e:
        err_msg = f"[ERROR] {str(e)}\n{traceback.format_exc()}"
        log(err_msg)
        return "서버 내부 오류가 발생했습니다. 로그를 확인하세요."

@app.route("/records")
def records():
    try:
        folders = get_all_records()
        return render_template("records.html", record_folders=folders)
    except Exception as e:
        log(f"[ERROR - /records] {str(e)}\n{traceback.format_exc()}")
        return "서버 내부 오류가 발생했습니다. 로그를 확인하세요."

@app.route("/records/<timestamp>")
def record_detail(timestamp):
    try:
        match_result, game_counts = get_record_detail(timestamp)
        return render_template("record_detail.html", folder_name=timestamp, match_result=match_result, game_counts=game_counts)
    except Exception as e:
        log(f"[ERROR - /records/<timestamp>] {str(e)}\n{traceback.format_exc()}")
        return "서버 내부 오류가 발생했습니다. 로그를 확인하세요."

@app.route("/delete_record/<timestamp>", methods=["POST"])
def delete(timestamp):
    try:
        password = request.form.get("password", "")
        if password != "4568":
            return "비밀번호가 틀렸습니다."
        delete_record(timestamp)
        return redirect(url_for("records"))
    except Exception as e:
        log(f"[ERROR - delete_record] {str(e)}\n{traceback.format_exc()}")
        return "삭제 중 오류가 발생했습니다."

@app.route("/log")
def show_log():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return f"<pre>{f.read()}</pre>"
    except Exception as e:
        return f"로그 파일을 읽는 중 오류 발생: {str(e)}"

