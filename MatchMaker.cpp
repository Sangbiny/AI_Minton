// MatchMaker.cpp
#include "player.h"
#include "MatchMaker.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <random>
#include <unordered_set>

void matchPlayers(std::vector<Player>& players, int totalGameCnt, std::ostream& out) {
    for (int currentGameIndex = 0; currentGameIndex < totalGameCnt; ++currentGameIndex) {
        std::vector<Player*> allPlayers;
        for (Player& p : players)
            allPlayers.push_back(&p);

        if (allPlayers.size() < 4) {
            std::cout << "[ERROR] 경기 " << currentGameIndex << ": 플레이어 수 부족\n";
            return;
        }

        std::sort(allPlayers.begin(), allPlayers.end(),
                  [](Player* a, Player* b) {
                      return a->getGames() < b->getGames();
                  });

        int minGames = allPlayers.front()->getGames();
        std::vector<Player*> priority;
        for (Player* p : allPlayers) {
            if (p->getGames() == minGames)
                priority.push_back(p);
        }

        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(priority.begin(), priority.end(), g);

        std::vector<Player*> result;
        for (Player* p : priority) {
            if (result.size() < 4 && p->getStates() != currentGameIndex)
                result.push_back(p);
        }

        std::unordered_set<int> existingStates;
        for (Player* p : result) {
            existingStates.insert(p->getStates());
        }

        std::vector<Player*> stateCandidates;
        std::vector<Player*> stateFallback;

        for (Player* p : allPlayers) {
            if (p->getGames() == minGames + 1 &&
                std::find(result.begin(), result.end(), p) == result.end()) {
                if (existingStates.find(p->getStates()) == existingStates.end() &&
                    p->getStates() != currentGameIndex - 1)
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

        for (int i = 0; i < 4; ++i) {
            result[i]->incrementGames();
            result[i]->setStates(currentGameIndex);
            out << result[i]->getName();
            if (i == 3) out << "\n";
            else        out << " ";
        }
    }
}
