import json
import ipaddress
from ..database import Database, TCPSession
from ..utils import hosts_in_the_same_netowrk, is_local_address
from .geolocation import GeoLocation

def fix_unknown_geolocations():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"]) 
    tcp_sessions = db.session.query(TCPSession).filter_by(remote_geolocation='UNKNOWN').all()
    for session in tcp_sessions:
        if is_local_address(session.ip_src) and is_local_address(session.ip_dst):
            session.remote_geolocation = "LOCAL"
        else:
            if is_local_address(session.ip_src):
                session.remote_geolocation = GeoLocation.get_country_by_address(session.ip_dst)
            else:
                session.remote_geolocation = GeoLocation.get_country_by_address(session.ip_src)
    db.session.commit()