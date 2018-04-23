from operator import itemgetter
import rethinkdb as r
from .. import config
from ..sniffer import TCPSegment, TCPSession

class RethinkDB:
    def __init__(self):
        self.conn = r.connect("localhost", 28015).repl()
    
    # GENERAL
    def create_all_tables(self):
        for _c in config['DB_TABLES']:
            if _c != 'database':
                self.create_table_if_not_exists(config['DB_TABLES']['database'], config['DB_TABLES'][_c])
    
    def clear_db(self):
        r.db_drop(config['DB_TABLES']['database']).run(self.conn)
        r.db_create(config['DB_TABLES']['database']).run(self.conn)
        self.create_all_tables()
    
    def create_table_if_not_exists(self, database, table_name):
        try:
            r.db(database).table_create(table_name).run(self.conn)
        except:
            pass
    
    def insert(self, table, document):
        return r.table(table).insert(document).run(self.conn)
    
    def count_in_table(self, table_name):
        return r.table(table_name).count().run(self.conn)
    
    # UNSAFE
    def is_domain_unsafe(self, domain):
        return True if r.table(config['DB_TABLES']['unsafe_domain_table']).filter({ 'domain' : domain }).count().run(self.conn) > 0 else False
    
    def is_url_unsafe(self, url):
        return True if r.table(config['DB_TABLES']['unsafe_url_table']).filter({ 'url' : url }).count().run(self.conn) > 0 else False
    
    def is_ip_unsafe(self, ip):
        return True if r.table(config['DB_TABLES']['unsafe_ip_table']).filter({ 'ip' : ip }).count().run(self.conn) > 0 else False
    
    # ARP
    def get_mac_by_ip(self, ip):
        pass
    
    # ANALYZED
    def get_analyzed_domain_info(self, domain):
        return r.table(config['DB_TABLES']['analyzed_domain_table']).filter({ 'domain' : domain }).run(self.conn)
    
    # SESSIONS
    def insert_new_tcp_session(self, tcp_session):
        if isinstance(tcp_session, TCPSession):
            return r.table(config['DB_TABLES']['tcp_session_table']).insert(tcp_session.__dict__).run(self.conn)
        return None
    
    def get_last_tcp_session(self, ip_src, src_port, ip_dst, dst_port):
        res = r.table(config['DB_TABLES']['tcp_session_table']).filter(
            lambda session: (session['ip_src'] == ip_src) & (session['src_port'] == src_port) & (session['ip_dst'] == ip_dst)
            & (session['dst_port'] == dst_port) & (session['last_segm_tstmp'])).run(self.conn)
        sorted_res = sorted(res, key=itemgetter('last_segm_tstmp'))
        if len(sorted_res) > 0:
            return sorted_res[-1]
        else:
            return None

    
    def count_active_tcp_sessions(self):
        return r.table(config['DB_TABLES']['tcp_session_table']).filter(r.row['is_active'] == True).count().run(self.conn)
    
    def insert_tcp_segment(self, ip_src, src_port, ip_dst, dst_port, tcp_segment):
        
        # update last_segm_tstmp 
        pass
    
    def get_all_active_tcp_sessions(self):
        pass
    
    def get_active_tcp_sessions_by_host(self, ip):
        pass
    
    def get_host_tcp_sessions_by_timestamp(self, from_timestamp, to_timestamp):
        pass
    
    def get_all_tcp_sessions_by_timestamp(self, from_timestamp, to_timestamp):
        pass