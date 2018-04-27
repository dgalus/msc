from enum import Enum
from collections import namedtuple


Alert = namedtuple("Alert", "alert_type description")


class AlertType(Enum):
    ARP_SPOOFING = 1
    NEW_HOST_DETECTED = 2
    SYN_FLOOD = 3
    TCP_SYN_SCAN = 4
    
    def __str__(self):
        return self.name


class ARPSpoofingAlert:
    def __init__(self, ip_addr, arp_mac, db_mac):
        self.ip_addr = ip_addr
        self.arp_mac = arp_mac
        self.db_mac = db_mac
    
    def to_string(self):
        return ip.addr + " is known under " + db_mac + " but " + arp_mac + " found in reply. Check for ARP spoofing."


class NewHostDetectedAlert:
    def __init__(self, ip_addr):
        self.ip_addr = ip_addr
        
    def to_string(self):
        return "New host detected: " + ip_addr + "."