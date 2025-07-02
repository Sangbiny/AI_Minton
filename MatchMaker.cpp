// MatchMaker.cpp
#include "player.h"
#include "MatchMaker.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <random>
#include <unordered_set>
#include <map>
#include <set>

void matchPlayers(std::vector<Player>& players, int totalGameCnt, std::ostream& out) {
    std::map<int, std::set<std::string>> gameHistory;

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
            if (result.size() < 4)
                result.push_back(p);
        }

        std::vector<Player*> extraCandidates;
        for (Player* p : allPlayers) {
            if (p->getGames() == minGames + 1 &&
                std::find(result.begin(), result.end(), p) == result.end()) {
                extraCandidates.push_back(p);
            }
        }

        std::shuffle(extraCandidates.begin(), extraCandidates.end(), g);
        for (Player* p : extraCandidates) {
            if (result.size() < 4)
                result.push_back(p);
        }

        if (result.size() < 4) {
            std::cout << "[ERROR] 경기 " << currentGameIndex << ": 최종 후보 부족 (" << result.size() << "명)\n";
            return;
        }

        if (currentGameIndex > 0) {
            std::set<std::string> prevTeam = gameHistory[currentGameIndex - 1];
            std::set<std::string> currentTeam;
            for (Player* p : result)
                currentTeam.insert(p->getName());
            if (prevTeam == currentTeam) {
                std::cout << "[WARNING] 경기 " << currentGameIndex << ": 전 경기와 동일한 조합 -> 건너뜀\n";
                continue;
            }
        }

        for (Player* p : result) {
            p->incrementGames();
            gameHistory[currentGameIndex].insert(p->getName());
        }

        for (int i = 0; i < 4; ++i) {
            out << result[i]->getName();
            if (i == 3) out << "\n";
            else        out << " ";
        }
    }
}
