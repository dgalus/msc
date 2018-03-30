from enum import Enum
from collections import namedtuple


Alert = namedtuple("Alert", "alert_type description")


class AlertType(Enum):
    ARP_SPOOFING = 1


class ARPSpoofingAlert:
    def __init__(self, ip_addr, arp_mac, db_mac):
        self.ip_addr = ip_addr
        self.arp_mac = arp_mac
        self.db_mac = db_mac
    
    def to_string(self):
        return ip.addr + " is known under " + db_mac + " but " + arp_mac + " found in reply. Check for ARP spoofing."


class Alerts:
    def __init__(self):
        self.alerts = []
    
    def push(self, alert):
        if isinstance(alert, Alert):
            self.alerts.append(alert)
        
    def store(self):
        pass