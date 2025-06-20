#ifndef PLAYER_H
#define PLAYER_H

// player.h

#include <string>

// Level Define
#define LEVEL_A 5
#define LEVEL_B 4
#define LEVEL_C 3
#define LEVEL_D 2
#define LEVEL_E 1

class Player {
private:
    std::string name;
    char    gender;
    int     level;
    int     games;
    int     states;  // 경기 번호를 나타냄

public:
    // 생성자
    Player(std::string n, char g, int l, int gs, int st);

    // Getter
    std::string getName()   const;
    char        getGender() const;
    int         getLevel()  const;
    int         getGames()  const;
    int         getStates() const;

    // Setter
    void        setName(std::string n);
    void        setGender(char g);
    void        setLevel(int l);
    void        setGames(int gs);
    void        setStates(int st);

    // Games Number Cnt
    void        incrementGames();

    // Print for Debug
    void        printInfo() const;
};

#endif

