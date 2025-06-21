#include "MatchMaker.h"
#include <algorithm>
#include <random>
#include <set>
#include <map>
#include <ctime>

MatchMaker::MatchMaker(std::vector<Player>& players, int totalGames)
    : players(players), totalGames(totalGames) {
    std::srand(std::time(nullptr));
}

void MatchMaker::run() {
    std::set<std::string> lastGamePlayers;

    for (int gameIndex = 1; gameIndex <= totalGames; ++gameIndex) {
        std::vector<Player*> eligible;

        // 최소 게임수 계산
        int minGames = INT_MAX;
        for (auto& p : players) {
            if (p.games < minGames) minGames = p.games;
        }

        // 게임수 가장 적은 사람들만 후보로
        for (auto& p : players) {
            if (p.games == minGames) {
                eligible.push_back(&p);
            }
        }

        // 연속 출전 방지
        std::vector<Player*> pool;
        for (auto* p : eligible) {
            if (lastGamePlayers.find(p->name) == lastGamePlayers.end()) {
                pool.push_back(p);
            }
        }

        // 후보가 4명 안 되면, eligible 중에서도 추가
        if (pool.size() < 4) {
            for (auto* p : eligible) {
                if (std::find(pool.begin(), pool.end(), p) == pool.end()) {
                    pool.push_back(p);
                    if (pool.size() == 4) break;
                }
            }
        }

        // 그래도 부족하면 다음 게임수 사람 중 추가
        int gamesToCheck = minGames + 1;
        while (pool.size() < 4) {
            for (auto& p : players) {
                if (p.games == gamesToCheck && 
                    lastGamePlayers.find(p.name) == lastGamePlayers.end() &&
                    std::find(pool.begin(), pool.end(), &p) == pool.end()) {
                    pool.push_back(&p);
                    if (pool.size() == 4) break;
                }
            }
            gamesToCheck++;
        }

        // 랜덤 셔플
        std::random_shuffle(pool.begin(), pool.end());

        // 최종 4명 선택
        std::vector<Player*> selected(pool.begin(), pool.begin() + 4);

        // 게임 결과 출력
        std::cout << "제 " << gameIndex << " 경기: ";
        for (auto* p : selected) {
            std::cout << p->name << " ";
            p->games += 1;
        }
        std::cout << std::endl;

        // 마지막 출전자 저장
        lastGamePlayers.clear();
        for (auto* p : selected) {
            lastGamePlayers.insert(p->name);
        }
    }
}

