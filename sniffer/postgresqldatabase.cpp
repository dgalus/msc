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

std::vector<std::string> PostgresqlDatabase::getUnsafeDomains()
{

}

std::vector<std::string> PostgresqlDatabase::getUnsafeIPs()
{

}

std::vector<std::string> PostgresqlDatabase::getUnsafeURLs()
{

}

void PostgresqlDatabase::insertNewTCPSessions(std::vector<TCPSession> sessions)
{

}

void PostgresqlDatabase::insertTCPSegments(std::vector<std::pair<unsigned int, TCPSegment> > segments)
{

}

std::vector<std::pair<TCPSessionMin, unsigned int>> PostgresqlDatabase::getActiveTCPSessions()
{
    std::vector<std::pair<TCPSessionMin, unsigned int>> ret;
    std::string sql = "select id, ip_src, src_port, ip_dst, dst_port from tcp_session where is_active = true;";
    pqxx::nontransaction N(*conn);
    pqxx::result R(N.exec(sql.c_str()));

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

void PostgresqlDatabase::closeTCPSessions(std::vector<unsigned int> sessiondIds)
{

}

bool PostgresqlDatabase::executeQuery(std::string query)
{
    try{
        pqxx::work W(*conn);
        W.exec(query.c_str());
        W.commit();
        return true;
    }
    catch(const std::exception &e)
    {
        std::cerr << e.what() << std::endl;
        return false;
    }
}


