from ..database import Database, TCPSession, UDPSegment, UnsafeIP
from ..alert import generate_alert, AlertType
from ..utils import is_local_address
import datetime
import json

def look_for_unsafe_ip():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    alert_ip = []
    addresses_to_check = []
    current_time = datetime.datetime.now()
    two_min_ago = current_time - datetime.timedelta(minutes=2)
    sessions = db.session.query(TCPSession).filter(TCPSession.last_segm_tstmp < two_min_ago).all()
    udp_segments = db.session.query(UDPSegment).filter(UDPSegment.timestamp < two_min_ago).all()
    for s in sessions:
        if not is_local_address(s.ip_src):
            addresses_to_check.append(s.ip_src)
        if not is_local_address(s.ip_dst):
            addresses_to_check.append(s.ip_dst)
    for u in udp_segments:
        if not is_local_address(u.ip_src):
            addresses_to_check.append(u.ip_src)
        if not is_local_address(u.ip_dst):
            addresses_to_check.append(u.ip_dst)
    unsafe_ip = db.session.query(UnsafeIP.ip).all()
    for addr in addresses_to_check:
        if addr in unsafe_ip:
            alert_ip.append(addr)
    s_alert_ip = list(set(alert_ip))
    for aip in s_alert_ip:
        generate_alert(AlertType.UNSAFE_IP_DETECTED, UnsafeIPDetectedAlert(aip), 30)