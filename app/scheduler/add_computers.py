from ..database import *
from ..utils import is_local_address
import json
import datetime

def add_computers_and_last_active():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    
    current_time = datetime.datetime.now()
    minute_ago = current_time - datetime.timedelta(minutes=1)
    
    sessions = db.session.query(TCPSession).filter(TCPSession.last_segm_tstmp < minute_ago).all()
    computers = db.session.query(Computer).all()
    
    ips_to_check = []
    for session in sessions:
        if is_local_address(session.ip_src):
            ips_to_check.append(session.ip_src)
        if is_local_address(session.ip_dst):
            ips_to_check.append(session.ip_dst)
    ips_to_check = set(ips_to_check)
    
    computers_set = set([i.ip for i in computers])
    computers_to_add = []
    for ip in ips_to_check:
        if ip not in computers_set:
            db.session.add(Computer(ip))
    db.session.commit()
    
    computers = db.session.query(Computer).order_by(Computer.id.asc()).all()
    for s in sessions:
        if is_local_address(s.ip_src):
            for c in computers:
                if c.ip == s.ip_src:
                    c.last_active = s.last_segm_tstmp
        if is_local_address(s.ip_dst):
            for c in computers:
                if c.ip == s.ip_dst:
                    c.last_active = s.last_segm_tstmp
    db.session.commit()