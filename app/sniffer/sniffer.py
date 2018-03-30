import socket, struct, os, array, sys
from scapy.all import ETH_P_ALL
from scapy.all import select
from scapy.all import MTU
from scapy.config import conf
import ctypes
import fcntl
import queue
import threading
import time

class Sniffer:
    def __init__(self, interface_name):
        self.interface_name = interface_name
        self.ins = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
        self.ins.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**30)
        self.ins.bind((self.interface_name, ETH_P_ALL))
    
    def sniff(self):
        while True:
            pkt, sa_ll = self.ins.recvfrom(MTU)
            if len(pkt) <= 0:
                break
            eth_header = struct.unpack("!6s6sH", pkt[0:14])
            if eth_header[2] != 0x800 :
                continue
            ip_queue.put(pkt)
            
    def __recv(self):
        pass
    

arp_queue = queue.Queue()
ip_queue = queue.Queue()
icmp_queue = queue.Queue()
udp_queue = queue.Queue()
tcp_queue = queue.Queue()

def process_ip(pkt):
    while True:
        pkt = ip_queue.get()
        if pkt is None:
            break

def process_arp():
    pass

def process_icmp():
    pass

def process_udp():
    pass

def process_tcp():
    pass