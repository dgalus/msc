#ifndef IDATABASE_H
#define IDATABASE_H

#include <string>
#include "structures.h"

class IDatabase
{
public:
    virtual bool createTables() = 0;
    virtual bool clearDatabase() = 0;
    virtual bool createTableIfNotExists() = 0;
    virtual bool isDomainSafe(std::string& domain) = 0;
    virtual bool isURLSafe(std::string& url) = 0;
    virtual bool isIPSafe(std::string& ip) = 0;
    virtual std::string getMACByIP(std::string& ip) = 0;
    virtual double insertNewTCPSession(TCPSession& session) = 0;
    virtual double getLastTCPSessionId(std::string& ipSrc, int& srcPort, std::string& ipDst, int& dstPort) = 0;
    virtual double insertTCPSegment(int sessionId, TCPSegment& segment) = 0;
};

#endif
