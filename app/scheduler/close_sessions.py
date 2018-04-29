from ..database import Database, TCPSession
from sqlalchemy import and_
import datetime
import json

def close_sessions():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    current_time = datetime.datetime.now()
    day_ago = current_time - datetime.timedelta(days=1)
    sessions = db.session.query(TCPSession).filter(and_(TCPSession.last_segm_tstmp < day_ago, TCPSession.is_active == True)).all()
    for s in sessions:
        s.is_active = False
    db.session.commit()