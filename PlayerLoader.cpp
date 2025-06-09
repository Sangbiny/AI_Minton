#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include "player.h"



int convertLevel(char levelChar) {
    switch (levelChar) {
        case 'A': return LEVEL_A;
        case 'B': return LEVEL_B;
        case 'C': return LEVEL_C;
        case 'D': return LEVEL_D;
        case 'E': return LEVEL_E;
        default: return 0;
    }
}

std::vector<Player> loadPlayersFromFile(const std::string& filename, int& totalGameCnt) {
    std::vector<Player> players;
    std::ifstream infile(filename);

    if (!infile) {
        std::cerr << "파일을 열 수 없습니다: " << filename << std::endl;
        return players;
    }

    if(!(infile >> totalGameCnt)) {
        std::cerr << "게임 수를 읽는 데 실패했습니다." << std::endl;
        return players;
    }

    std::string name;
    char gender, levelChar;

    while (infile >> name >> gender >> levelChar) {
        int level = convertLevel(levelChar);
        players.emplace_back(name, gender, level, 0, WAITING);
    }

    infile.close();
    return players;
}

