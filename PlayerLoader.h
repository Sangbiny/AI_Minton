#ifndef PLAYER_LOADER_H
#define PLAYER_LOADER_H

#include <vector>
#include <string>
#include "player.h"

std::vector<Player> loadPlayersFromFile(const std::string& filename, int& totalGameCnt);

#endif

