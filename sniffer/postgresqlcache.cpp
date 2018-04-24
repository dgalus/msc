#include "postgresqlcache.h"

PostgreSQLCache::PostgreSQLCache()
{
    db = new PostgresqlDatabase();
    c = new Counters();
    unsafeDomains = db->getUnsafeDomains();
    unsafeIPs = db->getUnsafeIPs();
    unsafeURLs = db->getUnsafeURLs();
    arpTable = db->getARPTable();
    activeTCPSessions = db->getActiveTCPSessions();
}

PostgreSQLCache::~PostgreSQLCache()
{
    delete c;
    delete db;
}

void PostgreSQLCache::pushTCPSegment(TCPSessionMin session, TCPSegment segment)
{

}

void PostgreSQLCache::pushICMPSegment(ICMPSegment segment)
{
    icmpSegments.push_back(segment);
}

void PostgreSQLCache::pushUDPSegment(UDPSegment segment)
{
    udpSegments.push_back(segment);
}

bool PostgreSQLCache::isDomainSafe(std::string &domain)
{
    if(std::find(unsafeDomains.begin(), unsafeDomains.end(), domain) != unsafeDomains.end())
       return false;
    else
       return true;
}

bool PostgreSQLCache::isURLSafe(std::string &url)
{
    if(std::find(unsafeURLs.begin(), unsafeURLs.end(), domain) != unsafeURLs.end())
       return false;
    else
       return true;
}

bool PostgreSQLCache::isIPSafe(std::string &ip)
{
    if(std::find(unsafeIPs.begin(), unsafeIPs.end(), domain) != unsafeIPs.end())
       return false;
    else
       return true;
}

double PostgreSQLCache::getTCPSessionId(TCPSessionMin sessionData)
{

}

void PostgreSQLCache::bulkInsertTCPSegments()
{

}

void PostgreSQLCache::bulkInsertUDPSegments()
{

}

void PostgreSQLCache::bulkInsertICMPSegments()
{

}
