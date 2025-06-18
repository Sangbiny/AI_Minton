# app.py
import os
import logging
from flask import Flask, render_template, request, redirect, url_for
from db import (
    init_db, save_record, get_all_records,
    get_record_detail, delete_record, update_display_name
)

app = Flask(__name__)

# 로그 설정
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

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
        total_game_count = int(request.form.get("total_game_count", 0))
        players = []
        i = 1
        while True:
            name = request.form.get(f"name{i}")
            gender = request.form.get(f"gender{i}")
            level = request.form.get(f"level{i}")
            if not name:
                break
            players.append({"name": name, "gender": gender, "level": level})
            i += 1

        with open("input.txt", "w", encoding="utf-8") as f:
            f.write(f"{total_game_count}\n{len(players)}\n")
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

        game_counts_str = "\n".join([f"{k} {v}" for k, v in game_counts.items()])
        save_record(result, game_counts_str)

        return render_template("index.html", players=players, result=result, game_counts=game_counts)
    except Exception as e:
        logging.error(f"[run_match] {e}")
        return "오류가 발생했습니다."

@app.route("/records")
def records():
    try:
        records = get_all_records()
        return render_template("records.html", record_folders=records)
    except Exception as e:
        logging.error(f"[records] {e}")
        return "기록 불러오기 오류"

@app.route("/records/<int:record_id>")
def record_detail(record_id):
    try:
        match_result, game_counts = get_record_detail(record_id)
        return render_template("record_detail.html", folder_name=record_id, match_result=match_result, game_counts=game_counts)
    except Exception as e:
        logging.error(f"[record_detail] {e}")
        return "기록 상세 조회 오류"

@app.route("/delete_record", methods=["POST"])
def delete():
    try:
        record_id = request.form.get("record_id")
        password = request.form.get("password")
        if password != "4568":
            return "<script>alert('비밀번호가 틀렸습니다.'); history.back();</script>"

        delete_record(record_id)
        return redirect(url_for("records"))
    except Exception as e:
        logging.error(f"[delete_record] {e}")
        return "삭제 오류"

@app.route("/rename_record", methods=["POST"])
def rename_record():
    try:
        record_id = request.form.get("record_id")
        new_name = request.form.get("new_name", "").strip()
        if new_name:
            update_display_name(record_id, new_name)
        return redirect(url_for("records"))
    except Exception as e:
        logging.error(f"[rename_record] {e}")
        return "이름 변경 오류"

if __name__ == "__main__":
    app.run(debug=True)

