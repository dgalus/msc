class TCPSession:
    def __init__(self, ip_src, ip_dst, src_port, dst_port, size, packets=0, last_packet=None, remote_geolocation=None, traffic_pattern=None):
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.src_port = src_port
        self.dst_port = dst_port
        self.size = size
        self.packets = packets
        self.last_packet = last_packet
        self.remote_geolocation = remote_geolocation
        self.traffic_pattern = traffic_pattern