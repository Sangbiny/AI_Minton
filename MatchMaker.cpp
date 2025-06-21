#include "MatchMaker.h"
#include <algorithm>
#include <random>
#include <set>

void matchPlayers(std::vector<Player>& players, int currentGameIndex, std::ostream& out) {
    std::vector<Player*> sortedPlayers;
    for (auto& p : players) {
        sortedPlayers.push_back(&p);
    }

    // 게임수 기준 정렬 (오름차순)
    std::sort(sortedPlayers.begin(), sortedPlayers.end(), [](Player* a, Player* b) {
        return a->getGames() < b->getGames();
    });

    std::set<std::string> lastGamePlayers;
    for (auto& p : players) {
        if (p.getStates() == currentGameIndex - 1) {
            lastGamePlayers.insert(p.getName());
        }
    }

    std::vector<Player*> candidates;
    // 연속 출전은 피하기 위해 lastGame에 없으면서 게임수가 적은 후보 먼저 채택
    for (auto* p : sortedPlayers) {
        if (lastGamePlayers.find(p->getName()) == lastGamePlayers.end()) {
            candidates.push_back(p);
        }
    }

    // 그래도 부족하면 lastGame에 포함된 사람도 추가
    for (auto* p : sortedPlayers) {
        if (std::find(candidates.begin(), candidates.end(), p) == candidates.end()) {
            candidates.push_back(p);
        }
    }

    // 후보 섞기 (랜덤)
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(candidates.begin(), candidates.end(), g);

    std::vector<Player*> selected;
    std::set<std::string> alreadyPicked;

    for (auto* p : candidates) {
        if (selected.size() < 4 && alreadyPicked.find(p->getName()) == alreadyPicked.end()) {
            selected.push_back(p);
            alreadyPicked.insert(p->getName());
        }
    }

    if (selected.size() < 4) {
        out << "== 제 " << currentGameIndex + 1 << " 경기: 매칭 실패 (최종후보 부족 " << selected.size() << "명)\n";
        return;
    }

    out << "== 제 " << currentGameIndex + 1 << " 경기: ";
    for (auto* p : selected) {
        out << p->getName() << " ";
        p->incrementGames();
        p->setStates(currentGameIndex);
    }
    out << "\n";
}

