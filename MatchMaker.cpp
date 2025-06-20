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

    // 1. 게임 수 오름차순 정렬
    std::sort(allPlayers.begin(), allPlayers.end(),
              [](Player* a, Player* b) {
                  return a->getGames() < b->getGames();
              });

    int minGames = allPlayers.front()->getGames();

    // 2. 게임 수가 minGames인 사람만 후보로 선정
    std::vector<Player*> candidates;
    for (Player* p : allPlayers) {
        if (p->getGames() == minGames) {
            candidates.push_back(p);
        } else {
            break;  // 정렬되어 있으므로 더 이상 안 봐도 됨
        }
    }

    // 3. 후보 중에서 이번 경기에 출전하지 않은 사람 우선
    std::vector<Player*> preferred;
    std::vector<Player*> fallback;

    for (Player* p : candidates) {
        if (p->getStates() != currentGameIndex) {
            preferred.push_back(p);
        } else {
            fallback.push_back(p);
        }
    }

    // 4. 셔플
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(preferred.begin(), preferred.end(), g);
    std::shuffle(fallback.begin(), fallback.end(), g);

    // 5. 최종 4명 선발
    std::vector<Player*> result;
    for (Player* p : preferred) {
        if (result.size() < 4) result.push_back(p);
    }
    for (Player* p : fallback) {
        if (result.size() < 4) result.push_back(p);
    }

    if (result.size() < 4) {
        std::cout << "[SKIP] 경기 " << currentGameIndex << ": minGames=" << minGames << ", 후보 부족(" << result.size() << "명)\n";
        return;
    }

    // 6. 결과 반영
    for (int i = 0; i < 4; ++i) {
        result[i]->incrementGames();
        result[i]->setStates(currentGameIndex);
        out << result[i]->getName();
        if (i == 3) out << "\n";
        else        out << " ";
    }
}

