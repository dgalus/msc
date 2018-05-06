from .malc0de import malc0de_get_unsafe_addresses
from .malwaredomainlist import malware_domain_list_get_unsafe_addresses, malware_domain_list_get_unsafe_domains
from .openphish import openphish_get_unsafe_urls
import sys
import os
import json
from ..database import Database, UnsafeDomain, UnsafeIP, UnsafeURL

def initialize_unsafe_connections_list():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])    
    addresses = []
    domains = []
    urls = []
    addresses += malc0de_get_unsafe_addresses()
    addresses += malware_domain_list_get_unsafe_addresses()
    domains += malware_domain_list_get_unsafe_domains()
    urls += openphish_get_unsafe_urls()
    for addr in addresses:
        db.session.add(UnsafeIP(addr))
    for url in urls:
        db.session.add(UnsafeURL(url))
    for domain in domains:
        db.session.add(UnsafeDomain(domain))
    db.session.commit()