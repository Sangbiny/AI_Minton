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

    // 2. 게임 수별 그룹핑
    std::map<int, std::vector<Player*>> gameGroup;
    for (Player* p : allPlayers) {
        gameGroup[p->getGames()].push_back(p);
    }

    // 3. 랜덤 셔플 엔진 준비
    std::random_device rd;
    std::mt19937 g(rd());

    std::vector<Player*> result;

    // 4. 가장 낮은 게임수부터 4명이 가능한 조합이 있는지 탐색
    for (const auto& [games, group] : gameGroup) {
        std::vector<Player*> groupPreferred;
        std::vector<Player*> groupFallback;

        for (Player* p : group) {
            if (p->getStates() != currentGameIndex)
                groupPreferred.push_back(p);
            else
                groupFallback.push_back(p);
        }

        std::shuffle(groupPreferred.begin(), groupPreferred.end(), g);
        std::shuffle(groupFallback.begin(), groupFallback.end(), g);

        std::vector<Player*> groupResult;
        for (Player* p : groupPreferred) {
            if (groupResult.size() < 4) groupResult.push_back(p);
        }
        for (Player* p : groupFallback) {
            if (groupResult.size() < 4) groupResult.push_back(p);
        }

        if (groupResult.size() == 4) {
            result = groupResult;
            break; // 4명 정확히 확보되면 이 조합 사용
        }
    }

    if (result.size() < 4) {
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 매칭 실패 (4명 불충분)\n";
        return;
    }

    // 5. 최종 적용
    for (int i = 0; i < 4; ++i) {
        result[i]->incrementGames();
        result[i]->setStates(currentGameIndex);
        out << result[i]->getName();
        if (i == 3) out << "\n";
        else        out << " ";
    }
}

