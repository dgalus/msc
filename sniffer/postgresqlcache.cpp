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

    // create thread to insert to db
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
    if(std::find(unsafeURLs.begin(), unsafeURLs.end(), url) != unsafeURLs.end())
       return false;
    else
       return true;
}

bool PostgreSQLCache::isIPSafe(std::string &ip)
{
    if(std::find(unsafeIPs.begin(), unsafeIPs.end(), ip) != unsafeIPs.end())
       return false;
    else
       return true;
}

unsigned int PostgreSQLCache::getTCPSessionId(TCPSessionMin sessionData)
{

}

void PostgreSQLCache::bulkInsertTCPSegments()
{
    // find session id
    //db->insertTCPSegments(tcpSegments);
}

void PostgreSQLCache::bulkInsertUDPSegments()
{
    db->insertUDPSegments(udpSegments);
    udpSegments.clear();
}

void PostgreSQLCache::bulkInsertICMPSegments()
{
    db->insertICMPSegments(icmpSegments);
    icmpSegments.clear();
}
