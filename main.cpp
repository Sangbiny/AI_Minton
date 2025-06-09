#include <iostream>
#include <fstream>
#include <locale>
#include <vector>
#include "player.h"
#include "MatchMaker.h"
#include "PlayerLoader.h"

// main.cpp

int main()  {

    //std::vector<Player> players;

// -------------------------------------------------------------

// -------------------------------------------------------------
// 알고리즘 만든 뒤
// -------------------------------------------------------------
// vector for Player Object
   
    int totalGameCnt;

    std::vector<Player> players = loadPlayersFromFile("./input.txt", totalGameCnt);
    // Output File Dump
    std::ofstream fout("./result_of_match.txt");
    std::ofstream gout("./games_per_member.txt");
    //fout.imbue(std::locale("en_US.UTF-8"));


    //totalGameCnt = 20;

    std::cout << "total game Count = " << totalGameCnt << "\n";
    for(int j=0; j<totalGameCnt; ++j){
        matchPlayers(players, totalGameCnt, fout);
    }
    
    std::cout << "\n 멤버별 게임수\n";
    for (const Player& p : players) {
        gout << p.getName() << " " << p.getGames() << "\n";
    }
    
    
    fout.close();
    gout.close();

    return 0;
}
//EOF
