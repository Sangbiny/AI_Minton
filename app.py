# app.py
import os
import logging
from flask import Flask, request, render_template, redirect, url_for
from db import (
    init_db, save_record, get_all_records,
    get_record_detail, delete_record, update_display_name
)

app = Flask(__name__)

# 로그 설정
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# DB 초기화
init_db()

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/match")
def match():
    return render_template("index.html", players=[], result="", game_counts={})

@app.route("/match", methods=["POST"])
def run_match():
    try:
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

        total_game_count = request.form.get("total_game_count", "0")
        if not total_game_count.isdigit():
            raise ValueError("게임 수는 숫자여야 합니다.")

        with open("input.txt", "w", encoding="utf-8") as f:
            f.write(f"{total_game_count}\n")
            for p in players:
                f.write(f"{p['name']} {p['gender']} {p['level']}\n")

        os.system("./match")

        result = ""
        if os.path.exists("result_of_match.txt"):
            with open("result_of_match.txt", "r", encoding="utf-8") as f:
                result = f.read()

        game_counts = {}
        if os.path.exists("games_per_member.txt"):
            with open("games_per_member.txt", "r", encoding="utf-8") as f:
                for line in f:
                    name, count = line.strip().split()
                    game_counts[name] = count

        save_record(result, "\n".join([f"{k} {v}" for k, v in game_counts.items()]))

        return render_template("index.html", players=players, result=result, game_counts=game_counts)

    except Exception as e:
        logging.error(f"[ERROR /match] {e}")
        return "오류가 발생했습니다."

@app.route("/records")
def records():
    try:
        folders = get_all_records()
        return render_template("records.html", record_folders=folders)
    except Exception as e:
        logging.error(f"[ERROR /records] {e}")
        return "기록 불러오기 오류"

@app.route("/records/<folder>")
def record_detail(folder):
    try:
        match_result, game_counts = get_record_detail(folder)

        if match_result is None or game_counts is None:
            raise ValueError("match_result or game_counts is None")

        return render_template("record_detail.html",
                               folder_name=folder,
                               match_result=match_result,
                               game_counts=game_counts)
    except Exception as e:
        logging.error(f"[ERROR /records/<folder>] {e}")
        return "기록 상세 조회 오류"


@app.route("/delete_record", methods=["POST"])
def delete():
    try:
        folder = request.form.get("folder")
        password = request.form.get("password")
        if password != "4568":
            return "<script>alert('비밀번호가 틀렸습니다.'); history.back();</script>"

        delete_record(folder)
        return redirect(url_for("records"))
    except Exception as e:
        logging.error(f"[ERROR /delete_record] {e}")
        return "삭제 중 오류 발생"

@app.route("/rename_record", methods=["POST"])
def rename():
    try:
        folder = request.form.get("folder")
        new_name = request.form.get("new_name")
        update_display_name(folder, new_name)
        return redirect(url_for("records"))
    except Exception as e:
        logging.error(f"[ERROR /rename_record] {e}")
        return "이름 변경 중 오류 발생"

if __name__ == "__main__":
    app.run(debug=True)

