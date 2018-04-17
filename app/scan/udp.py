import socket
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser


def udp_scan(hostname):
    open_ports = []
    for port in range(1950, 2100):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.1)
            s.sendto(b"test", (hostname, port))
            data, server = s.recvfrom(4096)
            print(data)
        except Exception as e:
            print(e)
            print(str(port))
        finally:
            s.close()
    return open_ports