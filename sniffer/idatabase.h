#ifndef IDATABASE_H
#define IDATABASE_H

#include <string>
#include <unordered_map>
#include "structures.h"

class IDatabase
{
public:
    virtual bool isDomainSafe(std::string& domain) = 0;
    virtual bool isURLSafe(std::string& url) = 0;
    virtual bool isIPSafe(std::string& ip) = 0;
    virtual std::string getMACByIP(std::string& ip) = 0;
    virtual double insertNewTCPSession(TCPSession& session) = 0;
    virtual double getLastTCPSessionId(std::string& ipSrc, int& srcPort, std::string& ipDst, int& dstPort) = 0;
    virtual double insertTCPSegment(int sessionId, TCPSegment& segment) = 0;
    virtual std::unordered_map<TCPSessionMin, int> getActiveTCPSessions() = 0;
};

#endif
