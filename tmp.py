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

ETH_P_ALL = 0x0003

class IPSniff:
    def __init__(self, interface_name):
        self.interface_name = interface_name
        self.ins = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
        self.ins.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**30)
        self.ins.bind((self.interface_name, ETH_P_ALL))
 
    def __process_ipframe(self, pkt_type, ip_header, payload):
        fields = struct.unpack("!BBHHHBBHII", ip_header)
        dummy_hdrlen = fields[0] & 0xf
        iplen = fields[2]
        ip_src = payload[12:16]
        ip_dst = payload[16:20]
        proto = payload[9]
        ip_frame = payload[0:iplen]
        ip_src_str = socket.inet_ntoa(ip_src)
        ip_dst_str = socket.inet_ntoa(ip_dst)
        
        if proto == 6 or proto == 17:
            if dummy_hdrlen <= 5:
                src_port = payload[20:22]
                dest_port = payload[22:24]
                src_port_int = struct.unpack('>H', src_port)[0]
                dst_port_int = struct.unpack('>H', dest_port)[0]
            else:
                st_byte = dummy_hdrlen*4
                src_port = payload[st_byte:st_byte+2]
                dest_port = payload[st_byte+2:st_byte+4]
                src_port_int = struct.unpack('>H', src_port)[0]
                dst_port_int = struct.unpack('>H', dest_port)[0]
            key = ("%s:%d -> %s:%d" % (ip_src_str, src_port_int, ip_dst_str, dst_port_int))
            q.put(key)
            
    def recv(self):
        while True:
            pkt, sa_ll = self.ins.recvfrom(MTU)
            if len(pkt) <= 0:
                break
            eth_header = struct.unpack("!6s6sH", pkt[0:14])
            dummy_eth_protocol = socket.ntohs(eth_header[2])
            if eth_header[2] != 0x800 :
                continue
            ip_header = pkt[14:34]
            payload = pkt[14:]
            self.__process_ipframe(sa_ll[2], ip_header, payload)

def process_packet():
    while True:
        key = q.get()
        if key is None:
            break
        if key in packets:
            packets[key] += 1
        else:
            packets[key] = 1

def print_stats():
    while True:
        os.system('clear')
        for key, value in packets.items():
            print(key + ": " + str(value))
        time.sleep(1)

packets = dict()
q = queue.Queue()
t = threading.Thread(target=process_packet)
t.start()
t2 = threading.Thread(target=print_stats)
t2.start()

ip_sniff = IPSniff(sys.argv[1])
ip_sniff.recv()

t.join()
t2.join()