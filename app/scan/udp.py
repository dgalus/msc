from libnmap.process import NmapProcess
from bs4 import BeautifulSoup


def udp_scan(ip):
    nm = NmapProcess(ip, options="-sU -T4 -p 1-65535")
    nm.run()
    soup = BeautifulSoup(nm.stdout, "lxml")
    ports_xml = soup.find('host').find('ports').find_all('port')
    open_ports = []
    closed_ports = []
    for px in ports_xml:
        if px.find('state').get('state') == 'open':
            open_ports.append(int(px.get('portid')))
        elif px.find('state').get('state') == 'closed':
            closed_ports.append(int(px.get('portid')))
    return { 'open' : open_ports, 'closed' : closed_ports }