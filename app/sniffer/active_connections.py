from .tcp_session import TCPSession

class ActiveConnections:
    def __init__(self):
        self.tcp_sessions = []

    def add_tcp_session(self, session):
        if isinstance(session, TCPSession):
            pass

    def add_tcp_datagram(self):
        pass

