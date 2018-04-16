import socket

def udp_scan(hostname):
    open_ports = []
    for port in range(1, 65536):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.01)
            s.sendto("test", (hostname, port))
            recv, svr = s.recvfrom(255)
        except ValueError:
            open_ports.append(port)
        s.close()
    return open_ports