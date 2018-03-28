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
        pass
    
    def __recv(self):
        pass
    

arp_queue = queue.Queue()
ip_queue = queue.Queue()
icmp_queue = queue.Queue()
udp_queue = queue.Queue()
tcp_queue = queue.Queue()

def process_arp():
    pass

def process_ip():
    pass

def process_icmp():
    pass

def process_udp():
    pass

def process_tcp():
    pass