from .malc0de import malc0de_get_unsafe_addresses
from .malwaredomainlist import malware_domain_list_get_unsafe_addresses, malware_domain_list_get_unsafe_domains
from .openphish import openphish_get_unsafe_urls
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
        db.create_table_if_not_exists(database=DATABASE, table_name=UNSAFE_URL_TABLE)
        db.create_table_if_not_exists(database=DATABASE, table_name=UNSAFE_IP_TABLE)
        db.create_table_if_not_exists(database=DATABASE, table_name=UNSAFE_DOMAIN_TABLE)
    except:
        pass

    for url in urls:
        urls_obj.append({ "url" : url })

    for address in addresses:
        addresses_obj.append({ "address" : address })

    for domain in domains:
        domain_obj.append({ "domain" : domain })

    if db.count_in_table(table_name=UNSAFE_URL_TABLE) == 0:
        db.insert(table=UNSAFE_URL_TABLE, document=urls_obj)
    if db.count_in_table(table_name=UNSAFE_DOMAIN_TABLE) == 0:
        db.insert(table=UNSAFE_DOMAIN_TABLE, document=domain_obj)
    if db.count_in_table(table_name=UNSAFE_IP_TABLE) == 0:
        db.insert(table=UNSAFE_IP_TABLE, document=addresses_obj)