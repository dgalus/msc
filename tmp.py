from app.database import *
from app.scheduler import *
from app.email_sender import send_alerts
import json
import datetime
from sqlalchemy import and_

#config = json.load(open("config.json"))
#db = Database(config["database"]["user"], 
              #config["database"]["password"], 
              #config["database"]["host"], 
              #config["database"]["port"], 
              #config["database"]["db"])

#ts = TCPSession("192.168.1.40", 59382, "192.168.1.17", 7788, True, datetime.datetime.now(), datetime.datetime.now(), "LOCAL")
#db.session.add(ts)
#db.session.commit()
 
#ts = db.session.query(TCPSession).filter(TCPSession.last_segm_tstmp > (datetime.datetime.now() - datetime.timedelta(hours=1))).first()

#segm = TCPSegment("SYN", 46, ts.last_segm_tstmp, 1, ts.id)
#db.session.add(segm)
#db.session.commit()

#add_computers_and_last_active()
#analyze_new_computers()
#rebuild_computer_behavior()
send_alerts()