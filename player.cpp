#include "player.h"
#include <iostream>

// player.cpp

Player::Player(std::string n, char g, int l, int gs, int st)
    : name(n), gender(g), level(l), games(gs), states(st) {}

    std::string Player::getName()   const   { return name   ;   }    
    char        Player::getGender() const   { return gender ;   }
    int         Player::getLevel()  const   { return level  ;   }
    int         Player::getGames()  const   { return games  ;   }
    int         Player::getStates() const   { return states ;   }

    void        Player::setName(std::string n)  { name      =n  ;   }
    void        Player::setGender(char g)       { gender    =g  ;   }
    void        Player::setLevel(int l)         { level     =l  ;   }
    void        Player::setGames(int gs)        { games     =gs ;   }
    void        Player::setStates(int st)       { states    =st ;   }

    void        Player::incrementGames()        { games++       ;   }

    //void        Player::printInfo() const {
    //    std::cout   <<  "Name:      "   << name
    //                <<  ", Gender:  "   << gender
    //                <<  ", Level:   "   << level
    //                <<  ", Games:   "   << games
    //                <<  ", States:  "   << states   << std::endl;
    //}        
    void        Player::printInfo() const {
        std::cout   <<  "Name:      "   << name
                    <<  ", Gender:  "   << gender
                    <<  ", Level:   "   << level
                    <<  ", Games:   "   << games
                    <<  ", States:  "   << states   << std::endl;
    }
