// main.cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <locale>
#include "player.h"
#include "MatchMaker.h"
#include "PlayerLoader.h"

int main() {
    int totalGameCnt;
    std::vector<Player> players = loadPlayersFromFile("./input.txt", totalGameCnt);

    std::ofstream fout("./result_of_match.txt");
    std::ofstream gout("./games_per_member.txt");

    std::cout << "total game Count = " << totalGameCnt << "\n";

    matchPlayers(players, totalGameCnt, fout);

    std::cout << "\n멤버별 게임 수\n";
    for (const Player& p : players) {
        gout << p.getName() << " " << p.getGames() << "\n";
    }

    fout.close();
    gout.close();

    return 0;
}

