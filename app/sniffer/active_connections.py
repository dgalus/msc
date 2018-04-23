from .tcp_session import TCPSession

class ActiveConnections:
    def __init__(self):
        self.tcp_sessions = set()

    def create_tcp_session(self, session):
        if isinstance(session, TCPSession):
            fs = find_session(session.ip_src, session.src_port, session.ip_dst, session.dst_port)
            if fs is None:
                self.tcp_sessions.add(session)
            

    def insert_tcp_segment(self, ip_src, src_port, ip_dst, dst_port, tcp_segment):
        session = find_session(ip_src, src_port, ip_dst, dst_port)
        if session is None:
            session = create_tcp_session(ip_src, src_port, ip_dst, dst_port)
        if session is not None:
            session.segments.append(tcp_segment)

    def find_session(self, ip_src, src_port, ip_dst, dst_port): 
        pass
