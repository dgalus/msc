import datetime
import os
from sqlalchemy import Column, Boolean, String, Integer, DateTime, ForeignKey
from . import base

class Counter(base):
    __tablename__ = 'counters'
    id = Column(Integer, primary_key=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    tcp_syn = Column(Integer, nullable=False)
    tcp_ack = Column(Integer, nullable=False)
    tcp_synack = Column(Integer, nullable=False)
    tcp_psh = Column(Integer, nullable=False)
    tcp_rst = Column(Integer, nullable=False)
    tcp_fin = Column(Integer, nullable=False)
    tcp = Column(Integer, nullable=False)
    ip = Column(Integer, nullable=False)
    arp = Column(Integer, nullable=False)
    udp = Column(Integer, nullable=False)
    icmp = Column(Integer, nullable=False)
    l2_traffic = Column(Integer, nullable=False)
    l3_traffic = Column(Integer, nullable=False)
    l4_traffic = Column(Integer, nullable=False)
    l2_frames = Column(Integer, nullable=False)
    l3_frames = Column(Integer, nullable=False)
    l4_frames = Column(Integer, nullable=False)

    def __init__(self, tcp_syn, tcp_ack, tcp_synack, tcp_psh, tcp_rst, tcp_fin, tcp, 
                     ip, arp, udp, icmp, l2_traffic, l3_traffic, l4_traffic, l2_frames, l3_frames, l4_frames):
        self.timestamp = datetime.datetime.now()
        self.tcp_syn = tcp_syn
        self.tcp_ack = tcp_ack
        self.tcp_synack = tcp_synack
        self.tcp_psh = tcp_psh
        self.tcp_rst = tcp_rst
        self.tcp_fin = tcp_fin
        self.tcp = tcp
        self.ip = ip
        self.arp = arp
        self.udp = udp
        self.icmp = icmp
        self.l2_traffic = l2_traffic
        self.l3_traffic = l3_traffic
        self.l4_traffic = l4_traffic
        self.l2_frames = l2_frames
        self.l3_frames = l3_frames
        self.l4_frames = l4_frames


class TCPSession(base):
    __tablename__ = 'tcp_session'
    id = Column(Integer, primary_key=True, nullable=False)
    ip_src = Column(String, nullable=False)
    src_port = Column(Integer, nullable=False)
    ip_dst = Column(String, nullable=False)
    dst_port = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)
    first_segm_tstmp = Column(DateTime, nullable=False)
    last_segm_tstmp = Column(DateTime, nullable=False)
    remote_geolocation = Column(String, nullable=False)

    def __init__(self, ip_src, src_port, ip_dst, dst_port, is_active, first_segm_tstmp, last_segm_tstmp, remote_geolocation):
        self.ip_src = ip_src
        self.src_port = src_port
        self.ip_dst = ip_dst
        self.dst_port = dst_port
        self.is_active = is_active
        self.first_segm_tstmp = first_segm_tstmp
        self.last_segm_tstmp = last_segm_tstmp
        self.remote_geolocation = remote_geolocation


class TCPSegment(base):
    __tablename__ = 'tcp_segment'
    id = Column(Integer, primary_key=True, nullable=False)
    flags = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    direction = Column(Integer, nullable=False)
    session_id = Column(Integer, ForeignKey('tcp_session.id'))

    def __init__(self, flags, size, timestamp, direction, session_id):
        self.flags = flags
        self.size = size
        self.timestamp = timestamp
        self.direction = direction
        self.session_id = session_id


class UnsafeURL(base):
    __tablename__ = 'unsafe_url'
    id = Column(Integer, primary_key=True, nullable=False)
    url = Column(String, nullable=False)

    def __init__(self, url):
        self.url = url


class UnsafeDomain(base):
    __tablename__ = 'unsafe_domain'
    id = Column(Integer, primary_key=True, nullable=False)
    domain = Column(String, nullable=False)

    def __init__(self, domain):
        self.domain = domain


class UnsafeIP(base):
    __tablename__ = 'unsafe_ip'
    id = Column(Integer, primary_key=True, nullable=False)
    ip = Column(String, nullable=False)

    def __init__(self, ip):
        self.ip = ip


class UDPSegment(base):
    __tablename__ = 'udp_segment'
    id = Column(Integer, primary_key=True, nullable=False)
    ip_src = Column(String, nullable=False)
    src_port = Column(Integer, nullable=False)
    ip_dst = Column(String, nullable=False)
    dst_port = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __init__(self, ip_src, src_port, ip_dst, dst_port, size, timestamp):
        self.ip_src = ip_src
        self.src_port = src_port
        self.ip_dst = ip_dst
        self.dst_port = dst_port
        self.size = size
        self.timestamp = timestamp


class ICMPSegment(base):
    __tablename__ = 'icmp_segment'
    id = Column(Integer, primary_key=True, nullable=False)
    ip_src = Column(String, nullable=False)
    ip_dst = Column(String, nullable=False)
    icmp_type = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __init__(self, ip_src, ip_dst, icmp_type, timestamp):
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.icmp_type = icmp_type
        self.timestamp = timestamp


class ARP(base):
    __tablename__ = 'arp'
    id = Column(Integer, primary_key=True, nullable=False)
    ip = Column(String, nullable=False)
    mac = Column(String, nullable=False)

    def __init__(self, ip, mac):
        self.ip = ip
        self.mac = mac


class ProposedIptablesRules(base):
    __tablename__ = 'proposed_iptables_rules'
    id = Column(Integer, primary_key=True, nullable=False)
    rule = Column(String, nullable=False)
    description = Column(String, nullable=False)
    notification_sent = Column(Boolean, nullable=False)
    admin_delete = Column(Boolean, nullable=False)    
    timestamp = Column(DateTime, nullable=False)
    rank = Column(Integer, nullable=False)

    def __init__(self, rule, description, notification_sent, admin_delete, timestamp, rank):
        self.rule = rule
        self.description = description
        self.notification_sent = notification_sent
        self.admin_delete = admin_delete
        self.timestamp = timestamp
        self.rank = rank

class Alert(base):
    __tablename__ = 'alert'
    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String, nullable=False)
    alert_type = Column(Integer, nullable=False)
    rank = Column(Integer, nullable=False)
    notification_sent = Column(Boolean, nullable=False)
    admin_delete = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __init__(self, description, alert_type, rank, notification_sent, admin_delete, timestamp):
        self.description = description
        self.alert_type = alert_type
        self.notification_sent = notification_sent
        self.admin_delete = admin_delete        
        self.rank = rank
        self.timestamp = timestamp
