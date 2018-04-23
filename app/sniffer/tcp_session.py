from ..geolocation import GeoLocation

class TCPSession:
    def __init__(self, ip_src, ip_dst, src_port, dst_port, remote_geolocation=None):
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.src_port = src_port
        self.dst_port = dst_port
        if remote_geolocation is not None:
            self.remote_geolocation = remote_geolocation
        else:
            # TODO: determine remote address
            self.remote_geolocation = GeoLocation.get_country_by_address(self.ip_dst)
        self.segments = set()