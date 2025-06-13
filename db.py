import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("환경 변수 DATABASE_URL이 설정되지 않았습니다.")
    # postgres:// → postgresql:// 교정
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # 최초 실행 시 테이블이 없으면 생성
    with app.app_context():
        db.create_all()

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    folder = db.Column(db.String(64), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

class MatchEntry(db.Model):
    __tablename__ = 'match_entries'
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'), nullable=False)
    round = db.Column(db.Integer, nullable=False)
    player1 = db.Column(db.String(64))
    player2 = db.Column(db.String(64))
    player3 = db.Column(db.String(64))
    player4 = db.Column(db.String(64))

class GameCount(db.Model):
    __tablename__ = 'game_counts'
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'), nullable=False)
    player = db.Column(db.String(64), nullable=False)
    count = db.Column(db.Integer, nullable=False)

