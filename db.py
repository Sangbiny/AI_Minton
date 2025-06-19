import os
import json
from datetime import datetime

def get_unique_folder_name(base_name, records_dir="records"):
    count = 1
    folder_name = base_name
    while os.path.exists(os.path.join(records_dir, folder_name)):
        count += 1
        folder_name = f"{base_name} ({count})"
    return folder_name

def save_record(match_result, game_counts):
    date_str = datetime.now().strftime("%Y-%m-%d")  # ✅ 원하는 날짜 포맷
    print("✅ 날짜 포맷 테스트:", date_str)  # ✅ Render 로그 확인용 디버깅 출력

    base_folder = get_unique_folder_name(date_str)
    folder_path = os.path.join("records", base_folder)
    os.makedirs(folder_path, exist_ok=True)

    with open(os.path.join(folder_path, "result_of_match.txt"), "w", encoding="utf-8") as f:
        f.write(match_result)

    with open(os.path.join(folder_path, "game_counts.json"), "w", encoding="utf-8") as f:
        json.dump(game_counts, f, ensure_ascii=False, indent=2)

def load_all_records():
    if not os.path.exists("records"):
        return []
    return sorted(os.listdir("records"), reverse=True)

def load_record_detail(folder_name):
    folder_path = os.path.join("records", folder_name)
    result_path = os.path.join(folder_path, "result_of_match.txt")
    game_counts_path = os.path.join(folder_path, "game_counts.json")

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

def rename_record(old_name, new_name):
    old_path = os.path.join("records", old_name)
    new_path = os.path.join("records", new_name)
    if os.path.exists(old_path) and not os.path.exists(new_path):
        os.rename(old_path, new_path)
        return True
    return False

