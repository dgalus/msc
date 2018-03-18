import socket
import struct

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
    pass

def tcp_syn_scan(ip):
    pass

def tcp_ack_scan(ip):
    pass

def tcp_fin_scan(ip):
    pass

tcp_connect_scan('192.168.1.1')