from ..database import *
from ..alert import  generate_alert, AlertType, HighTrafficAmountAlert, TcpSynScanAlert, SynFloodAlert, TcpFinScanAlert
from sqlalchemy import func, and_
from statistics import *
import statistics
import datetime
import json
import math


def simple_exp_smoothing(series, alpha):
    result = [series[0]]
    for n in range(1, len(series)):
        result.append(alpha*series[n] + (1-alpha)*result[n-1])
    return result[-1]


def get_biggest_increase_in_window(series):
    inc = 0
    for i in range(len(series)):
        if i < len(series)-1:
            if series[i+1] - series[i] > inc:
                inc = series[i+1] - series[i]
    return inc


def sigmoid(a, b, x):
    try:
        return 1./(1+math.exp(-1.*a*(x-b)))
    except:
        return 0
    

def analyze_counters():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    
    season_length = config["system"]["traffic_amount_anomaly_detection_model"]["season_length"]
    window_size = config["system"]["traffic_amount_anomaly_detection_model"]["window_size"]
    sigmoid_threshold = config["system"]["traffic_amount_anomaly_detection_model"]["sigmoid_threshold"]
    alpha = config["system"]["traffic_amount_anomaly_detection_model"]["alpha"]
    
    lfc_syn = []
    lfc_rst = []
    l2_traffic = []
    real_rst = []
    real_syn = []
    
    counters = db.session.query(Counter).order_by(Counter.id.asc()).all()
    last_fake_counters = db.session.query(FakeCounter).order_by(FakeCounter.id.asc()).all()
    
    if len(counters) == 0:
        return
    
    for l in last_fake_counters:
        lfc_syn.append(l.tcp_syn)
        lfc_rst.append(l.tcp_rst)
    for lc in counters:
        l2_traffic.append(lc.l2_traffic)
        real_rst.append(lc.tcp_rst)
        real_syn.append(lc.tcp_syn)
    
    # L2 traffic
    differences_increase = []
    if len(l2_traffic) > 3:
        test_val = l2_traffic[-1]
        l2_traffic = l2_traffic[:-2]
        if len(l2_traffic) > season_length:
            start_item = len(l2_traffic) % season_length
            end_item = len(l2_traffic) - 1
            while True:
                if start_item - int(window_size/2) < 0:
                    differences_increase.append(get_biggest_increase_in_window(l2_traffic[0:start_item+int(window_size/2)]))
                else:
                    differences_increase.append(get_biggest_increase_in_window(l2_traffic[start_item-int(window_size/2):start_item+int(window_size/2)]))
                start_item += season_length
                if start_item > end_item:
                    stddev = stdev(l2_traffic[-season_length:])
                    forecast = l2_traffic[-1] + simple_exp_smoothing(differences_increase, alpha)
                    sigm_res = sigmoid(1./stddev, forecast, test_val)
                    if sigm_res > sigmoid_threshold:
                        generate_alert(AlertType.HIGH_TRAFFIC_AMOUNT, str(HighTrafficAmountAlert()), config["system"]["ranks"]["high_traffic_amount"])
                    break
    
    # TCP Syn
    differences_increase = []
    if len(lfc_syn) > 3:
        test_val = real_syn[-1]
        if len(lfc_syn) > season_length:
            start_item = len(lfc_syn) % season_length
            end_item = len(lfc_syn) - 1
            while True:
                if start_item - int(window_size/2) < 0:
                    differences_increase.append(get_biggest_increase_in_window(lfc_syn[0:start_item+int(window_size/2)]))
                else:
                    differences_increase.append(get_biggest_increase_in_window(lfc_syn[start_item-int(window_size/2):start_item+int(window_size/2)]))
                start_item += season_length
                if start_item > end_item:
                    stddev = stdev(lfc_syn[-season_length:])
                    forecast = lfc_syn[-1] + simple_exp_smoothing(differences_increase, alpha)
                    sigm_res = sigmoid(1./stddev, forecast, test_val)
                    if sigm_res > sigmoid_threshold:
                        two_min_ago = datetime.datetime.now() - datetime.timedelta(minutes=2)
                        ip_pair = db.session.query(TCPSession.ip_dst, TCPSession.ip_src).filter(TCPSession.last_segm_tstmp > two_min_ago).group_by(TCPSession.ip_dst, TCPSession.ip_src).order_by(func.count(TCPSession.ip_dst).desc()).first()
                        dst_ports = db.session.query(TCPSession.dst_port).filter(and_(TCPSession.last_segm_tstmp > two_min_ago, TCPSession.ip_dst == ip_pair[0])).all()
                        if len(dst_ports) > test_val*0.5:
                            generate_alert(AlertType.TCP_SYN_SCAN, str(TcpSynScanAlert(ip_pair[1])), config["system"]["ranks"]["tcp_syn_scan"])
                        else:
                            generate_alert(AlertType.SYN_FLOOD, str(SynFloodAlert(ip_pair[0], ip_pair[1])), config["system"]["ranks"]["syn_flood"])
                        fake_tcp_syn = mean(lfc_syn[-100:])
                        fake_tcp_syn_avg = fake_tcp_syn
                    else:
                        fake_tcp_syn = test_val
                        fake_tcp_syn_avg = mean(lfc_syn[-100:].append(test_val))
                    break
        else:
            fake_tcp_syn = real_syn[-1]
            fake_tcp_syn_avg = mean(real_syn)
    else:
        fake_tcp_syn = real_rst[-1]
        fake_tcp_syn_avg = mean(real_syn)
                
    
    # TCP RST
    differences_increase = []
    if len(lfc_rst) > 3:
        test_val = real_rst[-1]
        if len(lfc_rst) > season_length:
            start_item = len(lfc_rst) % season_length
            end_item = len(lfc_rst) - 1
            while True:
                if start_item - int(window_size/2) < 0:
                    differences_increase.append(get_biggest_increase_in_window(lfc_rst[0:start_item+int(window_size/2)]))
                else:
                    differences_increase.append(get_biggest_increase_in_window(lfc_rst[start_item-int(window_size/2):start_item+int(window_size/2)]))
                start_item += season_length
                if start_item > end_item:
                    stddev = stdev(lfc_rst[-season_length:])
                    forecast = lfc_rst[-1] + simple_exp_smoothing(differences_increase, alpha)
                    sigm_res = sigmoid(1./stddev, forecast, test_val)
                    if sigm_res > sigmoid_threshold:
                        two_min_ago = datetime.datetime.now() - datetime.timedelta(minutes=2)
                        scanner_ip = db.session.query(TCPSession.ip_src).filter(TCPSession.last_segm_tstmp > two_min_ago).group_by(TCPSession.ip_src).order_by(func.count(TCPSession.ip_src).desc()).first()[0]
                        generate_alert(AlertType.TCP_FIN_SCAN, str(TcpFinScanAlert(scanner_ip)), config["system"]["ranks"]["tcp_fin_scan"])
                        fake_tcp_rst = mean(lfc_rst[-100:])
                        fake_tcp_rst_avg = fake_tcp_rst
                    else:
                        fake_tcp_rst = test_val
                        fake_tcp_rst_avg = mean(lfc_rst[-100:].append(test_val))
                    break
        else:
            fake_tcp_rst = real_rst[-1]
            fake_tcp_rst_avg = mean(real_rst)
    else:
        fake_tcp_rst = real_rst[-1]
        fake_tcp_rst_avg = mean(real_rst)
    
    # fake counters push
    fc = FakeCounter(fake_tcp_syn, fake_tcp_syn_avg, fake_tcp_rst, fake_tcp_rst_avg, counters[-1].udp)
    db.session.add(fc)
    db.session.commit()
