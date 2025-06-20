#include "player.h"
#include "MatchMaker.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <random>

void matchPlayers(std::vector<Player>& players, int currentGameIndex, std::ostream& out) {
    // 전체 플레이어 포인터 리스트 (정렬용)
    std::vector<Player*> allPlayers;
    for (Player& p : players) {
        allPlayers.push_back(&p);
    }

    // 게임 수 오름차순 정렬
    std::sort(allPlayers.begin(), allPlayers.end(),
              [](Player* a, Player* b) {
                  return a->getGames() < b->getGames();
              });

    if (allPlayers.size() < 4) {
        std::cout << "[ERROR] 플레이어 수가 4명 미만입니다.\n";
        return;
    }

    // 최소 게임 수
    int minGames = allPlayers.front()->getGames();

    // 후보 확보: minGames, minGames+1, ... 순서로 4명 이상 확보될 때까지 추가
    std::vector<Player*> candidates;
    int level = 0;
    while (candidates.size() < 4 && level < 100) {  // level 제한으로 무한 루프 방지
        for (Player* p : allPlayers) {
            if (p->getGames() == minGames + level) {
                candidates.push_back(p);
            }
        }
        level++;
    }

    if (candidates.size() < 4) {
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 후보 부족 (총 " << candidates.size() << "명)\n";
        return;
    }

    // 후보를 state 기준으로 나누기
    std::vector<Player*> preferred;
    std::vector<Player*> fallback;

    for (Player* p : candidates) {
        if (p->getStates() != currentGameIndex) {
            preferred.push_back(p);
        } else {
            fallback.push_back(p);
        }
    }

    // 셔플
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
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 최종 매칭 실패\n";
        return;
    }

    // 매칭 성공 → 결과 출력 및 상태 갱신
    for (int i = 0; i < 4; ++i) {
        result[i]->incrementGames();
        result[i]->setStates(currentGameIndex);
        out << result[i]->getName();
        if (i == 3) out << "\n";
        else        out << " ";
    }
}

