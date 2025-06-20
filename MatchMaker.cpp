#include "player.h"
#include "MatchMaker.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <random>
#include <unordered_set>

void matchPlayers(std::vector<Player>& players, int currentGameIndex, std::ostream& out) {
    std::vector<Player*> allPlayers;
    for (Player& p : players)
        allPlayers.push_back(&p);

    if (allPlayers.size() < 4) {
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 플레이어 수 부족\n";
        return;
    }

    // 1. 게임 수 오름차순 정렬
    std::sort(allPlayers.begin(), allPlayers.end(),
              [](Player* a, Player* b) {
                  return a->getGames() < b->getGames();
              });

    int minGames = allPlayers.front()->getGames();

    // 2. 후보군 수집: minGames 또는 minGames+1
    std::vector<Player*> candidates;
    for (Player* p : allPlayers) {
        if (p->getGames() == minGames || p->getGames() == minGames + 1)
            candidates.push_back(p);
    }

    // 3. candidates 중에서 firstGameCandidates(게임수 == 0) 추출
    std::vector<Player*> firstGameCandidates;
    std::vector<Player*> playedCandidates;

    for (Player* p : candidates) {
        if (p->getGames() == 0)
            firstGameCandidates.push_back(p);
        else
            playedCandidates.push_back(p);
    }

    // 셔플 준비
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(firstGameCandidates.begin(), firstGameCandidates.end(), g);
    std::shuffle(playedCandidates.begin(), playedCandidates.end(), g);

    std::vector<Player*> result;

    // 4. 첫 게임 후보로 먼저 채우기
    for (Player* p : firstGameCandidates) {
        if (result.size() < 4)
            result.push_back(p);
    }

    // 5. state 분산 고려해서 나머지 채우기
    std::unordered_set<int> existingStates;
    for (Player* p : result) {
        existingStates.insert(p->getStates());
    }

    // 가급적 state 겹치지 않게
    for (Player* p : playedCandidates) {
        if (result.size() >= 4) break;
        if (existingStates.find(p->getStates()) == existingStates.end()) {
            result.push_back(p);
            existingStates.insert(p->getStates());
        }
    }

    // state 겹쳐도 되는 fallback
    for (Player* p : playedCandidates) {
        if (result.size() >= 4) break;
        if (std::find(result.begin(), result.end(), p) == result.end())
            result.push_back(p);
    }

    if (result.size() < 4) {
        std::cout << "[ERROR] 경기 " << currentGameIndex << ": 최종 후보 부족 (" << result.size() << "명)\n";
        return;
    }

    // 6. 결과 반영
    for (int i = 0; i < 4; ++i) {
        result[i]->incrementGames();
        result[i]->setStates(currentGameIndex);
        out << result[i]->getName();
        if (i == 3) out << "\n";
        else        out << " ";
    }
}

