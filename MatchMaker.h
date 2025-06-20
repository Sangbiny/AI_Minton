// MatchMaker.h
#ifndef MATCH_MAKER_H
#define MATCH_MAKER_H

#include <vector>
#include "player.h"

// currentGameIndex를 추가로 받음
void matchPlayers(std::vector<Player>& players, int currentGameIndex, std::ostream& out);

#endif

