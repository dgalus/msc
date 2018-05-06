from ..database import *
from ..anomaly_detection import holt_winters_forecast
import datetime
import json

def generate_l2_traffic_forecast():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    
    last_timestamp = db.session.query(L2TrafficForecast.timestamp).order_by(L2TrafficForecast.id.desc()).first()
    l2_counters = db.session.query(Counter.l2_traffic).all()
    l2_counters = [l[0] for l in l2_counters]
    if last_timestamp is None:
        last_timestamp = datetime.datetime.now()
    if len(l2_counters) >= 2882:
        hwf = holt_winters_forecast(l2_counters, 1440, 0.999, 0, 0.01, 1440)
        for h in hwf:
            new_timestamp = last_timestamp + datetime.timedelta(minutes=1)
            last_timestamp = new_timestamp
            db.session.add(L2TrafficForecast(new_timestamp, h))
        db.session.commit()