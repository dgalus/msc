#t = threading.Thread(target=process_packet)
#t2 = threading.Thread(target=print_stats)
#t.start()
#t2.start()

#t.join()
#t2.join()


#print(DomainAnalysis.analyze('nereus1.radio.opole.pl'))

from app.database import Database, TCPSession
from sqlalchemy import func
import datetime
import json

config = json.load(open("config.json"))
db = Database(config["database"]["user"], 
              config["database"]["password"], 
              config["database"]["host"], 
              config["database"]["port"], 
              config["database"]["db"])

current_time = datetime.datetime.now()
two_min_ago = current_time - datetime.timedelta(weeks=2)
scanner_ip = db.session.query(TCPSession.ip_src).filter(TCPSession.last_segm_tstmp > two_min_ago).group_by(TCPSession.ip_src).order_by(func.count(TCPSession.ip_src).desc()).first()[0]
print(scanner_ip)