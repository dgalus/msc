import datetime
from sqlalchemy import Table, Column, Integer, String, ForeignKey, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

def connect(user, password, db, host='127.0.0.1', port=5432):
	url = 'postgresql://{}:{}@{}:{}/{}'
	url = ur.format(user, password, host, port, db)
	con = sqlalchemy.create_engine(url, client_encoding='utf8')
	meta = sqlalchemy.MetaData(bind=con, reflect=True)
	return con, meta

Base = declarative_base()

class Counter(Base):
	__tablename__ = 'counters'
	id = Column(Integer, primary_key=True)
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
		
