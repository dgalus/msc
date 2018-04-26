import json
import datetime
from ..database import Database, Alert

def generate_alert(alert_type, desctiption, rank):
    alert = Alert(description=desctiption, 
                  alert_type=alert_type.value, 
                  rank=rank, 
                  notification_sent=False,
                  admin_delete=False,
                  timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    db.session.add(alert)
    db.session.commit()