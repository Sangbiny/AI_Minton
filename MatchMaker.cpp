#include "player.h"
#include "MatchMaker.h"
#include <vector>
#include <algorithm> // sort
#include <iostream>
#include <fstream>
#include <cstdlib>  // rand, srand
#include <ctime>    // time
#include <random>

void matchPlayers(std::vector<Player>& players, int currentGameIndex, std::ostream& out) {
    // 1. 전체 플레이어 중 WAITING 상태였던 것을 이제 경기 번호 비교로 대체
    std::vector<Player*> waitingPlayers;
    for (Player& p : players) {
        waitingPlayers.push_back(&p); // 전체 다 포함
    }

    // 2. 게임 수 오름차순 정렬
    std::sort(waitingPlayers.begin(), waitingPlayers.end(),
              [](Player* a, Player* b) {
                  return a->getGames() < b->getGames();
              });

    // 3. 가장 적은 게임 수 찾기
    int minGames = waitingPlayers.front()->getGames();

    // 4. minGames인 후보만 추출
    std::vector<Player*> candidates;
    for (Player* p : waitingPlayers) {
        if (p->getGames() == minGames) {
            candidates.push_back(p);
        } else {
            break;
        }
    }

    // 5. 후보 중에서 state가 현재 경기 번호가 아닌 사람들을 우선 추출
    std::vector<Player*> preferred;
    std::vector<Player*> fallback;

    for (Player* p : candidates) {
        if (p->getStates() != currentGameIndex) {
            preferred.push_back(p);
        } else {
            fallback.push_back(p);
        }
    }

    // 6. 랜덤 셔플
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(preferred.begin(), preferred.end(), g);
    std::shuffle(fallback.begin(), fallback.end(), g);

    std::vector<Player*> result;
    for (Player* p : preferred) {
        if (result.size() < 4) result.push_back(p);
    }
    for (Player* p : fallback) {
        if (result.size() < 4) result.push_back(p);
    }

    if (result.size() < 4) {
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 매칭 인원이 부족합니다.\n";
        return;
    }

    // 7. 매칭 결과 반영
    for (int i = 0; i < 4; ++i) {
        result[i]->incrementGames();
        result[i]->setStates(currentGameIndex);  // 현재 경기 번호로 state 설정
        out << result[i]->getName();
        if (i == 3) out << "\n";
        else        out << " ";
    }
}

