import datetime
import os
from sqlalchemy import create_engine  
from sqlalchemy import Column, Boolean, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from .models import *
from . import base

class Database:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        db_string = "postgres://{}:{}@{}:{}/{}".format(user, password, host, port, database)
        engine = create_engine(db_string)  
        Session = sessionmaker(bind=engine)  
        self.session = Session()
        base.metadata.create_all(engine)
        
    def clear_db(self):
        self.session.query(Counter).delete()
        self.session.query(TCPSession).delete()
        self.session.query(TCPSegment).delete()
        self.session.query(UnsafeDomain).delete()
        self.session.query(UnsafeIP).delete()
        self.session.query(UnsafeURL).delete()
        self.session.query(UDPSegment).delete()
        self.session.query(ICMPSegment).delete()
        self.session.query(ARP).delete()
        self.session.query(ProposedIptablesRules).delete()
        self.session.query(Alert).delete()
        self.session.commit()