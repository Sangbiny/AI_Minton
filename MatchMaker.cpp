#include "MatchMaker.h"
#include <algorithm>
#include <random>
#include <set>
#include <climits>

void matchPlayers(std::vector<Player>& players, int currentGameIndex, std::ostream& out) {
    std::vector<Player*> playerPtrs;
    for (auto& p : players) {
        playerPtrs.push_back(&p);
    }

    int minGames = INT_MAX;
    for (auto* p : playerPtrs) {
        minGames = std::min(minGames, p->getGames());
    }

    std::set<std::string> lastGamePlayers;
    for (auto* p : playerPtrs) {
        if (p->getStates() == currentGameIndex - 1) {
            lastGamePlayers.insert(p->getName());
        }
    }

    std::vector<Player*> candidates;
    for (auto* p : playerPtrs) {
        if (p->getGames() == minGames && lastGamePlayers.count(p->getName()) == 0) {
            candidates.push_back(p);
        }
    }

    // 부족하면 직전 게임자 추가
    if (candidates.size() < 4) {
        for (auto* p : playerPtrs) {
            if (p->getGames() == minGames && lastGamePlayers.count(p->getName())) {
                if (std::find(candidates.begin(), candidates.end(), p) == candidates.end()) {
                    candidates.push_back(p);
                }
            }
        }
    }

    // 더 부족하면 그보다 많은 게임자도 추가
    if (candidates.size() < 4) {
        for (auto* p : playerPtrs) {
            if (std::find(candidates.begin(), candidates.end(), p) == candidates.end()) {
                candidates.push_back(p);
            }
        }
    }

    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(candidates.begin(), candidates.end(), g);

    if (candidates.size() < 4) {
        out << "== 제 " << currentGameIndex + 1 << " 경기: 매칭 실패 (후보 부족)\n";
        return;
    }

    std::vector<Player*> match;
    for (int i = 0; i < 4; ++i) {
        match.push_back(candidates[i]);
    }

    out << "== 제 " << currentGameIndex + 1 << " 경기: ";
    for (auto* p : match) {
        out << p->getName() << " ";
        p->incrementGames();
        p->setStates(currentGameIndex);
    }
    out << "\n";
}

