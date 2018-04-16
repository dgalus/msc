import rethinkdb as r
from .. import config

class RethinkDB:
    def __init__(self):
        self.conn = r.connect("localhost", 28015).repl()
    
    def create_all_tables(self):
        for _c in config['DB_TABLES']:
            if _c != 'database':
                self.create_table_if_not_exists(config['DB_TABLES']['database'], config['DB_TABLES'][_c])
    
    def clear_db(self):
        r.db_drop(config['DB_TABLES']['database']).run(conn)
        r.db_create(config['DB_TABLES']['database']).run(conn)
        self.create_all_tables()
    
    def create_table_if_not_exists(self, database, table_name):
        try:
            r.db(database).table_create(table_name).run(self.conn)
        except:
            pass
    
    def insert(self, table, document):
        r.table(table).insert(document).run(self.conn)
    
    def count_in_table(self, table_name):
        return r.table(table_name).count().run(self.conn)
    
    def is_domain_unsafe(self, domain):
        return True if r.table(config['DB_TABLES']['unsafe_domain_table']).filter({ 'domain' : domain }).count().run(self.conn) > 0 else False
    
    def is_url_unsafe(self, url):
        return True if r.table(config['DB_TABLES']['unsafe_url_table']).filter({ 'url' : url }).count().run(self.conn) > 0 else False
    
    def is_ip_unsafe(self, ip):
        return True if r.table(config['DB_TABLES']['unsafe_ip_table']).filter({ 'ip' : ip }).count().run(self.conn) > 0 else False
    
    def get_mac_by_ip(self, ip):
        pass
    
    def get_analyzed_domain_info(self, domain):
        return r.table(config['DB_TABLES']['analyzed_domain_table']).filter({ 'domain' : domain }).run(self.conn)