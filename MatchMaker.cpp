#include "player.h"
#include "MatchMaker.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <random>
#include <unordered_set>

void matchPlayers(std::vector<Player>& players, int currentGameIndex, std::ostream& out) {
    std::vector<Player*> allPlayers;
    for (Player& p : players)
        allPlayers.push_back(&p);

    if (allPlayers.size() < 4) {
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 플레이어 수 부족\n";
        return;
    }

    // 1. 게임 수 오름차순 정렬
    std::sort(allPlayers.begin(), allPlayers.end(),
              [](Player* a, Player* b) {
                  return a->getGames() < b->getGames();
              });

    int minGames = allPlayers.front()->getGames();

    // 2. minGames인 사람만 추림 (최우선)
    std::vector<Player*> priority;
    for (Player* p : allPlayers) {
        if (p->getGames() == minGames)
            priority.push_back(p);
    }

    // 셔플
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(priority.begin(), priority.end(), g);

    std::vector<Player*> result;
    for (Player* p : priority) {
        if (result.size() < 4)
            result.push_back(p);
    }

    // 3. 남은 자리에 state 고려하여 추가 (게임수 == minGames + 1)
    std::unordered_set<int> existingStates;
    for (Player* p : result) {
        existingStates.insert(p->getStates());
    }

    std::vector<Player*> stateCandidates;
    std::vector<Player*> stateFallback;

    for (Player* p : allPlayers) {
        if (p->getGames() == minGames + 1 &&
            std::find(result.begin(), result.end(), p) == result.end()) {
            if (existingStates.find(p->getStates()) == existingStates.end())
                stateCandidates.push_back(p);
            else
                stateFallback.push_back(p);
        }
    }

    std::shuffle(stateCandidates.begin(), stateCandidates.end(), g);
    std::shuffle(stateFallback.begin(), stateFallback.end(), g);

    for (Player* p : stateCandidates) {
        if (result.size() < 4)
            result.push_back(p);
    }
    for (Player* p : stateFallback) {
        if (result.size() < 4)
            result.push_back(p);
    }

    if (result.size() < 4) {
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 최종 후보 부족 (" << result.size() << "명)\n";
        return;
    }

    // 4. 매칭 결과 반영
    for (int i = 0; i < 4; ++i) {
        result[i]->incrementGames();
        result[i]->setStates(currentGameIndex);
        out << result[i]->getName();
        if (i == 3) out << "\n";
        else        out << " ";
    }
}

