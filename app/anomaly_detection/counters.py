from ..database import *
from ..alert import  generate_alert, AlertType, HighTrafficAmountAlert, TcpSynScanAlert, SynFloodAlert
import statistics

def is_outlier(traffic, test_value):
    traffic_without_duplicates = list(set(traffic))
    stddev = stdev(traffic_without_duplicates)
    avg = mean(traffic_without_duplicates)
    if test_value > (4*stddev)+avg:
        return True
    return False

def analyze_counters():
    last_counters = db.session.query(Counter).order_by(Counter.id.desc()).limit(1000)
    last_fake_counters = db.session.query(FakeCounter).order_by(FakeCounter.id.desc()).limit(1000)
    lfc_syn = []
    lfc_rst = []
    lc_l2traffic = []
    for l in last_fake_counters:
        lfc_syn.append(l.tcp_syn)
        lfc_rst.append(l.tcp_rst)
    for lc in last_counters:
        lc_l2traffic.append(lc.l2_traffic)
    if len(last_counters) > 0:
        if len(last_counters) > 100:
            # high traffic amount
            if is_outlier(lc_l2traffic[:-1], lc_l2traffic[-1]):
                ht = HighTrafficAmountAlert()
                if mean(lc_l2traffic[:-1])*3 < lc_l2traffic[-1]:
                    rank = 60
                else:
                    rank = 20
                generate_alert(AlertType.HIGH_TRAFFIC_AMOUNT, str(ht), rank)
            # higher tcp_syn (fake_counters)
            if is_outlier(lfc_syn, last_counters[-1].tcp_syn):
                new_tcp_syn = last_fake_counters[-1].tcp_syn_avg
                avg_syn = last_fake_counters[-1].tcp_syn_avg
                #generate alert (decide if syn-flood or syn scan)
            else:
                new_tcp_syn = last_counters[-1].tcp_syn
                lfc_syn.append(last_counters[-1].tcp_syn)
                avg_syn = mean(lfc_syn)
            # higher tcp_rst (fake_counters)
            pass
        
            fc = FakeCounter(new_tcp_syn, avg_syn, new_tcp_rst, avg_rst, last_counters[-1].udp)
            db.session.add(fc)
            db.session.commit(fc)
            #generate_alert
        else:
            new_tcp_syn = last_counters[-1].tcp_syn
            new_tcp_rst = last_counters[-1].tcp_rst
            s_syn = 0
            s_rst = 0
            for i in range(0, len(lfc_syn)):
                s_syn += lfc_syn[i]
                s_rst += lfc_rst[i]
            s_syn += new_tcp_syn
            s_rst += new_tcp_rst
            avg_syn = s_syn/(len(lfc_syn) + 1)
            avg_rst = s_rst/(len(lfc_rst) + 1)
            fc = FakeCounter(new_tcp_syn, avg_syn, new_tcp_rst, avg_rst, last_counters[-1].udp)
            db.session.add(fc)
            db.session.commit(fc)