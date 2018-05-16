import datetime
import json
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


class FakeCounter(base):
    __tablename__ = 'fake_counters'
    id = Column(Integer, primary_key=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    tcp_syn = Column(Integer, nullable=False)
    tcp_syn_avg = Column(Integer, nullable=False)
    tcp_rst = Column(Integer, nullable=False)
    tcp_rst_avg = Column(Integer, nullable=False)
    udp = Column(Integer, nullable=False)

    def __init__(self, tcp_syn, tcp_syn_avg, tcp_rst, tcp_rst_avg, udp):
        self.timestamp = datetime.datetime.now()
        self.tcp_syn = tcp_syn
        self.tcp_syn_avg = tcp_syn_avg
        self.tcp_rst = tcp_rst
        self.tcp_rst_avg = tcp_rst_avg
        self.udp = udp
        

class AdminPendingTask(base):
    __tablename__ = 'admin_pending_task'
    id = Column(Integer, primary_key=True, nullable=False)
    task = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    decision = Column(Boolean, nullable=True)
    is_finished = Column(Boolean, nullable=False)
    finished_timestamp = Column(DateTime, nullable=True)
    
    def __init__(self, task, timestamp=datetime.datetime.now()):
        self.task = task
        self.timestamp = timestamp
        self.is_finished = False
        

class AnalyzedIP(base):
    __tablename__ = 'analyzed_ip'
    id = Column(Integer, primary_key=True, nullable=False)
    ip = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    last_connection_timestamp = Column(DateTime, nullable=False)
    ports = Column(String, nullable=False)
    is_blacklisted = Column(String, nullable=False)
    is_admin_safe = Column(String, nullable=True)
    geolocation = Column(String, nullable=False)
    connected_from = Column(String, nullable=False)
    
    def __init__(self, ip, last_connection_timestamp, ports, is_blacklisted, geolocation, connected_from, timestamp=datetime.datetime.now()):
        self.ip = ip
        self.last_connection_timestamp = last_connection_timestamp
        self.ports = ports
        self.is_blacklisted = is_blacklisted
        self.geolocation = geolocation
        self.connected_from = connected_from
        self.timestamp = timestamp
        

class AnalyzedHTTPSite(base):
    __tablename__ = 'analyzed_http_site'
    id = Column(Integer, primary_key=True, nullable=False)
    domain = Column(String, nullable=False)
    urls = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    analyze_timestamp = Column(String, nullable=True)
    geolocation = Column(String, nullable=True)
    google_rank = Column(Integer, nullable=True)
    duckduckgo_rank = Column(Integer, nullable=True)
    last_visited = Column(DateTime, nullable=True)
    is_admin_safe = Column(Boolean, nullable=True)
    https = Column(Boolean, nullable=True)
    hsts = Column(Boolean, nullable=True)
    cors = Column(Boolean, nullable=True)
    bayes_safe = Column(Boolean, nullable=True)
    is_blacklisted = Column(Boolean, nullable=True)
    rank = Column(Integer, nullable=True)
    
    def __init__(self, domain, urls, ip):
        self.domain = domain
        self.urls = urls
        self.ip = ip
        

class Computer(base):
    __tablename__ = 'computer'
    id = Column(Integer, primary_key=True, nullable=False)
    ip = Column(String, nullable=False)
    alias = Column(String, nullable=True)
    active_use_times = Column(String, nullable=True)
    geolocations = Column(String, nullable=True)
    default_gw_mac = Column(String, nullable=True)
    default_gw_ip = Column(String, nullable=True)
    open_ports = Column(String, nullable=True)
    closed_ports = Column(String, nullable=True)
    filtered_ports = Column(String, nullable=True)
    last_ping_response_timestamp = Column(DateTime, nullable=True)
    last_active = Column(DateTime, nullable=True)
    last_port_scan = Column(DateTime, nullable=True)
    most_connected_ports = Column(String, nullable=True)
    
    def __init__(self, ip):
        self.ip = ip
        l = [0] * 1440
        d = { "mon" : l, "tue" : l, "wed" : l, "thu" : l, "fri" : l, "sat" : l, "sun" : l }
        self.active_use_times = json.dumps(d)
        
        
class GeolocationStatistics(base):
    __tablename__ = 'geolocation_statistics'
    id = Column(Integer, primary_key=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    geolocation_statistics = Column(String, nullable=False)
    
    def __init__(self, timestamp, geolocation_statistics):
        self.timestamp = timestamp
        self.geolocation_statistics = geolocation_statistics