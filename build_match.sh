pip3 install -r requirements.txt
g++ -std=c++17 main.cpp player.cpp MatchMaker.cpp PlayerLoader.cpp -o match
chmod +x match
