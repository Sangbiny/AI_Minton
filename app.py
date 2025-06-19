# app.py
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
        os.makedirs("output", exist_ok=True)

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
            return "\u4e0d\u952e\u884c\u4e2d\u9519\u8bef\u53d1\u751f\u4e86\u3002"

        try:
            with open("result_of_match.txt", "r", encoding="utf-8") as f:
                result = f.read()
        except FileNotFoundError:
            return "\u7ed3\u679c\u6587\u4ef6\u4e0d\u5b58\u5728\u3002"

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
    if result is None:
        return "\u8bb0\u5f55\u6587\u4ef6\u4e0d\u5b58\u5728\u6216\u635f\u574f\u3002"
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
            return "\u5220\u9664\u8fc7\u7a0b\u4e2d\u51fa\u9519\u3002"
        return redirect(url_for("records"))
    else:
        return "\u5bc6\u7801\u9519\u8bef\u3002"

@app.route("/rename_record", methods=["POST"])
def rename_record_route():
    old_name = request.form.get("old_name")
    new_name = request.form.get("new_name")
    password = request.form.get("password")

    if password == "mju":
        from db import rename_record
        if rename_record(old_name, new_name):
            return redirect(url_for("records"))
        return "이름 변경 실패: 이미 존재하거나 폴더 없음"
    return "비밀번호가 틀렸습니다."

if __name__ == "__main__":
    app.run(debug=True)


# db.py
import os
import json
from datetime import datetime

def save_record(match_result, game_counts):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_path = f"records/{timestamp}"
    os.makedirs(folder_path, exist_ok=True)

    with open(f"{folder_path}/result_of_match.txt", "w", encoding="utf-8") as f:
        f.write(match_result)

    with open(f"{folder_path}/game_counts.json", "w", encoding="utf-8") as f:
        json.dump(game_counts, f, ensure_ascii=False, indent=2)

def load_all_records():
    if not os.path.exists("records"):
        return []
    return sorted(os.listdir("records"), reverse=True)

def load_record_detail(folder_name):
    folder_path = f"records/{folder_name}"
    result_path = f"{folder_path}/result_of_match.txt"
    game_counts_path = f"{folder_path}/game_counts.json"

    if not os.path.exists(result_path) or not os.path.exists(game_counts_path):
        return None, None, None

    with open(result_path, "r", encoding="utf-8") as f:
        match_result = f.read()

    with open(game_counts_path, "r", encoding="utf-8") as f:
        game_counts = json.load(f)

    nth_game_counts = {}
    for i, line in enumerate(match_result.splitlines(), start=1):
        names = line.strip().split()
        for name in names:
            if name not in nth_game_counts:
                nth_game_counts[name] = []
            nth_game_counts[name].append(len(nth_game_counts[name]) + 1)

    return match_result, game_counts, nth_game_counts
