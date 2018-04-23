import ipaddress

def is_local_address(ip):
    return ipaddress.IPv4Address(ip).is_private

def hosts_in_the_same_netowrk(network_list, ip1, ip2):
    for network in network_list:
        if ipaddress.IPv4Address(ip1) in ipaddress.IPv4Network(network) and ipaddress.IPv4Address(ip2) in ipaddress.IPv4Network(network):
            return True
    return False