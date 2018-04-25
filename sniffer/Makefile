all:
	g++ -c utils.cpp -std=c++14
	g++ -c postgresqldatabase.cpp -std=c++14 -lpq -lpqxx
	g++ -c postgresqlcache.cpp -std=c++14 -lpq -lpqxx
	g++ -Wall utils.o postgresqldatabase.o postgresqlcache.o main.cpp -o ../bin/sniffer -std=c++14 -lpq -lpqxx
