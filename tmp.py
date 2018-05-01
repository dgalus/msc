#t = threading.Thread(target=process_packet)
#t2 = threading.Thread(target=print_stats)
#t.start()
#t2.start()

#t.join()
#t2.join()


#print(DomainAnalysis.analyze('nereus1.radio.opole.pl'))

from app.database import Database, Computer
from sqlalchemy import func
import datetime
import json

config = json.load(open("config.json"))
db = Database(config["database"]["user"], 
              config["database"]["password"], 
              config["database"]["host"], 
              config["database"]["port"], 
              config["database"]["db"])

c = Computer('192.168.1.1')
db.session.add(c)
db.session.commit()