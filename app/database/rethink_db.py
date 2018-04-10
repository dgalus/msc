import rethinkdb as r
from .. import config

class RethinkDB:
    def __init__(self):
        r.connect("localhost", 28015).repl()
        
    def create_table_if_not_exists(self, database, table_name):
        try:
            r.db(database).table_create(table_name).run()
        except:
            pass
    
    def insert(self, table, document):
        r.table(table).insert(document).run()
    
    def count_in_table(self, table_name):
        return r.table(table_name).count().run()
    
    def is_domain_unsafe(self, domain):
        pass
    
    def is_url_unsafe(self, url):
        pass
    
    def is_ip_unsafe(self, ip):
        pass
    
    def get_mac_by_ip(self, ip):
        pass