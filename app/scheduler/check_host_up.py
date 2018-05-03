from ..database import *
from ..scan import ping, PingScanResponse
import json

def check_host_up():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    current_time = datetime.datetime.now()
    computers = db.session.query(Computer).all()
    for c in computers:
        if ping(c.ip) == PingScanResponse.HOST_AVAILABLE:
            c.last_ping_response_timestamp = current_time
    db.session.commit()