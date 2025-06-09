from flask import Flask, render_template, request
import subprocess
import os

app = Flask(__name__)

INPUT_FILE = "input.txt"
MATCH_RESULT_FILE = "result_of_match.txt"
GAME_COUNT_FILE = "games_per_member.txt"
MATCH_EXECUTABLE = "./match"  # C++ 실행파일 이름

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", result=None)

@app.route("/match", methods=["POST"])
def match():
    try:
        # 총 게임 수 읽기
        total_game_count = request.form.get("total_game_count", "").strip()
        if not total_game_count.isdigit():
            raise ValueError("게임 수는 숫자여야 합니다.")

        # 참가자 정보 수집
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

        # input.txt 작성
        with open(INPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"{total_game_count}\n")
            for p in players:
                f.write(f"{p['name']} {p['gender']} {p['level']}\n")

        # 매칭 실행 (C++ 실행파일)
        result = subprocess.run([MATCH_EXECUTABLE], capture_output=True, text=True)

        # 매칭 결과 읽기
        match_output = ""
        if os.path.exists(MATCH_RESULT_FILE):
            with open(MATCH_RESULT_FILE, "r", encoding="utf-8") as f:
                match_output = f.read()

        # 멤버별 게임 수 읽기 (딕셔너리로)
        game_count_output = {}
        if os.path.exists(GAME_COUNT_FILE):
            with open(GAME_COUNT_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        name, count = parts
                        game_count_output[name] = count

        return render_template(
            "index.html",
            players=players,
            result=match_output,
            game_counts=game_count_output
        )

    except Exception as e:
        return f"에러가 발생했습니다: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)

