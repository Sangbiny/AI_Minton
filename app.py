# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess
from db import save_match_data, get_all_record_folders, delete_record_folder, get_record_detail

app = Flask(__name__)

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "POST":
        total_game_count = int(request.form.get("total_game_count", 0))
        players = []
        for i in range(1, 21):
            name = request.form.get(f"name{i}")
            gender = request.form.get(f"gender{i}")
            level = request.form.get(f"level{i}")
            if name and gender and level:
                players.append((name.strip(), gender.strip(), level.strip()))

        if not players:
            return "선수 정보를 입력해주세요."

        os.makedirs("input", exist_ok=True)
        with open("input/input.txt", "w") as f:
            f.write(f"{len(players)} {total_game_count}\n")
            for player in players:
                f.write(" ".join(player) + "\n")

        try:
            subprocess.run(["./match"], check=True)
            with open("output/result.txt", "r") as f:
                result = f.read()

            game_counts = {}
            for line in result.splitlines():
                for name in line.strip().split():
                    game_counts[name] = game_counts.get(name, 0) + 1

            folder_name = save_match_data(players, result)
            return render_template("index.html", result=result, game_counts=game_counts, folder_name=folder_name)
        except subprocess.CalledProcessError:
            return "매칭 실행 중 오류가 발생했습니다."

    return render_template("index.html")

@app.route("/records")
def records():
    folders = get_all_record_folders()
    return render_template("records.html", record_folders=folders)

@app.route("/records/<folder_name>")
def record_detail(folder_name):
    try:
        match_result, game_counts, per_game_play_counts = get_record_detail(folder_name)
        return render_template(
            "record_detail.html",
            folder_name=folder_name,
            match_result=match_result,
            game_counts=game_counts,
            per_game_play_counts=per_game_play_counts
        )
    except Exception as e:
        print(f"[Error] record_detail: {e}")
        return "기록 상세 조회 오류"

@app.route("/delete_record", methods=["POST"])
def delete_record():
    folder = request.form.get("folder")
    password = request.form.get("password")
    if password == "1993":
        delete_record_folder(folder)
    return redirect(url_for("records"))

if __name__ == "__main__":
    app.run(debug=True)

