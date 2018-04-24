#ifndef POSTGRESQLDATABASE_H
#define POSTGRESQLDATABASE_H

#include <fstream>
#include <iostream>
#include <string>
#include <pqxx/pqxx>
#include "idatabase.h"

class PostgresqlDatabase : public IDatabase
{
public:
    PostgresqlDatabase();
    ~PostgresqlDatabase();
    std::vector<std::string> getUnsafeDomains();
    std::vector<std::string> getUnsafeIPs();
    std::vector<std::string> getUnsafeURLs();
    void insertNewTCPSessions(std::vector<TCPSession> sessions);
    void insertTCPSegments(std::vector<std::pair<unsigned int, TCPSegment>> segments);
    std::vector<std::pair<TCPSessionMin, unsigned int>> getActiveTCPSessions();
    void closeTCPSessions(std::vector<unsigned int> sessiondIds);
    bool executeQuery(std::string query);
private:
    pqxx::connection* conn;
};

#endif // POSTGRESQLDATABASE_H
