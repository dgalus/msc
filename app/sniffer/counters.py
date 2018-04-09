import json
import datetime

class Counters:
    def __init__(self):
        self.session_count = 0
        self.tcp_syn = 0
        self.tcp_ack = 0
        self.tcp_synack = 0
        self.tcp_psh = 0
        self.tcp_rst = 0
        self.tcp_fin = 0
        self.tcp = 0
        self.ip = 0
        self.arp = 0
        self.udp = 0
        self.icmp = 0
        self.l2_traffic = 0
        self.l3_traffic = 0
        self.l4_traffic = 0
        self.l2_frames = 0
        self.l3_frames = 0
        self.l4_frames = 0
    
    def store_counters(self):
        ins = {}
        ins["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        ins["session"] = self.session_count
        ins["tcp_syn"] = self.tcp_syn
        ins["tcp_ack"] = self.tcp_ack
        ins["tcp_synack"] = self.tcp_synack
        ins["tcp_psh"] = self.tcp_psh
        ins["tcp_rst"] = self.tcp_rst
        ins["tcp_fin"] = self.tcp_fin
        ins["tcp"] = self.tcp
        ins["ip"] = self.ip
        ins["arp"] = self.arp
        ins["udp"] = self.udp
        ins["icmp"] = self.icmp
        ins["l2_traffic"] = self.l2_traffic
        ins["l3_traffic"] = self.l3_traffic
        ins["l4_traffic"] = self.l4_traffic
        ins["l2_frames"] = self.l2_frames
        ins["l3_frames"] = self.l3_frames
        ins["l4_frames"] = self.l4_frames