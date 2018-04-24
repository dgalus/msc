all:
	g++ -c postgresqldatabase.cpp -std=c++14 -lpq -lpqxx
	g++ -c postgresqlcache.cpp -std=c++14 -lpq -lpqxx
	g++ -Wall postgresqldatabase.o postgresqlcache.o main.cpp -o ../bin/sniffer -std=c++14 -lpq -lpqxx
