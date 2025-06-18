import os
import json
from datetime import datetime

def save_record(match_result, game_counts):
    # records/ 폴더 내부에 timestamp 폴더 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_path = f"records/{timestamp}"
    os.makedirs(folder_path, exist_ok=True)

    # 결과 저장 (파일명: result_of_match.txt)
    with open(f"{folder_path}/result_of_match.txt", "w", encoding="utf-8") as f:
        f.write(match_result)

    # 게임 수 저장
    with open(f"{folder_path}/game_counts.json", "w", encoding="utf-8") as f:
        json.dump(game_counts, f, ensure_ascii=False, indent=2)

def load_all_records():
    # records 폴더가 없으면 빈 리스트 반환
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

    # nth_game_counts: 각 선수의 경기 순번 기록
    nth_game_counts = {}
    for i, line in enumerate(match_result.splitlines(), start=1):
        names = line.strip().split()
        for name in names:
            if name not in nth_game_counts:
                nth_game_counts[name] = []
            nth_game_counts[name].append(len(nth_game_counts[name]) + 1)

    return match_result, game_counts, nth_game_counts

