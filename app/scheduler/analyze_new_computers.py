from ..database import *
from ..scan import *
import json
import datetime

def analyze_new_computers():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    
    computers = db.session.query(Computer).filter(Computer.most_connected_ports == None).all()
    for c in computers:
        c.open_ports = tcp_connect_scan(c.ip)
        c.closed_ports = tcp_fin_scan(c.ip)
        c.last_port_scan = datetime.datetime.now()
        most_connected_ports = {}
        for i in range(1, 65536):
            most_connected_ports[str(i)] = 0
        c.most_connected_ports = str(most_connected_ports)
    db.session.commit()