from .malc0de import malc0de_get_unsafe_addresses
from .malwaredomainlist import malware_domain_list_get_unsafe_addresses, malware_domain_list_get_unsafe_domains
from .openphish import openphish_get_unsafe_urls

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

    