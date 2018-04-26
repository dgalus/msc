#t = threading.Thread(target=process_packet)
#t2 = threading.Thread(target=print_stats)
#t.start()
#t2.start()

#t.join()
#t2.join()


#print(DomainAnalysis.analyze('nereus1.radio.opole.pl'))





from app.database import Database, TCPSession

db = Database("sniffer", "sniffer", "127.0.0.1", 5432, "sniffer")
#ts = TCPSession("10.100.100.100", 1234, "10.200.200.200", 2345, True, "2018-04-02 12:23:43", "2018-04-02 12:23:43", "LOCAL")
#db.session.add(ts)
#db.session.commit()
#db.clear_db()