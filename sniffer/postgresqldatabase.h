#ifndef POSTGRESQLDATABASE_H
#define POSTGRESQLDATABASE_H

#include <fstream>
#include <iostream>
#include <mutex>
#include <string>
#include <pqxx/pqxx>

#include "structures.h"
#include "counters.h"
#include "utils.h"

class PostgresqlDatabase
{
public:
    PostgresqlDatabase();
    ~PostgresqlDatabase();
    std::vector<std::string> getUnsafeDomains();
    std::vector<std::string> getUnsafeIPs();
    std::vector<std::string> getUnsafeURLs();
    std::vector<std::pair<std::string, std::string>> getARPTable();
    std::vector<std::pair<unsigned int, HTTPSite>> getHTTPSites();
    void insertNewTCPSessions(std::vector<TCPSession> sessions);
    void insertTCPSegments(std::vector<std::pair<unsigned int, TCPSegment>> segments);
    unsigned int insertTCPSession(TCPSession session);
    unsigned int insertHTTPSite(HTTPSite site);
    unsigned int insertARP(std::string mac, std::string ip);
    void insertArpSpoofingAlert(std::string ipAddr, std::string arpMac, std::string dbMac);
    void insertUDPSegments(std::vector<UDPSegment> segments);
    void insertICMPSegments(std::vector<ICMPSegment> segments);
    void insertCounters(Counters counters, std::string timestamp);
    void updateTCPSessionLastTimestamp(std::vector<std::pair<int, std::string>> newSessionTimestamps);
    void updateHTTPSites(std::vector<std::pair<unsigned int, HTTPSite>> &httpSites);
    std::vector<std::pair<TCPSessionMin, unsigned int>> getActiveTCPSessions();
    void closeTCPSessions(std::vector<unsigned int> sessionIds);
    bool executeQuery(std::string query);
private:
    pqxx::connection* conn;
    std::mutex dbMutex;
};

#endif // POSTGRESQLDATABASE_H
