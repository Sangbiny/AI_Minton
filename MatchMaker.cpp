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

    // 최소 게임 수 찾기
    int minGames = INT_MAX;
    for (auto* p : playerPtrs) {
        minGames = std::min(minGames, p->getGames());
    }

    // 직전 경기 출전자 이름 모음
    std::set<std::string> lastGamePlayers;
    for (auto* p : playerPtrs) {
        if (p->getStates() == currentGameIndex - 1) {
            lastGamePlayers.insert(p->getName());
        }
    }

    // 후보자 구성 (게임 수 적고, 직전 경기 출전 아님)
    std::vector<Player*> candidates;
    for (auto* p : playerPtrs) {
        if (p->getGames() == minGames && lastGamePlayers.count(p->getName()) == 0) {
            candidates.push_back(p);
        }
    }

    // 부족 시 직전 경기 출전자 추가
    if (candidates.size() < 4) {
        for (auto* p : playerPtrs) {
            if (p->getGames() == minGames && lastGamePlayers.count(p->getName())) {
                if (std::find(candidates.begin(), candidates.end(), p) == candidates.end()) {
                    candidates.push_back(p);
                }
            }
        }
    }

    // 그래도 부족하면 그 이상 게임한 사람도 추가
    if (candidates.size() < 4) {
        for (auto* p : playerPtrs) {
            if (std::find(candidates.begin(), candidates.end(), p) == candidates.end()) {
                candidates.push_back(p);
            }
        }
    }

    // 랜덤 섞기
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(candidates.begin(), candidates.end(), g);

    // 4명만 선택
    if (candidates.size() < 4) {
        out << "== 제 " << currentGameIndex + 1 << " 경기: 매칭 실패 (최종후보 부족)\n";
        return;
    }

    std::vector<Player*> match;
    for (int i = 0; i < 4; ++i) {
        match.push_back(candidates[i]);
    }

    // 매칭 출력 + 상태 갱신
    out << "== 제 " << currentGameIndex + 1 << " 경기: ";
    for (auto* p : match) {
        out << p->getName() << " ";
        p->incrementGames();
        p->setStates(currentGameIndex);
    }
    out << "\n";
}

