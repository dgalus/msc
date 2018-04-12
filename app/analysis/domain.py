import socket
from ..geolocation import GeoLocation
from ..database import RethinkDB

def analyze(domain):
    name = domain
    country = GeoLocation.get_country_by_name(domain)
    ip = __get_ip_by_domain(domain)
    db = RethinkDB()
    
    
def __get_ip_by_domain(domain):
    return socket.gethostbyname(domain)