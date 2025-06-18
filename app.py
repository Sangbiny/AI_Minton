from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os
from db import save_record, load_all_records, load_record_detail

app = Flask(__name__)

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "POST":
        os.makedirs("output", exist_ok=True)  # ❗ output 폴더 없으면 생성

        total_game_count = request.form.get("total_game_count", "20")
        try:
            total_game_count = int(total_game_count)
        except ValueError:
            total_game_count = 20

        with open("input.txt", "w", encoding="utf-8") as f:
            f.write(f"{total_game_count}\n")
            for i in range(1, 21):
                name = request.form.get(f"name{i}", "").strip()
                gender = request.form.get(f"gender{i}", "").strip()
                level = request.form.get(f"level{i}", "").strip()
                if name:
                    f.write(f"{name} {gender} {level}\n")

        try:
            subprocess.run(["./match"], check=True)
        except subprocess.CalledProcessError:
            return "매칭 실행 중 오류가 발생했습니다."

        try:
            with open("result_of_match.txt", "r", encoding="utf-8") as f:  # ✅ 경로 수정
                result = f.read()
        except FileNotFoundError:
            return "결과 파일을 찾을 수 없습니다."

        game_counts = {}
        for line in result.splitlines():
            for name in line.strip().split():
                game_counts[name] = game_counts.get(name, 0) + 1

        save_record(result, game_counts)
        return render_template("index.html", result=result, game_counts=game_counts)

    return render_template("index.html")

@app.route("/records")
def records():
    folders = load_all_records()
    return render_template("records.html", record_folders=folders)

@app.route("/records/<folder_name>")
def record_detail(folder_name):
    result, game_counts, nth_game_counts = load_record_detail(folder_name)
    return render_template(
        "record_detail.html",
        folder_name=folder_name,
        match_result=result,
        game_counts=game_counts,
        nth_game_counts=nth_game_counts,
    )

@app.route("/delete_record", methods=["POST"])
def delete_record():
    folder = request.form.get("folder")
    password = request.form.get("password")

    if password == "mju":
        try:
            import shutil
            shutil.rmtree(f"records/{folder}")
        except Exception:
            return "삭제 중 오류가 발생했습니다."
        return redirect(url_for("records"))
    else:
        return "비밀번호가 틀렸습니다."

if __name__ == "__main__":
    app.run(debug=True)

