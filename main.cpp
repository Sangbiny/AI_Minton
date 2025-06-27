// main.cpp
#include <iostream>
#include <fstream>
#include <locale>
#include <vector>
#include <map>
#include <set>
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

    std::cout << "\n 멤버별 게임수\n";
    for (const Player& p : players) {
        gout << p.getName() << " " << p.getGames() << "\n";
    }

    fout.close();
    gout.close();

    return 0;
}
