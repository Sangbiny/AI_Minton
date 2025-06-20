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

    // 1. 전체 정렬: 게임 수 오름차순
    std::sort(allPlayers.begin(), allPlayers.end(),
              [](Player* a, Player* b) {
                  return a->getGames() < b->getGames();
              });

    // 2. 출전 이력 기준 분리
    std::vector<Player*> preferred;
    std::vector<Player*> fallback;

    for (Player* p : allPlayers) {
        if (p->getStates() != currentGameIndex)
            preferred.push_back(p);
        else
            fallback.push_back(p);
    }

    // 3. 랜덤 셔플
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(preferred.begin(), preferred.end(), g);
    std::shuffle(fallback.begin(), fallback.end(), g);

    // 4. 최종 후보 구성
    std::vector<Player*> result;
    for (Player* p : preferred) {
        if (result.size() < 4) result.push_back(p);
    }
    for (Player* p : fallback) {
        if (result.size() < 4) result.push_back(p);
    }

    if (result.size() < 4) {
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 매칭 실패 (인원 부족)\n";
        return;
    }

    // 5. 결과 반영
    for (int i = 0; i < 4; ++i) {
        result[i]->incrementGames();
        result[i]->setStates(currentGameIndex);
        out << result[i]->getN

