# app.py
import os
import datetime
import subprocess
import traceback
from flask import Flask, render_template, request, redirect, url_for, flash
from db import init_db, save_record, get_all_records, get_record_detail, delete_record

app = Flask(__name__)
app.secret_key = "your_secret_key"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATCH_EXEC = os.path.join(BASE_DIR, "match")
INPUT_FILE = os.path.join(BASE_DIR, "input.txt")

# 로그 기록 함수
def log_message(message):
    with open(os.path.join(BASE_DIR, "log.txt"), "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {message}\n")

@app.route("/")
def start_page():
    return render_template("start.html")

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "POST":
        try:
            total_game_count = int(request.form.get("total_game_count", 20))
            players = []
            i = 1
            while True:
                name = request.form.get(f"name{i}")
                if not name:
                    break
                gender = request.form.get(f"gender{i}", "M")
                level = request.form.get(f"level{i}", "C")
                players.append((name.strip(), gender, level))
                i += 1

            if len(players) < 4:
                flash("최소 4명 이상의 참가자가 필요합니다.")
                return redirect(url_for("match"))

            with open(INPUT_FILE, "w", encoding="utf-8") as f:
                f.write(f"{total_game_count}\n{len(players)}\n")
                for p in players:
                    f.write(" ".join(p) + "\n")

            log_message(f"[입력 저장] 총 게임 수: {total_game_count}, 참가자 수: {len(players)}")

            result = subprocess.run([MATCH_EXEC], check=True, capture_output=True, text=True)
            log_message("[매칭 실행 완료]")

            with open("result_of_match.txt", "r", encoding="utf-8") as f:
                match_output = f.read()
            with open("games_per_member.txt", "r", encoding="utf-8") as f:
                game_count_output = f.read()

            save_record(match_output, game_count_output)

            game_counts = {}
            for line in game_count_output.strip().split("\n"):
                name, count = line.split()
                game_counts[name] = count

            return render_template("index.html", players=players, result=match_output, game_counts=game_counts)

        except Exception as e:
            error_detail = traceback.format_exc()
            log_message(f"[에러 발생]\n{error_detail}")
            return "서버 내부 오류가 발생했습니다. 로그를 확인하세요.", 500

    return render_template("index.html", players=[], result=None)

@app.route("/records")
def records():
    folders = get_all_records()
    return render_template("records.html", record_folders=folders)

@app.route("/records/<folder>")
def record_detail(folder):
    match_result, game_counts = get_record_detail(folder)
    return render_template("record_detail.html", folder_name=folder, match_result=match_result, game_counts=game_counts)

@app.route("/records/delete/<folder>", methods=["POST"])
def delete(folder):
    password = request.form.get("password")
    if password != "4568":
        flash("비밀번호가 틀렸습니다.")
        return redirect(url_for("record_detail", folder=folder))

    try:
        delete_record(folder)
        flash(f"{folder} 기록이 삭제되었습니다.")
        return redirect(url_for("records"))
    except Exception as e:
        flash(f"삭제 실패: {str(e)}")
        return redirect(url_for("record_detail", folder=folder))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
