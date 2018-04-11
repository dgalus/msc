from ..geolocation import GeoLocation

def analyze(domain):
    name = domain
    country = GeoLocation.get_country_by_name(domain)