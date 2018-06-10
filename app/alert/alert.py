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
    UNSAFE_IP_DETECTED = 7
    ABNORMAL_ACTIVITY_TIME = 8
    NEW_GEOLOCATION_DETECTED = 9
    NEW_DESTINATION_PORT_DETECTED = 10
    ABNORMALLY_MANY_CONNECTIONS_TO_GEOLOCATION = 11
    NEW_OPEN_PORT_ON_HOST_DETECTED = 12
    
    def __str__(self):
        return self.name


class ARPSpoofingAlert:
    def __init__(self, ip_addr, arp_mac, db_mac):
        self.ip_addr = ip_addr
        self.arp_mac = arp_mac
        self.db_mac = db_mac
    
    def __str__(self):
        return ip_addr + " is known under " + db_mac + " but " + arp_mac + " found in reply. Check for ARP spoofing."


class NewHostDetectedAlert:
    def __init__(self, ip_addr):
        self.ip_addr = ip_addr
        
    def __str__(self):
        return "New host detected: " + self.ip_addr + "."
    
    
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
        
class UnsafeIPDetectedAlert:
    def __init__(self, ip):
        self.ip = ip
        
    def __str__(self):
        return "Blacklisted IP (" + ip + ")  transmission detected."
    
    
class AbnormalActivityTimeAlert:
    def __init__(self, ip, timestamp):
        self.ip = ip
        self.timestamp = timestamp
        
    def __str__(self):
        return "Abnormal activity time on the workstation with IP " + self.ip + " detected at " + self.timestamp.strftime("%Y-%m-%d %H:%M:%S") + "."
    
    
class NewGeolocationDetectedAlert:
    def __init__(self, ip, geolocation):
        self.ip = ip
        self.geolocation = geolocation
        
    def __str__(self):
        return "Computer " + self.ip + " established just now connection to new geolocation: " + self.geolocation + " which may be unsafe."
    
    
class NewDestinationPortDetectedAlert:
    def __init__(self, src_ip, dst_ip, port):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.port = port
        
    def __str__(self):
        return "Computer " + self.src_ip +" established just now connection with " + self.dst_ip + " on port " + str(self.port) + " which is not marked as safe."
    
    
class AbnormallyManyConnectionsToGeolocation:
    def __init__(self, geolocation):
        self.geolocation = geolocation
        
    def __str__(self):
        return "Abnormally many connections to geolocation: " + self.geolocation
    
    
class NewOpenPortOnHostDetected:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        
    def __str__(self):
        return "New open port (" + str(self.port) + ") detected on " + self.ip + "."