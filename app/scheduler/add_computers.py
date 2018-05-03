from ..database import *
from ..utils import is_local_address
import json
import datetime

def add_computers():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    current_time = datetime.datetime.now()
    minute_ago = current_time - datetime.timedelta(minutes=1)
    ips = db.session.query(TCPSession.ip_src, TCPSession.ip_dst).filter(TCPSession.last_segm_tstmp > minute_ago).all()
    computers = db.session.query(Computer.ip).all()
    ips_to_check = []
    for ip in ips:
        if is_local_address(ip[0]):
            ips_to_check.append(ip[0])
        if is_local_address(ip[1]):
            ips_to_check.append(ip[1])
    ips_to_check = set(ips_to_check)
    computers_set = set([i[0] for i in computers])
    computers_to_add = []
    for ip in ips_to_check:
        if ip not in computers_set:
            db.session.add(Computer(ip))
    db.session.commit()