#ifndef IDATABASE_H
#define IDATABASE_H

#include <string>
#include <unordered_map>
#include "structures.h"

class IDatabase
{
public:
    virtual std::vector<std::string> getUnsafeDomains() = 0;
    virtual std::vector<std::string> getUnsafeIPs() = 0;
    virtual std::vector<std::string> getUnsafeURLs() = 0;
    virtual std::vector<std::pair<std::string, std::string>> getARPTable() = 0;
    virtual void insertNewTCPSessions(std::vector<TCPSession> sessions) = 0;
    virtual void insertTCPSegments(std::vector<std::pair<unsigned int, TCPSegment>> segments) = 0;
    virtual std::vector<std::pair<TCPSessionMin, unsigned int>> getActiveTCPSessions() = 0;
    virtual void closeTCPSessions(std::vector<unsigned int> sessionIds) = 0;
    virtual bool executeQuery(std::string query) = 0;
};

#endif
