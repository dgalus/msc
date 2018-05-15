from ..database import *
from ..utils import is_local_address
import json
import datetime
from sqlalchemy import and_

def execute_admin_tasks():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    apt = db.session.query(AdminPendingTask).filter(AdminPendingTask.is_finished==False).all()
    for a in apt:
        if a.decision == True:
            t = json.loads(a.task)
            if t["task"] == "add_new_safe_geolocation":
                config["system"]["safe_geolocations"].append(t["geolocation"])
            elif t["task"] == "add_new_safe_port":
                config["system"]["safe_ports"].append(t["port"])
            with open('config.json', 'w') as outfile:
                json.dump(config, outfile)
            a.is_finished = True
            a.finished_timestamp = datetime.datetime.now()
        elif a.decision == False:
            a.is_finished = True
            a.finished_timestamp = datetime.datetime.now()
    db.session.commit()
    