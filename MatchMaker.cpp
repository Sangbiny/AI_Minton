#include "MatchMaker.h"
#include <iostream>
#include <algorithm>
#include <random>
#include <ctime>
#include <set>

MatchMaker::MatchMaker(std::vector<Player>& players) : players(players) {}

void MatchMaker::makeMatches(int totalGames) {
    std::set<std::string> lastGamePlayers;  // 연속 출전 방지용
    std::mt19937 rng(std::random_device{}());

    for (int gameIndex = 1; gameIndex <= totalGames; ++gameIndex) {
        // 1. 가장 적은 게임 수 찾기
        int minGames = INT_MAX;
        for (const auto& p : players) {
            if (p.games < minGames) {
                minGames = p.games;
            }
        }

        // 2. 최소 게임 수 가진 후보 추리기
        std::vector<Player*> candidates;
        for (auto& p : players) {
            if (p.games == minGames) {
                candidates.push_back(&p);
            }
        }

        // 3. 그 중에서 연속 출전이 아닌 사람 우선 추리기
        std::vector<Player*> nonConsecutive;
        for (auto* p : candidates) {
            if (lastGamePlayers.find(p->name) == lastGamePlayers.end()) {
                nonConsecutive.push_back(p);
            }
        }

        // 4. 부족하면 candidates에서 보충
        std::vector<Player*> pool = nonConsecutive;
        for (auto* p : candidates) {
            if (std::find(pool.begin(), pool.end(), p) == pool.end()) {
                pool.push_back(p);
                if (pool.size() == 4) break;
            }
        }

        // 5. 그래도 부족하면 다음 게임 수 가진 사람들에서 보충
        int g = minGames + 1;
        while (pool.size() < 4) {
            for (auto& p : players) {
                if (p.games == g &&
                    lastGamePlayers.find(p.name) == lastGamePlayers.end() &&
                    std::find(pool.begin(), pool.end(), &p) == pool.end()) {
                    pool.push_back(&p);
                    if (pool.size() == 4) break;
                }
            }
            ++g;
        }

        // 6. 랜덤 셔플해서 4명 선택
        std::shuffle(pool.begin(), pool.end(), rng);
        std::vector<Player*> selected(pool.begin(), pool.begin() + 4);

        // 7. 출력 및 게임 수 반영
        std::cout << "제 " << gameIndex << " 경기: ";
        for (auto* p : selected) {
            std::cout << p->name << " ";
            p->games++;
        }
        std::cout << std::endl;

        // 8. 마지막 출전자 기록
        lastGamePlayers.clear();
        for (auto* p : selected) {
            lastGamePlayers.insert(p->name);
        }
    }
}

