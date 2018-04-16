import socket
from ..geolocation import GeoLocation
from ..search_engines import DuckDuckGo, Google
from ..database import RethinkDB

class DomainAnalysis:
    @staticmethod
    def analyze(domain):
        d = dict()
        d['name'] = domain
        db = RethinkDB()
        d['is_unsafe'] = db.is_domain_unsafe(domain)
        d['country'] = GeoLocation.get_country_by_name(domain)
        d['ip'] = socket.gethostbyname(domain)
        d['google'] = Google.get_position(domain)
        d['duckduckgo'] = DuckDuckGo.get_position(domain)
        return d