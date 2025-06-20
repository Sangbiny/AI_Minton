#include <iostream>
#include <fstream>
#include <locale>
#include <vector>
#include "player.h"
#include "MatchMaker.h"
#include "PlayerLoader.h"

// main.cpp

int main() {
    int totalGameCnt;
    std::vector<Player> players = loadPlayersFromFile("./input.txt", totalGameCnt);

    std::ofstream fout("./result_of_match.txt");
    std::ofstream gout("./games_per_member.txt");

    std::cout << "total game Count = " << totalGameCnt << "\n";

    // totalGameCnt만큼 반복, 경기 번호는 i
    for (int i = 0; i < totalGameCnt; ++i) {
        matchPlayers(players, i, fout);  // i는 현재 경기 번호
    }

    std::cout << "\n 멤버별 게임수\n";
    for (const Player& p : players) {
        gout << p.getName() << " " << p.getGames() << "\n";
    }

    fout.close();
    gout.close();

    return 0;
}

