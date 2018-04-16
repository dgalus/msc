from enum import Enum

class PingScanResponse(Enum):
    HOST_AVAILABLE = 1
    HOST_UNAVAILABLE = 2

class TCPConnectScanResponse(Enum):
    PORT_OPEN = 1
    PORT_CLOSED = 2

class TCPSynScanResponse(Enum):
    PORT_OPEN = 1
    PORT_CLOSED = 2

class TCPFinScanResponse(Enum):
    PORT_OPEN_OR_FILTERED = 1
    PORT_CLOSED = 2

class TCPAckScanResponse(Enum):
    PORT_SECURED = 1
    PORT_NOT_SECURED = 2

class UDPScanResponse(Enum):
    PORT_OPEN_OR_FILTERED = 1
    PORT_CLOSED = 2

from .ping import ping
from .tcp import tcp_ack_scan, tcp_connect_scan, tcp_fin_scan, tcp_syn_scan
from .udp import udp_scan