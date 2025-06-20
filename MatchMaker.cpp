#include "player.h"
#include "MatchMaker.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <random>

void matchPlayers(std::vector<Player>& players, int currentGameIndex, std::ostream& out) {
    std::vector<Player*> allPlayers;
    for (Player& p : players) {
        allPlayers.push_back(&p);
    }

    if (allPlayers.size() < 4) {
        std::cout << "[ERROR] 플레이어 수가 4명 미만입니다.\n";
        return;
    }

    // 게임 수 오름차순 정렬
    std::sort(allPlayers.begin(), allPlayers.end(),
              [](Player* a, Player* b) {
                  return a->getGames() < b->getGames();
              });

    int minGames = allPlayers.front()->getGames();

    // 후보군 설정 (minGames or minGames+1)
    std::vector<Player*> candidates;
    for (Player* p : allPlayers) {
        int g = p->getGames();
        if (g == minGames || g == minGames + 1) {
            candidates.push_back(p);
        }
    }

    // candidates 중 state 기준 분리
    std::vector<Player*> preferred;
    std::vector<Player*> fallback;

    for (Player* p : candidates) {
        if (p->getStates() != currentGameIndex)
            preferred.push_back(p);
        else
            fallback.push_back(p);
    }

    // 셔플
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(preferred.begin(), preferred.end(), g);
    std::shuffle(fallback.begin(), fallback.end(), g);

    // 최종 선발
    std::vector<Player*> result;
    for (Player* p : preferred) {
        if (result.size() < 4) result.push_back(p);
    }
    for (Player* p : fallback) {
        if (result.size() < 4) result.push_back(p);
    }

    if (result.size() < 4) {
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 매칭 실패 (4명 부족)\n";
        return;
    }

    // 적용
    for (int i = 0; i < 4; ++i) {
        result[i]->incrementGames();
        result[i]->setStates(currentGameIndex);
        out << result[i]->getName();
        if (i == 3) out << "\n";
        else        out << " ";
    }
}

