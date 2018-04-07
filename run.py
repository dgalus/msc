import rethinkdb as r
from app import *
from app.banlist import *

DATABASE = "test"
UNSAFE_URL_TABLE = "unsafe_url"
UNSAFE_IP_TABLE = "unsafe_ip"
UNSAFE_DOMAIN_TABLE = "unsafe_domain"

def initialize_unsafe_connections_list():
    addresses = []
    addresses_obj = []
    domains = []
    domain_obj = []
    urls = []
    urls_obj = []
    addresses += malc0de_get_unsafe_addresses()
    addresses += malware_domain_list_get_unsafe_addresses()
    domains += malware_domain_list_get_unsafe_domains()
    urls += openphish_get_unsafe_urls()
    r.connect("localhost", 28015).repl()
    try:
        r.db(DATABASE).table_create(UNSAFE_URL_TABLE).run()
        r.db(DATABASE).table_create(UNSAFE_IP_TABLE).run()
        r.db(DATABASE).table_create(UNSAFE_DOMAIN_TABLE).run()
    except:
        pass
    
    for url in urls:
        urls_obj.append({ "url" : url })
        
    for address in addresses:
        addresses_obj.append({ "address" : address })
        
    for domain in domains:
        domain_obj.append({ "domain" : domain })
    
    if r.table(UNSAFE_URL_TABLE).count().run() == 0:
        r.table(UNSAFE_URL_TABLE).insert(urls_obj).run()
    if r.table(UNSAFE_DOMAIN_TABLE).count().run() == 0:
        r.table(UNSAFE_DOMAIN_TABLE).insert(domain_obj).run()
    if r.table(UNSAFE_IP_TABLE).count().run() == 0:
        r.table(UNSAFE_IP_TABLE).insert(addresses_obj).run()

initialize_unsafe_connections_list()