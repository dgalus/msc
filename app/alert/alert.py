from enum import Enum

class AlertType(Enum):
    ARP_SPOOFING = 1

class ARPSpoofingAlert:
    def __init__(self, ip_addr, arp_mac, db_mac):
        self.ip_addr = ip_addr
        self.arp_mac = arp_mac
        self.db_mac = db_mac
    
    def to_string(self):
        pass

class Alert:
    def __init__(self, alert_type):
        pass