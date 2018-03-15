import socket, struct, os, array, sys
from scapy.all import ETH_P_ALL
from scapy.all import select
from scapy.all import MTU
from scapy.config import conf
import ctypes
import fcntl

ETH_P_ALL = 0x0003

packets = dict()

class IPSniff:
    def __init__(self, interface_name):#, on_ip_incoming, on_ip_outgoing):
        self.interface_name = interface_name
        #self.on_ip_incoming = on_ip_incoming
        #self.on_ip_outgoing = on_ip_outgoing
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
            if key in packets:
                packets[key] += 1
            else:
                packets[key] = 1
            os.system('clear')
            for key, value in packets.items():
                print(key + ": " + str(value))
            
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
 
def test_incoming_callback(src, dst, frame):
    print("incoming - src=%s, dst=%s, frame len = %d" %(socket.inet_ntoa(src), socket.inet_ntoa(dst), len(frame)))
 
def test_outgoing_callback(src, dst, frame):
    print("outgoing - src=%s, dst=%s, frame len = %d" %(socket.inet_ntoa(src), socket.inet_ntoa(dst), len(frame)))
 
ip_sniff = IPSniff(sys.argv[1])#, test_incoming_callback, test_outgoing_callback)
ip_sniff.recv()
