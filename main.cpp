// main.cpp
#include <iostream>
#include <fstream>
#include <locale>
#include <vector>
#include "player.h"
#include "MatchMaker.h"
#include "PlayerLoader.h"

int main() {
    int totalGameCnt;
    std::vector<Player> players = loadPlayersFromFile("./input.txt", totalGameCnt);

    std::ofstream fout("./result_of_match.txt");
    std::ofstream gout("./games_per_member.txt");

    std::cout << "total game Count = " << totalGameCnt << "\n";

    matchPlayers(players, totalGameCnt, fout);  // 반복문 내부로 이전됨

    std::cout << "\n 멤버별 게임수\n";
    for (const Player& p : players) {
        gout << p.getName() << " " << p.getGames() << "\n";
    }

    fout.close();
    gout.close();

    return 0;
}
