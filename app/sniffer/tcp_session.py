from .utils import *
from .. import user_config
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
            
            if not hosts_in_the_same_netowrk(user_config['local_netowrks'], ip_src, ip_dst):
                if is_local_address(ip_src):
                    self.remote_geolocation = GeoLocation.get_country_by_address(self.ip_dst)
                else:
                    self.remote_geolocation = GeoLocation.get_country_by_address(self.ip_src)
            else:
                self.remote_geolocation = 'LOCAL'
        self.segments = set()