from ..database import *
import json
import datetime

def create_geolocation_statistics():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    
    current_time = datetime.datetime.now()
    hour_ago = current_time - datetime.timedelta(hours=1)
    
    sessions = db.session.query(TCPSession).filter(TCPSession.last_segm_tstmp > hour_ago).all()
    sessions_count = len(sessions)
    
    d = {}
    stats = []
    for s in sessions:
        d[s.remote_geolocation] = d.get(s.remote_geolocation, 0) + 1
    for key, value in d.items():
        stats.append({ "geolocation" : key, "perc" : value*100.0/sessions_count })
    obj = { "statistics" : stats }
    gs = GeolocationStatistics(current_time, json.dumps(obj))
    db.session.add(gs)
    db.session.commit()