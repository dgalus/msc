#include "postgresqldatabase.h"

PostgresqlDatabase::PostgresqlDatabase()
{

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


