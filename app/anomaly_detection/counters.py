from ..database import *
from ..alert import  generate_alert, AlertType, HighTrafficAmountAlert, TcpSynScanAlert, SynFloodAlert, TcpFinScanAlert
from sqlalchemy import func, and_
import statistics
import datetime
import json


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
    
    counters = db.session.query(Counter).order_by(Counter.id.asc()).all()
    last_fake_counters = db.session.query(FakeCounter).order_by(FakeCounter.id.asc()).all()
    
    for l in last_fake_counters:
        lfc_syn.append(l.tcp_syn)
        lfc_rst.append(l.tcp_rst)
    for lc in counters:
        l2_traffic.append(lc.l2_traffic)
    
    # L2 traffic
    differences_increase = []
    test_val = l2_traffic[-1]
    l2_traffic = l2_traffic[:-2]    
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
    
    
    # TCP RST
    differences_increase = []
    test_val = lfc_rst[-1]
    lfc_rst = lfc_rst[:-2]    
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
                fake_tcp_rst_avg = mean(lfc_rst[-100:])
    
    
    # fake counters push
    #tcp_syn = 
    #tcp_syn_avg = 
    fc = FakeCounter(tcp_syn, tcp_syn_avg, fake_tcp_rst, fake_tcp_rst_avg, counters[-1].udp)
    db.session.add(fc)
    db.session.commit()
