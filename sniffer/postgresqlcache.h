#ifndef POSTGRESQLCACHE_H
#define POSTGRESQLCACHE_H

#include <string>
#include <thread>
#include <vector>

#include "structures.h"
#include "postgresqldatabase.h"

class PostgreSQLCache
{
public:
    PostgreSQLCache();
    void pushTCPSegment(TCPSessionMin session, TCPSegment segment);
    void pushICMPSegment(ICMPSegment segment);
    void pushUDPSegment(UDPSegment segment);
    bool isDomainSafe(std::string& domain);
    bool isURLSafe(std::string& url);
    bool isIPSafe(std::string& ip);
private:
    double getTCPSessionId(TCPSessionMin sessionData);
    void bulkInsertTCPSegments();
    void bulkInsertUDPSegments();
    void bulkInsertICMPSegments();

    PostgresqlDatabase db;
    std::vector<TCPSegment> tcpSegments;
    std::vector<ICMPSegment> icmpSegments;
    std::vector<UDPSegment> udpSegments;
    std::vector<std::string> unsafeURLs;
    std::vector<std::string> unsafeDomains;
    std::vector<std::string> unsafeIPs;
    std::vector<std::pair<TCPSessionMin, unsigned int>> tcpSessions;
    std::vector<int> sessionsToClose;
};

#endif // POSTGRESQLCACHE_H
