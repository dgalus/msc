#include "postgresqlcache.h"

PostgreSQLCache::PostgreSQLCache()
{
    db = new PostgresqlDatabase();
    c = new Counters();
    unsafeDomains = db->getUnsafeDomains();
    unsafeIPs = db->getUnsafeIPs();
    unsafeURLs = db->getUnsafeURLs();
    arpTable = db->getARPTable();
    activeTCPSessionsMutex.lock();
    activeTCPSessions = db->getActiveTCPSessions();
    activeTCPSessionsMutex.unlock();

    std::thread l(&PostgreSQLCache::insertLoop, this);
    sleep(1);
    std::thread hl(&PostgreSQLCache::httpLoop, this);
    sleep(1);
    std::thread acl(&PostgreSQLCache::activeTCPSessionsLoop, this);
    l.detach();
    hl.detach();
    acl.detach();
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

void PostgreSQLCache::pushHTTP(std::string httpContent)
{
    httpContentsMutex.lock();
    httpContents.push_back(httpContent);
    httpContentsMutex.unlock();
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
    activeTCPSessionsMutex.lock();
    for(auto it = activeTCPSessions.begin(); it != activeTCPSessions.end(); it++)
    {
        if(it->first.ip_src == sessionData.ip_src && it->first.ip_dst == sessionData.ip_dst && it->first.src_port == sessionData.src_port && it->first.dst_port == sessionData.dst_port)
        {
            segment->direction = FROM_SRC_TO_DST;
            activeTCPSessionsMutex.unlock();
            return it->second;
        }
        if(it->first.ip_src == sessionData.ip_dst && it->first.ip_dst == sessionData.ip_src && it->first.src_port == sessionData.dst_port && it->first.dst_port == sessionData.src_port)
        {
            segment->direction = FROM_DST_TO_SRC;
            activeTCPSessionsMutex.unlock();
            return it->second;
        }
    }
    activeTCPSessionsMutex.unlock();
    TCPSession ts;
    ts.dst_port = sessionData.dst_port;
    ts.first_segm_tstmp = getCurrentDateTime();
    ts.ip_dst = sessionData.ip_dst;
    ts.ip_src = sessionData.ip_src;
    ts.is_active = true;
    ts.last_segm_tstmp = ts.first_segm_tstmp;
    ts.src_port = sessionData.src_port;
    ts.remote_geolocation = "UNKNOWN";
    unsigned int id = db->insertTCPSession(ts);
    activeTCPSessionsMutex.lock();
    activeTCPSessions.push_back(std::pair<TCPSessionMin, unsigned int>(sessionData, id));
    activeTCPSessionsMutex.unlock();
    segment->direction = FROM_SRC_TO_DST;
    if(std::find(segment->flags.begin(), segment->flags.end(), "RST") != segment->flags.end())
    {
        sessionsToCloseMutex.lock();
        sessionsToClose.push_back(id);
        sessionsToCloseMutex.unlock();
        activeTCPSessionsMutex.lock();
        for(int i = 0; i < activeTCPSessions.size(); i++)
            if(activeTCPSessions.at(i).second == id)
                activeTCPSessions.erase(activeTCPSessions.begin()+i);
        activeTCPSessionsMutex.unlock();
    }
    if(std::find(segment->flags.begin(), segment->flags.end(), "FIN") != segment->flags.end())
    {
        sessionsToCloseMutex.lock();
        sessionsToClose.push_back(id);
        sessionsToCloseMutex.unlock();
        activeTCPSessionsMutex.lock();
        for(int i = 0; i < activeTCPSessions.size(); i++)
            if(activeTCPSessions.at(i).second == id)
                activeTCPSessions.erase(activeTCPSessions.begin()+i);
        activeTCPSessionsMutex.unlock();
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
    std::vector<int> sessionIds;
    std::vector<std::pair<int, std::string>> newSessionTimestamps;
    for(auto it = my_tcpSegments.begin(); it != my_tcpSegments.end(); it++)
        sessionIds.push_back(it->first);
    std::sort(sessionIds.begin(), sessionIds.end());
    sessionIds.erase(std::unique(sessionIds.begin(), sessionIds.end()), sessionIds.end());
    for(auto it = sessionIds.begin(); it != sessionIds.end(); it++)
    {
        std::multiset<std::string> timestamps;
        for(auto iter = my_tcpSegments.begin(); iter != my_tcpSegments.end(); iter++)
        {
            if(iter->first == *it)
                timestamps.insert(iter->second.timestamp);
        }
        newSessionTimestamps.push_back(std::pair<int, std::string>(*it, *timestamps.rbegin()));
    }
    db->updateTCPSessionLastTimestamp(newSessionTimestamps);
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
    try{
        while(true)
        {
            sleep(60);
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
        std::cerr << "insertLoop() thread " << std::this_thread::get_id() << " throwed an exception - " << e.what() << std::endl;
    }
    std::cerr << "insertLoop() thread " << std::this_thread::get_id() << " stopped!" << std::endl;
}

void PostgreSQLCache::httpLoop()
{
    try{
        while(true)
        {
            sleep(20);
            httpContentsMutex.lock();
            
            httpContentsMutex.unlock();
        }
    }
    catch(const std::exception& e)
    {
        std::cerr << "httpLoop() thread " << std::this_thread::get_id() << " throwed an exception - " << e.what() << std::endl;
    }
    std::cerr << "httpLoop() thread " << std::this_thread::get_id() << " stopped!" << std::endl;
}

void PostgreSQLCache::activeTCPSessionsLoop()
{
    try{
        while(true)
        {
            sleep(60);
            activeTCPSessionsMutex.lock();
            activeTCPSessions.clear();
            activeTCPSessions = db->getActiveTCPSessions();
            activeTCPSessionsMutex.unlock();
        }
    }
    catch(const std::exception& e)
    {
        std::cerr << "activeTCPSessionsLoop() thread " << std::this_thread::get_id() << " throwed an exception - " << e.what() << std::endl;
    }
    std::cerr << "activeTCPSessionsLoop() thread " << std::this_thread::get_id() << " stopped!" << std::endl;
}