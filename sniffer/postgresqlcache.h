#ifndef POSTGRESQLCACHE_H
#define POSTGRESQLCACHE_H

#include <unistd.h>

#include <algorithm>
#include <mutex>
#include <set>
#include <string>
#include <thread>
#include <vector>

#include "structures.h"
#include "postgresqldatabase.h"
#include "utils.h"

class PostgreSQLCache
{
public:
    PostgreSQLCache();
    ~PostgreSQLCache();
    void pushTCPSegment(TCPSessionMin session, TCPSegment segment);
    void pushICMPSegment(ICMPSegment segment);
    void pushUDPSegment(UDPSegment segment);
    void pushHTTP(HTTPSite site);
    void pushARP(std::string mac, std::string ip);
    void pushArpSpoofingAlert(std::string ipAddr, std::string arpMac, std::string dbMac);
    bool isDomainSafe(std::string& domain);
    bool isURLSafe(std::string& url);
    bool isIPSafe(std::string& ip);
    Counters* c;
    std::mutex counterMutex;
    std::vector<std::pair<std::string, std::string>> arpTable;

private:
    unsigned int getTCPSessionId(TCPSessionMin sessionData, TCPSegment* segment);
    void bulkInsertTCPSegments();
    void bulkInsertUDPSegments();
    void bulkInsertICMPSegments();
    void bulkInserSessionsToClose();

    void httpLoop();
    void insertLoop();
    void activeTCPSessionsLoop();
    std::mutex tcpSegmentsMutex;
    std::mutex icmpSegmentsMutex;
    std::mutex udpSegmentsMutex;
    std::mutex httpMutex;
    std::mutex arpMutex;
    std::mutex sessionsToCloseMutex;
    std::mutex activeTCPSessionsMutex;

    PostgresqlDatabase* db;
    std::vector<std::pair<unsigned int, TCPSegment>> tcpSegments;
    std::vector<ICMPSegment> icmpSegments;
    std::vector<UDPSegment> udpSegments;
    std::vector<std::pair<unsigned int, HTTPSite>> httpSites;
    std::vector<std::string> unsafeURLs;
    std::vector<std::string> unsafeDomains;
    std::vector<std::string> unsafeIPs;
    std::vector<std::pair<TCPSessionMin, unsigned int>> activeTCPSessions;
    std::vector<unsigned int> sessionsToClose;
};

#endif // POSTGRESQLCACHE_H
