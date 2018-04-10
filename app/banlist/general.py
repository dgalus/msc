from .malc0de import malc0de_get_unsafe_addresses
from .malwaredomainlist import malware_domain_list_get_unsafe_addresses, malware_domain_list_get_unsafe_domains
from .openphish import openphish_get_unsafe_urls
from .. import config
from ..database import *

def initialize_unsafe_connections_list():
    db = RethinkDB()
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
    try:
        db.create_table_if_not_exists(database=config['DB_TABLES']['database'], table_name=config['DB_TABLES']['unsafe_url_table'])
        db.create_table_if_not_exists(database=config['DB_TABLES']['database'], table_name=config['DB_TABLES']['unsafe_ip_table'])
        db.create_table_if_not_exists(database=config['DB_TABLES']['database'], table_name=config['DB_TABLES']['unsafe_domain_table'])
    except:
        pass

    for url in urls:
        urls_obj.append({ "url" : url })

    for address in addresses:
        addresses_obj.append({ "address" : address })

    for domain in domains:
        domain_obj.append({ "domain" : domain })

    if db.count_in_table(table_name=config['DB_TABLES']['unsafe_url_table']) == 0:
        db.insert(table=config['DB_TABLES']['unsafe_url_table'], document=urls_obj)
    if db.count_in_table(table_name=config['DB_TABLES']['unsafe_domain_table']) == 0:
        db.insert(table=config['DB_TABLES']['unsafe_domain_table'], document=domain_obj)
    if db.count_in_table(table_name=config['DB_TABLES']['unsafe_ip_table']) == 0:
        db.insert(table=config['DB_TABLES']['unsafe_ip_table'], document=addresses_obj)