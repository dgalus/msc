from enum import Enum
from collections import namedtuple


Alert = namedtuple("Alert", "alert_type description")


class AlertType(Enum):
    ARP_SPOOFING = 1
    NEW_HOST_DETECTED = 2
    SYN_FLOOD = 3
    TCP_SYN_SCAN = 4
    TCP_FIN_SCAN = 5
    HIGH_TRAFFIC_AMOUNT = 6
    
    def __str__(self):
        return self.name


class ARPSpoofingAlert:
    def __init__(self, ip_addr, arp_mac, db_mac):
        self.ip_addr = ip_addr
        self.arp_mac = arp_mac
        self.db_mac = db_mac
    
    def __str__(self):
        return ip.addr + " is known under " + db_mac + " but " + arp_mac + " found in reply. Check for ARP spoofing."


class NewHostDetectedAlert:
    def __init__(self, ip_addr):
        self.ip_addr = ip_addr
        
    def __str__(self):
        return "New host detected: " + ip_addr + "."
    
    
class SynFloodAlert:
    def __init__(self, victim_ip, attacker_ip):
        self.victim_ip = victim_ip
        self.attacker_ip = attacker_ip
        
    def __str__(self):
        return "Host " + self.victim_ip + " is possibly SYN-flooded by " + self.attacker_ip + "."
    
class TcpSynScanAlert:
    def __init__(self, scanner_ip):
        self.scanner_ip = scanner_ip
        
    def __str__(self):
        return "Host " + self.scanner_ip + " is scanning ports using TCP SYN scan method."
    
class TcpFinScanAlert:
    def __init__(self, scanner_ip):
        self.scanner_ip = scanner_ip
        
    def __str__(self):
        return "Host " + self.scanner_ip + " is scanning ports using TCP FIN scan method."
    
class HighTrafficAmountAlert:
    def __str__(self):
        return "Traffic is higher than usual."
        