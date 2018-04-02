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
from .counters import Counters

ip_queue = queue.Queue()
arp_queue = queue.Queue()
icmp_queue = queue.Queue()
udp_queue = queue.Queue()
tcp_queue = queue.Queue()
c = Counters()

class Sniffer:
    def __init__(self, interface_name):
        self.interface_name = interface_name
        self.ins = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
        self.ins.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**30)
        self.ins.bind((self.interface_name, ETH_P_ALL))
    
    def sniff(self):
        p_ip = threading.Thread(target=process_ip, daemon=True)
        p_arp = threading.Thread(target=process_arp, daemon=True)
        p_tcp = threading.Thread(target=process_tcp, daemon=True)
        p_icmp = threading.Thread(target=process_icmp, daemon=True)
        p_udp = threading.Thread(target=process_udp, daemon=True)
        p_ip.start()
        p_arp.start()
        p_tcp.start()
        p_icmp.start()
        p_udp.start()
        try:
            while True:
                pkt, sa_ll = self.ins.recvfrom(MTU)
                if len(pkt) <= 0:
                    break
                eth_header = struct.unpack("!6s6sH", pkt[0:14])
                if eth_header[2] == 0x800:
                    ip_queue.put(pkt)
                elif eth_header[2] == 0x806: 
                    arp_queue.put(pkt)
                c.l2_traffic += len(pkt)
                c.l2_frames += 1
        except(KeyboardInterrupt, SystemExit):
            sys.exit()
    

def process_ip():
    while True:
        pkt = ip_queue.get()
        if pkt is None:
            break
        c.l3_traffic += len(pkt)
        c.l3_frames += 1
        if pkt[23] == 1:
            icmp_queue.put(pkt)
        elif pkt[23] == 6:
            tcp_queue.put(pkt)
        elif pkt[23] == 17:
            udp_queue.put(pkt)
        print("process_ip()")

def process_arp():
    while True:
        pkt = arp_queue.get()
        if pkt is None:
            break
        c.l3_traffic += len(pkt)
        c.l3_frames += 1
        print("process_arp()")

def process_icmp():
    while True:
        pkt = icmp_queue.get()
        if pkt is None:
            break
        c.l4_traffic += len(pkt)
        c.l4_frames += 1
        c.icmp += 1
        print("process_icmp()")

def process_udp():
    while True:
        pkt = udp_queue.get()
        if pkt is None:
            break
        c.l4_traffic += len(pkt)
        c.l4_frames += 1
        c.udp += 1
        print("process_udp()")

def process_tcp():
    while True:
        pkt = tcp_queue.get()
        if pkt is None:
            break
        c.l4_traffic += len(pkt)
        c.l4_frames += 1
        c.tcp += 1
        ip_src = socket.inet_ntoa(pkt[26:30])
        ip_dst = socket.inet_ntoa(pkt[30:34])
        ip_hdrlen_st = struct.unpack("!B", pkt[14])
        ip_hdrlen = ip_hdrlen_st[0] & 0xf
        if dummy_hdrlen <= 5:
            src_port = struct.unpack('>H', payload[34:36])[0]
            dst_port = struct.unpack('>H', payload[36:38])[0]
        else:
            st_byte = ip_hdrlen*4
            src_port = struct.unpack('>H', payload[14+st_byte:16+st_byte])[0]
            dst_port = struct.unpack('>H', payload[16+st_byte:18+st_byte])[0]
        
        print("process_tcp()")