import socket
from ..geolocation import GeoLocation
from ..search_engines import DuckDuckGo, Google

class DomainAnalysis:
    @staticmethod
    def analyze(domain):
        d = dict()
        d['name'] = domain
        d['is_unsafe'] = 0
        d['country'] = GeoLocation.get_country_by_name(domain)
        d['ip'] = socket.gethostbyname(domain)
        d['google'] = Google.get_position(domain)
        d['duckduckgo'] = DuckDuckGo.get_position(domain)
        return d