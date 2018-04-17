import socket
import struct
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
        s = s + w
    s = (s>>16) + (s & 0xffff);
    s = s + (s >> 16);
    s = ~s & 0xffff
    return s

def tcp_connect_scan(dest_ip):
    open_ports = []
    for port in range(1, 65536):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.01)
            result = sock.connect_ex((dest_ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass
    return open_ports

def tcp_syn_scan(ip):
    pass

def tcp_ack_scan(ip):
    pass

def tcp_fin_scan(ip):
    pass