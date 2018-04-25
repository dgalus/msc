import json
import ipaddress
from ..database import Database, TCPSession
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
        if hosts_in_the_same_netowrk(config["local_networks"], session.ip_src, session.ip_dst):
            session.remote_geolocation = "LOCAL"
        else:
            if is_local_address(session.ip_src):
                session.remote_geolocation = GeoLocation.get_country_by_address(session.ip_dst)
            else:
                session.remote_geolocation = GeoLocation.get_country_by_address(session.ip_src)
    db.session.commit()

def is_local_address(ip):
    return ipaddress.IPv4Address(ip).is_private

def hosts_in_the_same_netowrk(network_list, ip1, ip2):
    for network in network_list:
        if ipaddress.IPv4Address(ip1) in ipaddress.IPv4Network(network) and ipaddress.IPv4Address(ip2) in ipaddress.IPv4Network(network):
            return True
    return False
