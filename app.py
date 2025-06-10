from flask import Flask, render_template, request, send_from_directory
import subprocess
import os
import traceback
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "input.txt")
MATCH_RESULT_FILE = os.path.join(BASE_DIR, "result_of_match.txt")
GAME_COUNT_FILE = os.path.join(BASE_DIR, "games_per_member.txt")
MATCH_EXECUTABLE = os.path.join(BASE_DIR, "match")
RECORDS_DIR = os.path.join(BASE_DIR, "records")
LOG_FILE = os.path.join(BASE_DIR, "log.txt")

os.makedirs(RECORDS_DIR, exist_ok=True)

def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print(message)

@app.route("/")
def start_page():
    return render_template("start.html")

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "GET":
        return render_template("index.html", result=None)

    try:
        log("== 매칭 요청 수신 ==")

        # 총 게임 수
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

        with open(INPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"{total_game_count}\n")
            for p in players:
                f.write(f"{p['name']} {p['gender']} {p['level']}\n")
        log("[파일] input.txt 저장 완료")

        if not os.path.exists(MATCH_EXECUTABLE):
            return "매칭 실행파일이 없습니다."
        if not os.access(MATCH_EXECUTABLE, os.X_OK):
            return "match 실행파일에 실행 권한이 없습니다."

        subprocess.run([MATCH_EXECUTABLE], check=True)
        log("[실행] match 실행 완료")

        match_output = ""
        if os.path.exists(MATCH_RESULT_FILE):
            with open(MATCH_RESULT_FILE, "r", encoding="utf-8") as f:
                match_output = f.read()
            log("[파일] result_of_match.txt 읽기 완료")

        game_count_output = {}
        if os.path.exists(GAME_COUNT_FILE):
            with open(GAME_COUNT_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        name, count = parts
                        game_count_output[name] = count
            log("[파일] games_per_member.txt 읽기 완료")

        # 저장용 디렉토리 만들기
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        record_path = os.path.join(RECORDS_DIR, timestamp)
        os.makedirs(record_path, exist_ok=True)
        with open(os.path.join(record_path, "result_of_match.txt"), "w", encoding="utf-8") as f:
            f.write(match_output)
        with open(os.path.join(record_path, "games_per_member.txt"), "w", encoding="utf-8") as f:
            for name, count in game_count_output.items():
                f.write(f"{name} {count}\n")
        log(f"[기록] {record_path} 에 저장 완료")

        return render_template("index.html", players=players, result=match_output, game_counts=game_count_output)

    except Exception as e:
        err = f"에러 발생: {str(e)}\n{traceback.format_exc()}"
        log(err)
        return err

@app.route("/records")
def show_records():
    folders = sorted(os.listdir(RECORDS_DIR))
    return render_template("records.html", record_folders=folders)

@app.route("/records/<folder>")
def show_record_detail(folder):
    record_path = os.path.join(RECORDS_DIR, folder)
    result_file = os.path.join(record_path, "result_of_match.txt")
    game_file = os.path.join(record_path, "games_per_member.txt")

    match_output = ""
    game_counts = {}

    if os.path.exists(result_file):
        with open(result_file, "r", encoding="utf-8") as f:
            match_output = f.read()

    if os.path.exists(game_file):
        with open(game_file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    name, count = parts
                    game_counts[name] = count

    return render_template("index.html", players=[], result=match_output, game_counts=game_counts)

@app.route("/log")
def show_log():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except Exception as e:
        return f"로그 파일을 읽는 중 오류 발생: {e}"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)

