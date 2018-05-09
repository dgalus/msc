from ..database import *
from ..alert import  generate_alert, AlertType, HighTrafficAmountAlert, TcpSynScanAlert, SynFloodAlert, TcpFinScanAlert
from sqlalchemy import func, and_
import statistics
import datetime
import json

def is_outlier(traffic, test_value):
    config = json.load(open("config.json"))
    traffic_without_duplicates = list(set(traffic))
    stddev = stdev(traffic_without_duplicates)
    avg = mean(traffic_without_duplicates)
    if test_value > (config['system']['sigmas']*stddev)+avg:
        return True
    return False

def is_outlier_by_last(traffic, test_value):
    traffic_without_duplicates = list(set(traffic))
    stddev = stdev(traffic_without_duplicates)
    last = traffic[-1]
    if test_value > (config['system']['sigmas']*stddev)+last:
        return True
    return False

def analyze_counters():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    last_counters = db.session.query(Counter).order_by(Counter.id.desc()).limit(1000).all()
    last_fake_counters = db.session.query(FakeCounter).order_by(FakeCounter.id.desc()).limit(1000).all()
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
                # check long-term forecast
                one_minute = datetime.timedelta(minutes=1)
                current_time = datetime.datetime.now()
                ltf = db.session.query(L2TrafficForecast.forecast).filter(and_(L2TrafficForecast.timestamp <= (current_time+one_minute), L2TrafficForecast.timestamp >= current_time)).first()
                if ltf:
                    if lc_l2traffic > (ltf*config['system']['long_forecast_traffic_interval']):
                        # check short-term forecast
                        if is_outlier_by_last(lc_l2traffic[:-1], lc_l2traffic[-1]):
                            ht = HighTrafficAmountAlert()
                            if mean(lc_l2traffic[:-1])*3 < lc_l2traffic[-1]:
                                rank = 60
                            else:
                                rank = 20
                            generate_alert(AlertType.HIGH_TRAFFIC_AMOUNT, str(ht), rank)
                else:
                    # check short-term forecast
                    if is_outlier_by_last(lc_l2traffic[:-1], lc_l2traffic[-1]):
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
                # TODO: generate alert (decide if syn-flood or syn scan)
                
            else:
                new_tcp_syn = last_counters[-1].tcp_syn
                lfc_syn.append(last_counters[-1].tcp_syn)
                avg_syn = mean(lfc_syn)
                
            # higher tcp_rst (fake_counters)
            if is_outlier(lfc_rst, last_counters[-1].tcp_rst):
                new_tcp_rst = last_fake_counters[-1].tcp_rst_avg
                avg_rst = last_fake_counters[-1].tcp_rst_avg
                current_time = datetime.datetime.now()
                two_min_ago = current_time - datetime.timedelta(minutes=2)
                scanner_ip = db.session.query(TCPSession.ip_src).filter(TCPSession.last_segm_tstmp > two_min_ago).group_by(TCPSession.ip_src).order_by(func.count(TCPSession.ip_src).desc()).first()[0]
                generate_alert(AlertType.TCP_FIN_SCAN, TcpFinScanAlert(scanner_ip), 60)
            else:
                new_tcp_rst = last_counters[-1].tcp_rst
                lfc_rst.append(last_counters[-1].tcp_rst)
                avg_rst = mean(lfc_rst)
            fc = FakeCounter(new_tcp_syn, avg_syn, new_tcp_rst, avg_rst, last_counters[-1].udp)
            db.session.add(fc)
            db.session.commit(fc)
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