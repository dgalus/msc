from app import *
from app.banlist import *

def initialize_unsafe_connections_list():
    addresses = []
    domains = []
    urls = []
    addresses += malc0de_get_unsafe_addresses()
    addresses += malware_domain_list_get_unsafe_addresses()
    domains += malware_domain_list_get_unsafe_domains()
    urls += openphish_get_unsafe_urls()
    print(domains)

initialize_unsafe_connections_list()