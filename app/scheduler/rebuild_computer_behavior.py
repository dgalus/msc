from ..database import *
from ..alert import generate_alert, AlertType, AbnormalActivityTimeAlert
from ..utils import is_local_address
import json
import datetime

weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

def rebuild_computer_behavior():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    
    current_time = datetime.datetime.now()
    minute_ago = current_time - datetime.timedelta(minutes=1)
    
    sessions = db.session.query(TCPSession).filter(TCPSession.last_segm_tstmp >= minute_ago).all()
    computers = db.session.query(Computer).all()
    
    for c in computers:
        sess = []
        for s in sessions:
            if s.ip_src == c.ip or s.ip_dst == c.ip:
                sess.append(s)
        if len(sess) > 0:
            # activity time
            aut = json.loads(c.active_use_times)
            minute = current_time.hour*60+current_time.minute
            weekday = datetime.datetime.today().weekday()
            aut[weekdays[weekday]][minute] += 1
            c.active_use_times = json.dumps(aut)
            arr = []
            for l in weekdays:
                arr.extend(aut[l])
            m = max(arr)
            if (aut[weekdays[weekday]][minute]/m) < config['system']['active_use_times_threshold']:
                generate_alert(AlertType.ABNORMAL_ACTIVITY_TIME, AbnormalActivityTimeAlert(c.ip, current_time), config["system"]["ranks"]["abnormal_activity_time"])
            
            # geolocations
            computer_geolocations = json.loads(c.geolocations)["geolocations"]
            geolocations = []
            for s in sess:
                geolocations.append(s.remote_geolocation)
            for g in geolocations:
                if g not in computer_geolocations:
                    computer_geolocations.append(g)
                if g not in config["system"]["safe_geolocations"]:
                    generate_alert(AlertType.NEW_GEOLOCATION_DETECTED, NewGeolocationDetectedAlert(c.ip, g), config["system"]["ranks"]["new_geolocation_detected"])
                    ansgt = AddNewSafeGeolocationTask(g)
                    apt = AdminPendingTask(str(ansgt))
                    db.session.add(apt)
            d = {}
            d["geolocations"] = computer_geolocations
            c.geolocations = json.dumps(d)
                    
            # ports
            computer_ports = json.loads(c.most_connected_ports)["ports"]
            for s in sess:
                if s.ip_src == c.ip:
                    ip_src = c.ip
                    ip_dst = s.ip_dst
                    port = s.dst_port
                else:
                    ip_src = s.ip_dst
                    ip_dst = s.ip_src
                    port = s.src_port
                if port not in computer_ports:
                    computer_ports.append(port)
                if port not in config["system"]["safe_ports"]:
                    generate_alert(AlertType.NEW_DESTINATION_PORT_DETECTED, NewDestinationPortDetectedAlert(ip_src, ip_dst, port), config["system"]["ranks"]["new_destination_port_detected"])
                    anspt = AddNewSafePortTask(port)
                    apt = AdminPendingTask(str(anspt))
                    db.session.add(apt)
            d = {}
            d["ports"] = computer_ports
            c.most_connected_ports = json.dumps(d)
    db.session.commit()    