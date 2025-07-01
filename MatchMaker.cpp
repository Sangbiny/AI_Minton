#include "player.h"
#include "MatchMaker.h"
#include <vector>
#include <algorithm> // sort
#include <iostream>
#include <fstream>
#include <cstdlib>  // rand, srand
#include <ctime>    // time
#include <random>

void matchPlayers(std::vector<Player>& players, int totalGame, std::ostream& out) {
    //int playersPerGame = 4; // Double play : 2 vs 2
    //int courtCount = 1;
    int gameCnt = 0;  


    int matchableCount = 0;


    for (const Player& p : players) {
        //if (p.getStates() == WAITING) matchableCount++;
        if (p.getName() != "") matchableCount++;
    }
        //std::cout << matchableCount << "\n";
        //std::cout << playersPerGame << "\n";

    //if (matchableCount < playersPerGame * totalMatches) {
    //    std::cout << "매칭 가능한 인원 부족\n"; // temp
    //    return;
    //}

    // WAITING 상태인 사람들만 따로 뽑기
    std::vector<Player*> waitingPlayers;
    for (Player& p : players) {
        if (p.getStates() == WAITING) {
            waitingPlayers.push_back(&p); // 포인터로 저장
        }
    }

    // 게임 수 기준으로 정렬(오름차순) : 흠.. 나중엔 바꿔야지. 랜덤으로.
    std::sort(waitingPlayers.begin(), waitingPlayers.end(),
            [](Player* a, Player* b) {
                return a->getGames() < b->getGames();
            });

    // 가장 적은 게임 수를 가진 사람들 중 4명랜덤 선택
    int minGames = waitingPlayers.front()->getGames();

    std::vector<Player*> candidates;
    for (Player* p : waitingPlayers) {
        if (p->getGames() == minGames) {
            candidates.push_back(p);
        } else {
            break; // 이미 정렬되어 있어서 그 이상은 안봐도 됨
        }
    }
    
    // 최소게임수인 사람이 4명이 안될 경우 그다음 게임수가 적은 사람 추가
    std::vector<Player*> candidates_1;
    std::vector<Player*> candidates_2;
    if (candidates.size() < 4) { 
        for (Player* p : waitingPlayers) {
            if (p->getGames() == minGames + 1) {
                candidates_1.push_back(p);
            } else if(p->getGames() == minGames + 2) {
                candidates_2.push_back(p);
            }
        }
    }
    
    // Random Shuffle
    std::vector<Player*> result;
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(candidates.begin(), candidates.end(), g);
    std::shuffle(candidates_1.begin(), candidates_1.end(), g);
    std::shuffle(candidates_2.begin(), candidates_2.end(), g); 

    for (Player* p : candidates) {
        if (result.size() < 4) result.push_back(p);
        else break;
    }
    for (Player* p : candidates_1) {
        if (result.size() < 4) result.push_back(p);
        else break;
    }
    for (Player* p : candidates_2) {
        if (result.size() < 4) result.push_back(p);
        else break;
    }

    if (result.size() < 4) {
        std::cout << "ERROR\n" << std::endl;
        return;
    }


    for (int i = 0; i < 4; ++i) {
        result[i]->incrementGames();
        out << result[i]->getName();
        //if (i !=3) out << ", "; //마지막 사람 뒤에는 쉼표 뻄
        //else       out << "\n";
        if (i == 3) out << "\n";
        else        out << " ";
        ++gameCnt;
        //std::cout << result[i]->getName();
        //if (i !=3) std::cout << ", "; //마지막 사람 뒤에는 쉼표 뻄
        //else       std::cout << "\n";
    }


    std::cout << std::endl;
}
