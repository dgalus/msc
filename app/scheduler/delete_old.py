from ..database import *

def delete_old():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    
    timeout = int(config['persist_time_days'])
    current_time = datetime.datetime.now()
    timeout = current_time - datetime.timedelta(days=timeout)
    
    counters = db.session.query(Counter).filter(Counter.timestamp < timeout).all()
    for c in counters:
        db.session.delete(c)
    db.session.commit()
    
    tcp_segments = db.session.query(TCPSegment).filter(TCPSegment.timestamp < timeout).all()
    for t in tcp_segments:
        db.session.delete(t)
    db.session.commit()
    
    tcp_sessions = db.session.query(TCPSession).filter(TCPSession.last_segm_tstmp < timeout).all()
    for t in tcp_sessions:
        db.session.delete(t)
    db.session.commit()
    
    udp_segments = db.session.query(UDPSegment).filter(UDPSegment.timestamp < timeout).all()
    for u in udp_segments:
        db.session.delete(u)
    db.session.commit()
    
    icmp_segments = db.session.query(ICMPSegment).filter(ICMPSegment.timestamp < timeout).all()
    for i in icmp_segments:
        db.session.delete(i)
    db.session.commit()
    
    fake_counters = db.session.query(FakeCounter).filter(FakeCounter.timestamp < timeout).all()
    for fc in fake_counters:
        db.session.delete(fc)
    db.session.commit()
    
    