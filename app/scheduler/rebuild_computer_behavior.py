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
            
            # geolocations (+admin pending request)
            
            
            # ports (+ admin pending request)
            
    db.session.commit()    