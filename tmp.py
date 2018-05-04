#t = threading.Thread(target=process_packet)
#t2 = threading.Thread(target=print_stats)
#t.start()
#t2.start()

#t.join()
#t2.join()


#print(DomainAnalysis.analyze('nereus1.radio.opole.pl'))

from app.scheduler import *
from app.database import *

config = json.load(open("config.json"))
db = Database(config["database"]["user"], 
              config["database"]["password"], 
              config["database"]["host"], 
              config["database"]["port"], 
              config["database"]["db"])

c = Counter(
    tcp_syn = 1,
    tcp_ack = 2,
    tcp_synack = 3,
    tcp_psh = 4,
    tcp_rst = 5,
    tcp_fin = 6,
    tcp = 7,
    ip = 8,
    arp = 9,
    udp = 10,
    icmp = 11,
    l2_traffic = 12,
    l3_traffic = 13,
    l4_traffic = 14,
    l2_frames = 15,
    l3_frames = 16,
    l4_frames = 17
)
db.session.add(c)
db.session.commit()

generate_l2_traffic_forecast()