from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess
import traceback
from datetime import datetime
from db import init_db, save_record, get_all_records, get_record_detail, delete_record

app = Flask(__name__)

# Constants
INPUT_FILE = "input.txt"
MATCH_RESULT_FILE = "result_of_match.txt"
GAME_COUNT_FILE = "games_per_member.txt"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATCH_EXECUTABLE = os.path.join(BASE_DIR, "match")
LOG_FILE = os.path.join(BASE_DIR, "log.txt")
DB_PATH = os.path.join(BASE_DIR, "records.db")

def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message)

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/match", methods=["GET"])
def show_match_form():
    return render_template("index.html", result=None)

@app.route("/match", methods=["POST"])
def run_match():
    try:
        log("== 매칭 요청 수신 ==")

        total_game_count = request.form.get("total_game_count", "").strip()
        log(f"[입력] 총 게임 수: {total_game_count}")
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

        log(f"[입력] 참가자 수: {len(players)}")

        # input.txt 작성
        with open(INPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"{total_game_count}\n")
            for p in players:
                f.write(f"{p['name']} {p['gender']} {p['level']}\n")
        log("[파일] input.txt 저장 완료")

        # match 실행
        if not os.path.exists(MATCH_EXECUTABLE):
            raise FileNotFoundError("match 실행파일이 존재하지 않습니다.")
        if not os.access(MATCH_EXECUTABLE, os.X_OK):
            raise PermissionError("match 실행파일에 실행 권한이 없습니다.")

        subprocess.run([MATCH_EXECUTABLE], check=True)
        log("[실행] match 실행 완료")

        # 결과 파일 읽기
        match_output = ""
        game_counts = {}

        if os.path.exists(MATCH_RESULT_FILE):
            with open(MATCH_RESULT_FILE, "r", encoding="utf-8") as f:
                match_output = f.read()
            log("[파일] result_of_match.txt 읽기 완료")

        if os.path.exists(GAME_COUNT_FILE):
            with open(GAME_COUNT_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        name, count = parts
                        game_counts[name] = count
            log("[파일] games_per_member.txt 읽기 완료")

        # DB 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_record(match_output, game_counts)
        log(f"[DB] 기록 저장 완료: {timestamp}")

        return render_template("index.html", players=players, result=match_output, game_counts=game_counts)

    except Exception as e:
        error_msg = traceback.format_exc()
        log("[오류 발생]\n" + error_msg)
        return f"<h2>서버 내부 오류</h2><pre>{error_msg}</pre>"

@app.route("/records")
def show_records():
    folders = get_all_records(DB_PATH)
    return render_template("records.html", record_folders=folders)

@app.route("/records/<folder>")
def show_record_detail(folder):
    match_result, game_counts = get_record_detail(DB_PATH, folder)
    return render_template("record_detail.html", folder_name=folder, match_result=match_result, game_counts=game_counts)

@app.route("/delete/<folder>", methods=["POST"])
def delete(folder):
    password = request.form.get("password")
    if password != "4568":
        return "<script>alert('비밀번호가 틀렸습니다.'); window.location.href='/records';</script>"
    delete_record(DB_PATH, folder)
    return redirect(url_for("show_records"))

if __name__ == "__main__":
    init_db(DB_PATH)
    app.run(debug=True, host="0.0.0.0", port=5050)

