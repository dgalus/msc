from enum import Enum

class PingScanResponse(Enum):
    HOST_AVAILABLE = 1
    HOST_UNAVAILABLE = 2

from .ping import ping
from .tcp import tcp_connect_scan, tcp_fin_scan, tcp_syn_scan
from .udp import udp_scan