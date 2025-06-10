from flask import Flask, render_template, request
import subprocess
import os
import traceback
import shutil
from datetime import datetime

app = Flask(__name__)

INPUT_FILE = "input.txt"
MATCH_RESULT_FILE = "result_of_match.txt"
GAME_COUNT_FILE = "games_per_member.txt"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATCH_EXECUTABLE = os.path.join(BASE_DIR, "match")
LOG_FILE = "log.txt"

def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message)

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "GET":
        return render_template("index.html", result=None)

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
        log(f"[파일] input.txt 저장 완료")

        if not os.path.exists(MATCH_EXECUTABLE):
            log(f"[오류] 실행파일 없음: {MATCH_EXECUTABLE}")
            return f"Error: match 실행파일이 존재하지 않습니다: {MATCH_EXECUTABLE}"
        if not os.access(MATCH_EXECUTABLE, os.X_OK):
            log(f"[오류] 실행권한 없음: {MATCH_EXECUTABLE}")
            return f"Error: match 실행파일에 실행 권한이 없습니다"

        log(f"[실행] match 실행 시작: {MATCH_EXECUTABLE}")
        subprocess.run([MATCH_EXECUTABLE], check=True)
        log("[실행] match 실행 완료")

        # 매칭 결과 읽기
        match_output = ""
        if os.path.exists(MATCH_RESULT_FILE):
            with open(MATCH_RESULT_FILE, "r", encoding="utf-8") as f:
                match_output = f.read()
            log("[파일] result_of_match.txt 읽기 완료")

        # 멤버별 게임 수 읽기
        game_count_output = {}
        if os.path.exists(GAME_COUNT_FILE):
            with open(GAME_COUNT_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        name, count = parts
                        game_count_output[name] = count
            log("[파일] games_per_member.txt 읽기 완료")

        # 기록 디렉토리에 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        record_dir = os.path.join(BASE_DIR, "records", timestamp)
        os.makedirs(record_dir, exist_ok=True)
        shutil.copy(INPUT_FILE, os.path.join(record_dir, INPUT_FILE))
        shutil.copy(MATCH_RESULT_FILE, os.path.join(record_dir, MATCH_RESULT_FILE))
        shutil.copy(GAME_COUNT_FILE, os.path.join(record_dir, GAME_COUNT_FILE))
        log(f"[기록] {record_dir} 에 저장 완료")

        return render_template(
            "index.html",
            players=players,
            result=match_output,
            game_counts=game_count_output
        )

    except Exception as e:
        err_msg = f"에러 발생: {str(e)}\n{traceback.format_exc()}"
        log(err_msg)
        return err_msg

@app.route("/log")
def show_log():
    try:
        with open("log.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except Exception as e:
        return f"로그 파일을 읽는 중 오류 발생: {e}"

