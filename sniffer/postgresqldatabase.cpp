#include "postgresqldatabase.h"

PostgresqlDatabase::PostgresqlDatabase()
{
    try {
       conn = new pqxx::connection("dbname = sniffer user = sniffer password = sniffer hostaddr = 127.0.0.1 port = 5432");
       if (!conn->is_open()) {
          std::cout << "Can't open database" << std::endl;
          exit(2);
       }
    } catch (const std::exception &e) {
       std::cerr << e.what() << std::endl;
       exit(3);
    }
}

PostgresqlDatabase::~PostgresqlDatabase()
{
    conn->disconnect();
    delete conn;
}

std::vector<std::pair<unsigned int, HTTPSite>> PostgresqlDatabase::getHTTPSites()
{
    std::vector<std::pair<unsigned int, HTTPSite>> httpSites;
    std::string sql = "select * from analyzed_http_site;";
    dbMutex.lock();
    pqxx::nontransaction N(*conn);
    pqxx::result R(N.exec(sql.c_str()));
    dbMutex.unlock();
    for(pqxx::result::const_iterator c = R.begin(); c != R.end(); c++)
    {
        unsigned int id = c[0].as<unsigned int>();
        HTTPSite hs;
        hs.domain = c[1].as<std::string>();
        hs.url = c[2].as<std::string>();
        hs.ip = c[3].as<std::string>();
        httpSites.push_back(std::pair<unsigned int, HTTPSite>(id, hs));
    }
    return httpSites;
}

std::vector<std::string> PostgresqlDatabase::getUnsafeDomains()
{
    std::vector<std::string> domains;
    std::string sql = "select domain from unsafe_domain;";
    dbMutex.lock();
    pqxx::nontransaction N(*conn);
    pqxx::result R(N.exec(sql.c_str()));
    dbMutex.unlock();
    for(pqxx::result::const_iterator c = R.begin(); c != R.end(); c++)
    {
        domains.push_back(c[0].as<std::string>());
    }
    return domains;
}

std::vector<std::string> PostgresqlDatabase::getUnsafeIPs()
{
    std::vector<std::string> ips;
    std::string sql = "select ip from unsafe_ip;";
    dbMutex.lock();
    pqxx::nontransaction N(*conn);
    pqxx::result R(N.exec(sql.c_str()));
    dbMutex.unlock();

    for(pqxx::result::const_iterator c = R.begin(); c != R.end(); c++)
    {
        ips.push_back(c[0].as<std::string>());
    }
    return ips;
}

std::vector<std::string> PostgresqlDatabase::getUnsafeURLs()
{
    std::vector<std::string> urls;
    std::string sql = "select url from unsafe_url;";
    dbMutex.lock();
    pqxx::nontransaction N(*conn);
    pqxx::result R(N.exec(sql.c_str()));
    dbMutex.unlock();

    for(pqxx::result::const_iterator c = R.begin(); c != R.end(); c++)
    {
        urls.push_back(c[0].as<std::string>());
    }
    return urls;
}

std::vector<std::pair<std::string, std::string>> PostgresqlDatabase::getARPTable()
{
    std::vector<std::pair<std::string, std::string>> arpTable;
    std::string query = "select * from arp;";
    dbMutex.lock();
    pqxx::nontransaction N(*conn);
    pqxx::result R(N.exec(query.c_str()));
    dbMutex.unlock();
    for(pqxx::result::const_iterator c = R.begin(); c != R.end(); c++)
        arpTable.push_back(std::pair<std::string, std::string>(c[1].as<std::string>(), c[2].as<std::string>()));
    return arpTable;
}

void PostgresqlDatabase::insertNewTCPSessions(std::vector<TCPSession> sessions)
{
    if(sessions.size() > 0)
    {
        std::string query = "insert into tcp_session (ip_src, src_port, ip_dst, dst_port, is_active, first_segm_tstmp, last_segm_tstmp, remote_geolocation) values ";
        for(unsigned int i = 0; i < sessions.size(); i++)
        {
            query += "('" + sessions[i].ip_src + "', " + std::to_string(sessions[i].src_port) + ", '"
                    + sessions[i].ip_dst + "', " + std::to_string(sessions[i].dst_port)
                    + ", " + ((sessions[i].is_active) ? "TRUE" : "FALSE") + ", '" + sessions[i].first_segm_tstmp + "', '"
                    + sessions[i].last_segm_tstmp + "' , '" + sessions[i].remote_geolocation + "')";
            if(i < sessions.size()-1)
                query += ", ";
            else
                query += "; ";
        }
        executeQuery(query);
    }
}

void PostgresqlDatabase::insertTCPSegments(std::vector<std::pair<unsigned int, TCPSegment>> segments)
{
    if(segments.size() > 0)
    {
        std::string query = "insert into tcp_segment (flags, size, timestamp, direction, session_id) values ";
        for(unsigned int i = 0; i < segments.size(); i++)
        {
            std::string flags = "";
            for(auto it = segments[i].second.flags.begin(); it != segments[i].second.flags.end(); it++)
                flags += *it + " ";
            query += "('" + flags + "', " + std::to_string(segments[i].second.size) + ", '"
                    + segments[i].second.timestamp + "', " + std::to_string(segments[i].second.direction) + ", "
                    + std::to_string(segments[i].first) + ")";
            if(i < segments.size()-1)
                query += ", ";
            else
                query += "; ";
        }
        executeQuery(query);
    }
}

unsigned int PostgresqlDatabase::insertTCPSession(TCPSession session)
{
    std::string query = "insert into tcp_session (id, ip_src, src_port, ip_dst, dst_port, is_active, first_segm_tstmp, last_segm_tstmp, remote_geolocation) values (DEFAULT, "
                        "'" + session.ip_src + "', " + std::to_string(session.src_port) + ", '" + session.ip_dst + "', " + std::to_string(session.dst_port) + ", "
                        + ((session.is_active) ? "TRUE" : "FALSE") + ", '" + session.first_segm_tstmp + "', '" + session.last_segm_tstmp + "', '" + session.remote_geolocation + "') returning id";
    try{
        dbMutex.lock();
        pqxx::work W(*conn);
        pqxx::result R(W.exec(query.c_str()));
        W.commit(); 
        dbMutex.unlock();
        for(pqxx::result::const_iterator c = R.begin(); c != R.end(); c++)
        {
            return c[0].as<unsigned int>();
        }
    }
    catch(const std::exception &e)
    {
        dbMutex.unlock();
        std::cerr << e.what() << std::endl;
        return 0;
    }
    return 0;
}

unsigned int PostgresqlDatabase::insertHTTPSite(HTTPSite site)
{
    std::string query = "insert into analyzed_http_site (id, domain, urls, ip, last_visited) values (DEFAULT, "
                        "'" + site.domain+ "', '" + site.url + "', '" + site.ip + "', '" + getCurrentDateTime() + "') returning id";
    try{
        dbMutex.lock();
        pqxx::work W(*conn);
        pqxx::result R(W.exec(query.c_str()));
        W.commit();
        dbMutex.unlock();
        for(pqxx::result::const_iterator c = R.begin(); c != R.end(); c++)
        {
            return c[0].as<unsigned int>();
        }
    }
    catch(const std::exception &e)
    {
        dbMutex.unlock();
        std::cerr << e.what() << std::endl;
        return 0;
    }
    return 0;
}

unsigned int PostgresqlDatabase::insertARP(std::string mac, std::string ip)
{
    std::string query = "insert into arp (id, ip, mac) values (DEFAULT, '" + ip + "', '" + mac + "');";
    try{
        dbMutex.lock();
        pqxx::work W(*conn);
        pqxx::result R(W.exec(query.c_str()));
        W.commit();
        dbMutex.unlock();
        for(pqxx::result::const_iterator c = R.begin(); c != R.end(); c++)
        {
            return c[0].as<unsigned int>();
        }
    }
    catch(const std::exception &e)
    {
        dbMutex.unlock();
        std::cerr << e.what() << std::endl;
        return 0;
    }
    return 0;
}

void PostgresqlDatabase::insertArpSpoofingAlert(std::string ipAddr, std::string arpMac, std::string dbMac)
{
    std::string description = ipAddr + " is known under " + dbMac + " but " + arpMac + " found in reply. Check for ARP spoofing.";
    int alertType = 1;
    int rank = 50;
    std::string timestamp = getCurrentDateTime();
    
    std::string query = "insert into alert (id, description, alert_type, rank, notification_sent, admin_delete, timestamp) values "
                        "(DEFAULT, '" + description + "', " + std::to_string(alertType) + ", " + std::to_string(rank) + ", FALSE, FALSE, "
                        "'" + timestamp + "');";
    executeQuery(query);
}

void PostgresqlDatabase::insertUDPSegments(std::vector<UDPSegment> segments)
{
    if(segments.size() > 0)
    {
        std::string query = "insert into udp_segment (ip_src, src_port, ip_dst, dst_port, size, timestamp) values ";
        for(unsigned int i = 0; i < segments.size(); i++)
        {
            query += "('" + segments[i].ip_src + "', " + std::to_string(segments[i].src_port) + ", '" + segments[i].ip_dst + "', "
                    "" + std::to_string(segments[i].dst_port) + ", " + std::to_string(segments[i].size) + ", '" + segments[i].timestamp + "')";
            if(i < segments.size()-1)
                query += ", ";
            else
                query += "; ";
        }
        executeQuery(query);
    }
}

void PostgresqlDatabase::insertICMPSegments(std::vector<ICMPSegment> segments)
{
    if(segments.size() > 0)
    {
        std::string query = "insert into icmp_segment (ip_src, ip_dst, icmp_type, timestamp) values ";
        for(unsigned int i = 0; i < segments.size(); i++)
        {
            query += "('" + segments[i].ip_src + "', '" + segments[i].ip_dst + "', " + std::to_string(segments[i].type) + ", '" + segments[i].timestamp + "')";
            if(i < segments.size()-1)
                query += ", ";
            else
                query += "; ";
        }
        executeQuery(query);
    }
}

void PostgresqlDatabase::insertCounters(Counters counters, std::string timestamp)
{
    std::string query = "insert into counters (timestamp, tcp_syn, tcp_ack, tcp_synack, tcp_psh, tcp_rst, tcp_fin, tcp, "
                        "ip, arp, udp, icmp, l2_traffic, l3_traffic, l4_traffic, l2_frames, l3_frames, l4_frames) values ("
                        "'" + timestamp + "', " + std::to_string(counters.tcp_syn) + ", " + std::to_string(counters.tcp_ack) + ", "
                        "" + std::to_string(counters.tcp_synack) + ", " + std::to_string(counters.tcp_psh) + ", " + std::to_string(counters.tcp_rst) + ", "
                        "" + std::to_string(counters.tcp_fin) + ", " + std::to_string(counters.tcp) + ", " + std::to_string(counters.ip) + ", "
                        "" + std::to_string(counters.arp) + ", " + std::to_string(counters.udp) + ", " + std::to_string(counters.icmp) + ", "
                        "" + std::to_string(counters.l2_traffic) + ", " + std::to_string(counters.l3_traffic) + ", " + std::to_string(counters.l4_traffic) + ", "
                        "" + std::to_string(counters.l2_frames) + ", " + std::to_string(counters.l3_frames) + ", " + std::to_string(counters.l4_frames) + ");";
    executeQuery(query);
}

void PostgresqlDatabase::updateTCPSessionLastTimestamp(std::vector<std::pair<int, std::string>> newSessionTimestamps)
{
    if(newSessionTimestamps.size() > 0){
        std::string query = "update tcp_session set last_segm_tstmp = case ";
        for(auto it = newSessionTimestamps.begin(); it != newSessionTimestamps.end(); it++)
            query += "when id = " + std::to_string(it->first) + " then to_timestamp('" + it->second + "', 'YYYY-MM-DD hh24:mi:ss')::timestamp without time zone ";
        query += "end where id in (";
        for(unsigned int i = 0; i < newSessionTimestamps.size(); i++)
        {
            query += std::to_string(newSessionTimestamps[i].first);
            if(i < newSessionTimestamps.size()-1)
                query += ", ";
            else
                query += "); ";
        }
        executeQuery(query);
    }
}

void PostgresqlDatabase::updateHTTPSites(std::vector<std::pair<unsigned int, HTTPSite>> &httpSites)
{
    std::vector<unsigned int> ids;
    for(auto it = httpSites.begin(); it != httpSites.end(); it++)
    {
        if(it->second.update)
        {
            ids.push_back(it->first);
        }
    }
    if(ids.size() > 0)
    {
        std::string query = "update analyzed_http_site set urls = case ";
        for(auto it = httpSites.begin(); it != httpSites.end(); it++)
        {
            if(it->second.update)
            {
                query += "when id = " + std::to_string(it->first) + " then '" + it->second.url + "'";
            }
        }
        query += " end, last_visited = to_timestamp('" + getCurrentDateTime() + "', 'YYYY-MM-DD hh24:mi:ss')::timestamp without time zone ";
        query += "where id in (";
        for(unsigned int i = 0; i < ids.size(); i++)
        {
            query += std::to_string(ids[i]);
            if(i < ids.size()-1)
                query += ", ";
            else
                query += "); ";
        }
        executeQuery(query);
        for(auto it = httpSites.begin(); it != httpSites.end(); it++)
            it->second.update = false;
    }
}

std::vector<std::pair<TCPSessionMin, unsigned int>> PostgresqlDatabase::getActiveTCPSessions()
{
    std::vector<std::pair<TCPSessionMin, unsigned int>> ret;
    std::string sql = "select id, ip_src, src_port, ip_dst, dst_port from tcp_session where is_active = true;";
    dbMutex.lock();
    pqxx::nontransaction N(*conn);
    pqxx::result R(N.exec(sql.c_str()));
    dbMutex.unlock();

    for(pqxx::result::const_iterator c = R.begin(); c != R.end(); c++)
    {
        TCPSessionMin tsm;
        unsigned int id = c[0].as<unsigned int>();
        tsm.ip_src = c[1].as<std::string>();
        tsm.src_port = c[2].as<int>();
        tsm.ip_dst = c[3].as<std::string>();
        tsm.dst_port = c[4].as<int>();
        ret.push_back(std::pair<TCPSessionMin, unsigned int>(tsm, id));
    }
    return ret;
}

void PostgresqlDatabase::closeTCPSessions(std::vector<unsigned int> sessionIds)
{
    if(sessionIds.size() > 0){
        std::string query = "update tcp_session set is_active = false where id in (";
        for(unsigned int i = 0; i < sessionIds.size(); i++)
        {
            query += std::to_string(sessionIds[i]);
            if(i <sessionIds.size() - 1)
                query += ", ";
            else
                query += ");";
        }
        executeQuery(query);
    }
}

bool PostgresqlDatabase::executeQuery(std::string query)
{
    try{
        dbMutex.lock();
        pqxx::work W(*conn);
        W.exec(query.c_str());
        W.commit();
        dbMutex.unlock();
        return true;
    }
    catch(const std::exception &e)
    {
        dbMutex.unlock();
        std::cerr << e.what() << std::endl;
        return false;
    }
}


