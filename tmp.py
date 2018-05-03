#t = threading.Thread(target=process_packet)
#t2 = threading.Thread(target=print_stats)
#t.start()
#t2.start()

#t.join()
#t2.join()


#print(DomainAnalysis.analyze('nereus1.radio.opole.pl'))

from app.scheduler import *

analyze_http_sites()