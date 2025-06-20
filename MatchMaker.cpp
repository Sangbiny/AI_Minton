#include "player.h"
#include "MatchMaker.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <random>
#include <map>

void matchPlayers(std::vector<Player>& players, int currentGameIndex, std::ostream& out) {
    // 전체 플레이어 포인터 리스트 (정렬용)
    std::vector<Player*> allPlayers;
    for (Player& p : players) {
        allPlayers.push_back(&p);
    }

    if (allPlayers.size() < 4) {
        std::cout << "[ERROR] 플레이어 수가 4명 미만입니다.\n";
        return;
    }

    // 1. 게임 수 오름차순 정렬
    std::sort(allPlayers.begin(), allPlayers.end(),
              [](Player* a, Player* b) {
                  return a->getGames() < b->getGames();
              });

    // 2. 게임 수별로 그룹화
    std::map<int, std::vector<Player*>> gameGroup;
    for (Player* p : allPlayers) {
        gameGroup[p->getGames()].push_back(p);
    }

    // 3. 매칭할 후보 추출
    std::vector<Player*> preferred;  // state != currentGameIndex
    std::vector<Player*> fallback;   // state == currentGameIndex

    for (const auto& [games, group] : gameGroup) {
        for (Player* p : group) {
            if (p->getStates() != currentGameIndex)
                preferred.push_back(p);
            else
                fallback.push_back(p);
        }
        if (preferred.size() + fallback.size() >= 4)
            break; // 4명 확보되면 stop
    }

    if (preferred.size() + fallback.size() < 4) {
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 매칭할 인원이 부족합니다.\n";
        return;
    }

    // 4. 랜덤 셔플
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(preferred.begin(), preferred.end(), g);
    std::shuffle(fallback.begin(), fallback.end(), g);

    // 5. 최종 선발
    std::vector<Player*> result;
    for (Player* p : preferred) {
        if (result.size() < 4) result.push_back(p);
    }
    for (Player* p : fallback) {
        if (result.size() < 4) result.push_back(p);
    }

    if (result.size() < 4) {
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 최종 매칭 실패\n";
        return;
    }

    // 6. 매칭 결과 적용 및 출력
    for (int i = 0; i < 4; ++i) {
        result[i]->incrementGames();
        result[i]->setStates(currentGameIndex);
        out << result[i]->getName();
        if (i == 3) out << "\n";
        else        out << " ";
    }
}

