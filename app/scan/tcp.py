from libnmap.process import NmapProcess
from bs4 import BeautifulSoup

def tcp_connect_scan(ip):
    nm = NmapProcess(ip, options="-sT -T4 -p 1-65535")
    nm.run()
    soup = BeautifulSoup(nm.stdout, "lxml")
    ports_xml = soup.find('host').find('ports').find_all('port')
    open_ports = []
    for px in ports_xml:
        if px.find('state').get('state') == 'open':
            open_ports.append(int(px.get('portid')))
    return open_ports

def tcp_syn_scan(ip):
    nm = NmapProcess(ip, options="-sS -T4 -p 1-65535")
    nm.run()
    soup = BeautifulSoup(nm.stdout, "lxml")
    ports_xml = soup.find('host').find('ports').find_all('port')
    open_ports = []
    for px in ports_xml:
        if px.find('state').get('state') == 'open':
            open_ports.append(int(px.get('portid')))
    return open_ports

def tcp_ack_scan(ip):
    nm = NmapProcess(ip, options="-sA -T4 -p 1-65535")
    nm.run()
    soup = BeautifulSoup(nm.stdout, "lxml")
    ports_xml = soup.find('host').find('ports').find_all('port')
    open_ports = []
    for px in ports_xml:
        if px.find('state').get('state') == 'open':
            open_ports.append(int(px.get('portid')))
    return open_ports    

def tcp_fin_scan(ip):
    nm = NmapProcess(ip, options="-sF -T4 -p 1-65535")
    nm.run()
    soup = BeautifulSoup(nm.stdout, "lxml")
    ports_xml = soup.find('host').find('ports').find_all('port')
    closed_ports = []
    for px in ports_xml:
        if px.find('state').get('state') == 'closed':
            closed_ports.append(int(px.get('portid')))
    return closed_ports