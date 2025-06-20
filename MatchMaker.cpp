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
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 플레이어 수 부족\n";
        return;
    }

    // 게임 수 오름차순 정렬
    std::sort(allPlayers.begin(), allPlayers.end(),
              [](Player* a, Player* b) {
                  return a->getGames() < b->getGames();
              });

    int minGames = allPlayers.front()->getGames();

    // 후보: minGames인 사람들
    std::vector<Player*> candidates;
    for (Player* p : allPlayers) {
        if (p->getGames() == minGames)
            candidates.push_back(p);
    }

    // 부족하면 minGames + 1 사람까지 확장
    if (candidates.size() < 4) {
        for (Player* p : allPlayers) {
            if (p->getGames() == minGames + 1)
                candidates.push_back(p);
            if (candidates.size() >= 4) break;
        }
    }

    if (candidates.size() < 4) {
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 후보 부족 (" << candidates.size() << "명)\n";
        return;
    }

    // 셔플해서 4명 추출
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(candidates.begin(), candidates.end(), g);

    std::vector<Player*> result(candidates.begin(), candidates.begin() + 4);

    for (int i = 0; i < 4; ++i) {
        result[i]->incrementGames();
        result[i]->setStates(currentGameIndex);  // 상태는 써도 무시됨
        out << result[i]->getName();
        if (i == 3) out << "\n";
        else        out << " ";
    }
}

