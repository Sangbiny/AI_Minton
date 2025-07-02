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
    std::set<std::string> previousPlayers;

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
            if (result.size() < 4 && previousPlayers.find(p->getName()) == previousPlayers.end()) {
                result.push_back(p);
            }
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
            if (result.size() < 4 && previousPlayers.find(p->getName()) == previousPlayers.end()) {
                result.push_back(p);
            }
        }

        // 어쩔 수 없이 연속게임 허용 (인원이 부족한 경우)
        for (Player* p : allPlayers) {
            if (result.size() < 4 && std::find(result.begin(), result.end(), p) == result.end()) {
                result.push_back(p);
            }
        }

        if (result.size() < 4) {
            std::cout << "[ERROR] 경기 " << currentGameIndex << ": 최종 후보 부족 (" << result.size() << "명)\n";
            return;
        }

        std::set<std::string> currentTeam;
        for (Player* p : result) {
            p->incrementGames();
            currentTeam.insert(p->getName());
        }

        gameHistory[currentGameIndex] = currentTeam;
        previousPlayers = currentTeam;

        for (int i = 0; i < 4; ++i) {
            out << result[i]->getName();
            if (i == 3) out << "\n";
            else        out << " ";
        }
    }
}
