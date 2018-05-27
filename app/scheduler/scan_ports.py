from ..database import *
from ..scan import *
from ..alert import generate_alert, AlertType, NewOpenPortOnHostDetected
import ast
import json
import datetime
from sqlalchemy import and_

def scan_ports():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    
    current_time = datetime.datetime.now()
    minute_ago = current_time - datetime.timedelta(minutes=1)
    week_ago = current_time - datetime.timedelta(days=7)
    
    computers = db.session.query(Computer).filter(and_(Computer.last_port_scan < week_ago, Computer.last_ping_response_timestamp > minute_ago)).all()
    for c in computers:
        old_open_ports = list(ast.literal_eval(c.open_ports))
        new_open_ports = tcp_connect_scan(c.ip)
        new_closed_ports = tcp_fin_scan(c.ip)
        old_closed_ports = c.closed_ports
        for port in new_open_ports:
            if port in old_open_ports:
                new_open_ports.remove(port)
        if len(new_open_ports) > 0:
            for port in new_open_ports:
                nop = NewOpenPortOnHostDetected(c.ip, port)
                generate_alert(AlertType.NEW_OPEN_PORT_ON_HOST_DETECTED, str(nop), config["system"]["ranks"]["new_open_port_on_host_detected"])
        c.open_ports = list(set(new_open_ports + old_open_ports))
        c.closed_ports = new_closed_ports
        c.last_port_scan = datetime.datetime.now()
    db.session.commit()    