#include "postgresqldatabase.h"

PostgresqlDatabase::PostgresqlDatabase()
{
    try {
       conn = new pqxx::connection("dbname = sniffer user = sniffer password = sniffer hostaddr = 127.0.0.1 port = 5432");
       if (!conn->is_open()) {
          std::cout << "Can't open database" << std::endl;
          exit(2);
       }
    } catch (const std::exception &e) {
       std::cerr << e.what() << std::endl;
       exit(3);
    }
}

PostgresqlDatabase::~PostgresqlDatabase()
{
    conn->disconnect();
    delete conn;
}

std::vector<std::string> PostgresqlDatabase::getUnsafeDomains()
{

}

std::vector<std::string> PostgresqlDatabase::getUnsafeIPs()
{

}

std::vector<std::string> PostgresqlDatabase::getUnsafeURLs()
{

}

void PostgresqlDatabase::insertNewTCPSessions(std::vector<TCPSession> sessions)
{

}

void PostgresqlDatabase::insertTCPSegments(std::vector<std::pair<unsigned int, TCPSegment> > segments)
{

}

std::vector<std::pair<TCPSessionMin, unsigned int>> PostgresqlDatabase::getActiveTCPSessions()
{

}

void PostgresqlDatabase::closeTCPSessions(std::vector<unsigned int> sessiondIds)
{

}

bool PostgresqlDatabase::executeQuery(std::string query)
{

}


