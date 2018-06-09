from app.database import *
from app.scheduler import *
import json
import datetime
from sqlalchemy import and_

config = json.load(open("config.json"))
db = Database(config["database"]["user"], 
              config["database"]["password"], 
              config["database"]["host"], 
              config["database"]["port"], 
              config["database"]["db"])
ts = TCPSession("10.200.240.151", 63246, "10.200.240.1", 80, True, datetime.datetime.now(), datetime.datetime.now(), "LOCAL")
db.session.add(ts)
db.session.commit()

ts = db.session.query(TCPSession).filter(TCPSession.last_segm_tstmp > (datetime.datetime.now() - datetime.timedelta(hours=10))).first()

segm = TCPSegment("SYN", 46, ts.last_segm_tstmp, 1, ts.id)
db.session.add(segm)
db.session.commit()

rebuild_computer_behavior()