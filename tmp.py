from app.database import *
from sqlalchemy import func, and_
from statistics import *
import statistics
import datetime
import json
import math

config = json.load(open("config.json"))
db = Database(config["database"]["user"], 
              config["database"]["password"], 
              config["database"]["host"], 
              config["database"]["port"], 
              config["database"]["db"])

two_min_ago = datetime.datetime.now() - datetime.timedelta(minutes=20)

ip_pair = db.session.query(TCPSession.ip_dst, TCPSession.ip_src).filter(TCPSession.last_segm_tstmp > two_min_ago).group_by(TCPSession.ip_dst, TCPSession.ip_src).order_by(func.count(TCPSession.ip_dst).desc()).first()
print(ip_pair)
dst_ports = db.session.query(TCPSession.dst_port).filter(and_(TCPSession.last_segm_tstmp > two_min_ago, TCPSession.ip_dst == ip_pair[0])).all()
print(len(dst_ports))
tcp_syn_count = db.session.query(Counter.tcp_syn).order_by(Counter.id.desc()).first()[0]
print(tcp_syn_count)
if len(dst_ports) > tcp_syn_count*0.5:
    print("TCP SYN SCAN")
else:
    print("SYN FLOOD SCAN")

