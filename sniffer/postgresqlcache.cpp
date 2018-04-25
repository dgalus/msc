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

    std::thread l(&PostgreSQLCache::insertLoop, this);
    l.detach();
}

PostgreSQLCache::~PostgreSQLCache()
{
    delete c;
    delete db;
}

void PostgreSQLCache::pushTCPSegment(TCPSessionMin session, TCPSegment segment)
{
    unsigned int id = getTCPSessionId(session, &segment);
    tcpSegmentsMutex.lock();
    tcpSegments.push_back(std::pair<unsigned int, TCPSegment>(id, segment));
    tcpSegmentsMutex.unlock();
}

void PostgreSQLCache::pushICMPSegment(ICMPSegment segment)
{
    icmpSegmentsMutex.lock();
    icmpSegments.push_back(segment);
    icmpSegmentsMutex.unlock();
}

void PostgreSQLCache::pushUDPSegment(UDPSegment segment)
{
    udpSegmentsMutex.lock();
    udpSegments.push_back(segment);
    udpSegmentsMutex.unlock();
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

unsigned int PostgreSQLCache::getTCPSessionId(TCPSessionMin sessionData, TCPSegment* segment)
{
    for(auto it = activeTCPSessions.begin(); it != activeTCPSessions.end(); it++)
    {
        if(it->first.ip_src == sessionData.ip_src && it->first.ip_dst == sessionData.ip_dst && it->first.src_port == sessionData.src_port && it->first.dst_port == sessionData.dst_port)
        {
            segment->direction = FROM_SRC_TO_DST;
            return it->second;
        }
        if(it->first.ip_src == sessionData.ip_dst && it->first.ip_dst == sessionData.ip_src && it->first.src_port == sessionData.dst_port && it->first.dst_port == sessionData.src_port)
        {
            segment->direction = FROM_DST_TO_SRC;
            return it->second;
        }
    }
    TCPSession ts;
    ts.dst_port = sessionData.dst_port;
    ts.first_segm_tstmp = getCurrentDateTime();
    ts.ip_dst = sessionData.ip_dst;
    ts.ip_src = sessionData.ip_src;
    ts.is_active = true;
    ts.last_segm_tstmp = ts.first_segm_tstmp;
    ts.src_port = sessionData.src_port;
    ts.remote_geolocation = "UNKNOWN";      // TODO
    unsigned int id = db->insertTCPSession(ts);
    activeTCPSessions.push_back(std::pair<TCPSessionMin, unsigned int>(sessionData, id));
    segment->direction = FROM_SRC_TO_DST;
    if(std::find(segment->flags.begin(), segment->flags.end(), "RST") != segment->flags.end())
    {
        sessionsToCloseMutex.lock();
        sessionsToClose.push_back(id);
        sessionsToCloseMutex.unlock();
    }
    if(std::find(segment->flags.begin(), segment->flags.end(), "FIN") != segment->flags.end())
    {
        sessionsToCloseMutex.lock();
        sessionsToClose.push_back(id);
        sessionsToCloseMutex.unlock();
    }
    return id;
}

void PostgreSQLCache::bulkInsertTCPSegments()
{
    tcpSegmentsMutex.lock();
    std::vector<std::pair<unsigned int, TCPSegment>> my_tcpSegments = tcpSegments;
    tcpSegments.clear();
    tcpSegmentsMutex.unlock();
    db->insertTCPSegments(my_tcpSegments);
}

void PostgreSQLCache::bulkInsertUDPSegments()
{
    udpSegmentsMutex.lock();
    std::vector<UDPSegment> my_udpSegments = udpSegments;
    udpSegments.clear();
    udpSegmentsMutex.unlock();
    db->insertUDPSegments(my_udpSegments);
}

void PostgreSQLCache::bulkInsertICMPSegments()
{
    icmpSegmentsMutex.lock();
    std::vector<ICMPSegment> my_icmpSegments = icmpSegments;
    icmpSegments.clear();
    icmpSegmentsMutex.unlock();
    db->insertICMPSegments(my_icmpSegments);
}

void PostgreSQLCache::bulkInserSessionsToClose()
{
    sessionsToCloseMutex.lock();
    std::vector<unsigned int> my_sessionsToClose = sessionsToClose;
    sessionsToClose.clear();
    sessionsToCloseMutex.unlock();
    db->closeTCPSessions(my_sessionsToClose);
}

void PostgreSQLCache::insertLoop()
{
    std::cerr << "Thread " << std::this_thread::get_id() << " started!" << std::endl;
    try{
        while(true)
        {
            sleep(10);
            bulkInsertICMPSegments();
            bulkInsertUDPSegments();
            bulkInsertTCPSegments();
            bulkInserSessionsToClose();
            counterMutex.lock();
            db->insertCounters(*c, getCurrentDateTime());
            c->zeroize();
            counterMutex.unlock();
        }
    }
    catch(const std::exception& e)
    {
        std::cerr << "Thread " << std::this_thread::get_id() << " throwed an exception - " << e.what() << std::endl;
    }
    std::cerr << "Thread " << std::this_thread::get_id() << " stopped!" << std::endl;
}
