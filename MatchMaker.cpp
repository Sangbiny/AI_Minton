#include "MatchMaker.h"
#include <algorithm>
#include <random>
#include <set>
#include <climits> // for INT_MAX

void matchPlayers(std::vector<Player>& players, int currentGameIndex, std::ostream& out) {
    std::vector<Player*> sortedPlayers;
    for (auto& p : players) {
        sortedPlayers.push_back(&p);
    }

    // 최소 게임 수 계산
    int minGames = INT_MAX;
    for (const auto& p : players) {
        if (p.getGames() < minGames) {
            minGames = p.getGames();
        }
    }

    // 직전 경기 참가자 수집
    std::set<std::string> lastGamePlayers;
    for (const auto& p : players) {
        if (p.getStates() == currentGameIndex - 1) {
            lastGamePlayers.insert(p.getName());
        }
    }

    // 후보자: 최소 게임 수이고 직전 경기 출전 안 한 사람 우선
    std::vector<Player*> candidates;
    for (auto* p : sortedPlayers) {
        if (p->getGames() == minGames && lastGamePlayers.count(p->getName()) == 0) {
            candidates.push_back(p);
        }
    }

    // 부족할 경우, 직전 경기 참가자도 포함
    for (auto* p : sortedPlayers) {
        if (p->getGames() == minGames && std::find(candidates.begin(), candidates.end(), p) == candidates.end()) {
            candidates.push_back(p);
        }
    }

    // 그래도 부족하면 게임 수 많은 사람도 허용
    for (auto* p : sortedPlayers) {
        if (std::find(candidates.begin(), candidates.end(), p) == candidates.end()) {
            candidates.push_back(p);
        }
    }

    // 랜덤 섞기
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(candidates.begin(), candidates.end(), g);

    // 상위 4명 뽑기
    std::vector<Player*> match;
    for (auto* p : candidates) {
        if (match.size() < 4) {
            match.push_back(p);
        }
    }

    // 매칭 실패 처리
    if (match.size() < 4) {
        out << "== 제 " << currentGameIndex + 1 << " 경기: 매칭 실패 (최종후보 부족 " << match.size() << "명)\n";
        return;
    }

    // 결과 출력 및 상태 갱신
    out << "== 제 " << currentGameIndex + 1 << " 경기: ";
    for (auto* p : match) {
        out << p->getName() << " ";
        p->incrementGames();
        p->setStates(currentGameIndex);
    }
    out << "\n";
}

