// MatchMaker.cpp

#include "MatchMaker.h"
#include <algorithm>
#include <random>
#include <set>
#include <climits>  // for INT_MAX

void matchPlayers(std::vector<Player>& players, int currentGameIndex, std::ostream& out) {
    std::vector<Player*> candidates;

    // 1. 최소 게임 수 찾기
    int minGames = INT_MAX;
    for (const Player& p : players) {
        if (p.getGames() < minGames) {
            minGames = p.getGames();
        }
    }

    // 2. 최소 게임 수 가진 후보 수집
    for (Player& p : players) {
        if (p.getGames() == minGames) {
            candidates.push_back(&p);
        }
    }

    // 3. 섞기
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(candidates.begin(), candidates.end(), g);

    // 4. 부족하면 예외 처리
    if (candidates.size() < 4) {
        out << "제 " << currentGameIndex + 1 << "경기: 최종 후보 부족 (" << candidates.size() << "명)\n";
        return;
    }

    // 5. 상위 4명 선택
    std::vector<Player*> matchGroup(candidates.begin(), candidates.begin() + 4);

    // 6. 출력 및 상태 업데이트
    out << "제 " << currentGameIndex + 1 << "경기: ";
    for (Player* p : matchGroup) {
        out << p->getName() << " ";
        p->incrementGames();
        p->setStates(currentGameIndex);  // 경기 번호 저장
    }
    out << "\n";
}

