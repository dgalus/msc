class Counters:
    def __init__(self):
        self.session_count = 0
        self.tcp_syn = 0
        self.tcp_ack = 0
        self.tcp_synack = 0
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
        pass