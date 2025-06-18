# app.py
import os
import logging
from flask import Flask, render_template, request, redirect, url_for
from db import init_db, save_record, get_all_records, get_record_detail, delete_record, update_display_name

app = Flask(__name__)

# 로그 설정
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# DB 초기화
init_db()

@app.route("/")
def index():
    return render_template("index.html", players=[], result="", game_counts={})

@app.route("/match", methods=["GET"])
def match_page():
    return redirect(url_for("index"))

@app.route("/match", methods=["POST"])
def run_match():
    try:
        total_game_count = request.form.get("total_game_count", "20")
        logging.info(f"Total Game Count: {total_game_count}")

        players = []
        i = 1
        while True:
            name = request.form.get(f"name{i}")
            gender = request.form.get(f"gender{i}")
            level = request.form.get(f"level{i}")
            if name:
                players.append(f"{name},{gender},{level}")
                i += 1
            else:
                break

        logging.info(f"Players: {players}")

        if len(players) < 4:
            return render_template("index.html", players=players, result="플레이어가 최소 4명 필요합니다.", game_counts={})

        with open("input.txt", "w", encoding="utf-8") as f:
            f.write(f"{total_game_count}\n")
            f.write("\n".join(players))

        logging.info("input.txt 작성 완료. match 실행 시작")
        os.system("./match")

        result = ""
        if os.path.exists("result_of_match.txt"):
            with open("result_of_match.txt", "r", encoding="utf-8") as f:
                result = f.read()
        else:
            logging.error("result_of_match.txt 파일이 없습니다.")

        game_counts = {}
        if os.path.exists("games_per_member.txt"):
            with open("games_per_member.txt", "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        name, count = parts
                        game_counts[name] = int(count)
        else:
            logging.error("games_per_member.txt 파일이 없습니다.")

        save_record(result, "\n".join([f"{k} {v}" for k, v in game_counts.items()]))

        return render_template("index.html", players=players, result=result, game_counts=game_counts)

    except Exception as e:
        logging.error(f"[ERROR /match POST] {e}")
        return "오류가 발생했습니다."

@app.route("/records")
def records():
    all_records = get_all_records()
    return render_template("records.html", records=all_records)

@app.route("/records/<int:record_id>")
def record_detail(record_id):
    match_result, game_counts = get_record_detail(record_id)
    if match_result == "" and not game_counts:
        return "기록 상세 조회 오류"
    return render_template("record_detail.html", result=match_result, game_counts=game_counts, record_id=record_id)

@app.route("/records/delete/<int:record_id>", methods=["POST"])
def delete(record_id):
    delete_record(record_id)
    return redirect(url_for("records"))

@app.route("/records/rename/<int:record_id>", methods=["POST"])
def rename(record_id):
    new_name = request.form.get("new_name")
    update_display_name(record_id, new_name)
    return redirect(url_for("records"))

if __name__ == "__main__":
    app.run(debug=True)

