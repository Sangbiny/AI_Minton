import os, subprocess, traceback, logging
from flask import Flask, render_template, request, redirect, url_for
from db import init_app, db, Record, MatchEntry, GameCount

app = Flask(__name__)
init_app(app)

# 로깅 설정
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route("/")
def home():
    return render_template("start.html")

@app.route("/match", methods=["GET", "POST"])
def match():
    if request.method == "GET":
        return render_template("index.html", players=[], result="", game_counts={})

    # POST 처리
    try:
        total_game_count = request.form.get("total_game_count","").strip()
        if not total_game_count.isdigit():
            raise ValueError("총 게임 수는 숫자여야 합니다.")
        players = []
        i = 1
        while True:
            name = request.form.get(f"name{i}")
            if not name:
                break
            players.append({
                "name": name.strip(),
                "gender": request.form.get(f"gender{i}"),
                "level": request.form.get(f"level{i}")
            })
            i += 1

        # 실행 파일 호출 등 기존 로직...

        # 내역을 DB로 저장
        folder = Record(folder=str(datetime.utcnow()).replace(":", "_"))
        db.session.add(folder)
        db.session.flush()

        # match_output, game_counts 필요

        # 예시: match_output 라인의 순서에 따라 MatchEntry 저장
        for idx, line in enumerate(match_output.splitlines(), start=1):
            cols = line.split()
            entry = MatchEntry(
                record_id=folder.id, round=idx,
                player1=cols[0], player2=cols[1], player3=cols[2], player4=cols[3]
            )
            db.session.add(entry)

        for player, cnt in game_counts.items():
            gc = GameCount(record_id=folder.id, player=player, count=int(cnt))
            db.session.add(gc)

        db.session.commit()
        return render_template("index.html", players=players, result=match_output, game_counts=game_counts)

    except Exception as e:
        app.logger.error(traceback.format_exc())
        return f"에러 발생: {e}"

@app.route("/records")
def records():
    recs = Record.query.order_by(Record.id.desc()).all()
    return render_template("records.html", record_folders=recs)

@app.route("/records/<int:rec_id>")
def record_detail(rec_id):
    rec = Record.query.get_or_404(rec_id)
    matches = MatchEntry.query.filter_by(record_id=rec_id).order_by(MatchEntry.round).all()
    games = GameCount.query.filter_by(record_id=rec_id).all()
    return render_template("record_detail.html", record=rec, matches=matches, games=games)

@app.route("/delete_record", methods=["POST"])
def delete_record():
    rec_id = request.form.get("record_id")
    pw = request.form.get("password")
    if pw != "4568":
        return "비밀번호가 올바르지 않습니다.", 403
    rec = Record.query.get_or_404(rec_id)
    MatchEntry.query.filter_by(record_id=rec.id).delete()
    GameCount.query.filter_by(record_id=rec.id).delete()
    db.session.delete(rec)
    db.session.commit()
    return redirect(url_for("records"))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

