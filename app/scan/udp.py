import socket

def udp_scan(hostname):
    open_ports = []
    for port in range(1950, 2500):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.1)
            s.sendto(b"test", (hostname, port))
            recv, svr = s.recvfrom(255)
        except ValueError:
            print(str(port) + "valueerror")
            open_ports.append(port)
        except socket.error:
            print(str(port) + "socket.error")
        s.close()
    return open_ports