# db.py
import os
import shutil
from datetime import datetime

def save_match_data(players, result_text):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join("records", now)
    os.makedirs(folder, exist_ok=True)

    with open(os.path.join(folder, "players.txt"), "w") as f:
        for player in players:
            f.write(" ".join(player) + "\n")

    with open(os.path.join(folder, "result.txt"), "w") as f:
        f.write(result_text)

    return now

def get_all_record_folders():
    if not os.path.exists("records"):
        return []
    return sorted(os.listdir("records"), reverse=True)

def delete_record_folder(folder):
    path = os.path.join("records", folder)
    if os.path.exists(path):
        shutil.rmtree(path)

def get_record_detail(folder_name):
    folder_path = os.path.join("records", folder_name)
    players_path = os.path.join(folder_path, "players.txt")
    result_path = os.path.join(folder_path, "result.txt")

    if not os.path.exists(result_path):
        raise FileNotFoundError("result.txt not found")

    with open(result_path, "r") as f:
        match_result = f.read()

    game_counts = {}
    per_game_play_counts = {}

    for game_index, line in enumerate(match_result.splitlines()):
        players = line.strip().split()
        for name in players:
            game_counts[name] = game_counts.get(name, 0) + 1
            if name not in per_game_play_counts:
                per_game_play_counts[name] = []
            per_game_play_counts[name].append(game_counts[name])  # 각 경기에서의 n번째 경기 정보

    return match_result, game_counts, per_game_play_counts

