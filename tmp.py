import socket, struct, os, array, sys
from scapy.all import ETH_P_ALL
from scapy.all import select
from scapy.all import MTU
from scapy.config import conf
import ctypes
import fcntl

class ifreq(ctypes.Structure):
    _fields_ = [("ifr_ifrn", ctypes.c_char*16),
                ("ifr_flags", ctypes.c_short)]

class FLAGS(object):
    # linux/if_ether.h
    ETH_P_ALL     = 0x0003 # all protocols
    ETH_P_IP      = 0x0800 # IP only
    # linux/if.h
    IFF_PROMISC   = 0x100
    # linux/sockios.h
    SIOCGIFFLAGS  = 0x8913 # get the active flags
    SIOCSIFFLAGS = 0x8914 # set the active flags

class IPSniff:
    def __init__(self, interface_name):#, on_ip_incoming, on_ip_outgoing):
        self.interface_name = interface_name
        #self.on_ip_incoming = on_ip_incoming
        #self.on_ip_outgoing = on_ip_outgoing
 
        # The raw in (listen) socket is a L2 raw socket that listens
        # for all packets going through a specific interface.
        self.ins = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
        self.ins.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**30)
        self.ins.bind((self.interface_name, ETH_P_ALL))
 
    def __process_ipframe(self, pkt_type, ip_header, payload):
        # Extract the 20 bytes IP header, ignoring the IP options
        fields = struct.unpack("!BBHHHBBHII", ip_header)
        dummy_hdrlen = fields[0] & 0xf
        iplen = fields[2]
        ip_src = payload[12:16]
        ip_dst = payload[16:20]
        proto = payload[9]
        ip_frame = payload[0:iplen]
        
        if proto == 6 or proto == 17:
            if dummy_hdrlen <= 5:
                src_port = payload[20:22]
                dest_port = payload[22:24]
            else:
                st_byte = dummy_hdrlen*4
                src_port = payload[st_byte:st_byte+2]
                dest_port = payload[st_byte+2:st_byte+4]
            print("%s:%d -> %s:%d" % (socket.inet_ntoa(ip_src), struct.unpack('>H', src_port)[0], socket.inet_ntoa(ip_dst), struct.unpack('>H', dest_port)[0]))
 
#        if pkt_type == socket.PACKET_OUTGOING:
#            if self.on_ip_outgoing is not None:
#                self.on_ip_outgoing(ip_src, ip_dst, ip_frame)
#        else:
#            if self.on_ip_incoming is not None:
#                self.on_ip_incoming(ip_src, ip_dst, ip_frame)
 
    def recv(self):
        while True:
            pkt, sa_ll = self.ins.recvfrom(MTU)
#            if type == socket.PACKET_OUTGOING and self.on_ip_outgoing is None:
#                continue
#            elif self.on_ip_outgoing is None:
#                continue
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
