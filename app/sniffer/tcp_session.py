class TCPSession:
    def __init__(self, ip_src, ip_dst, src_port, dst_port, remote_geolocation=None):
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.src_port = src_port
        self.dst_port = dst_port
        self.remote_geolocation = remote_geolocation
        self.segments = set()

    def insert_segment(ip_src, ip_dest, src_port, dst_port, tcp_segment):
        pass