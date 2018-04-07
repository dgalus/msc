import ipaddress

def is_local_address(ip):
    if ip >= 0x0A000000 and ip <= 0x0AFFFFFF:
        return True
    if ip >= 0xAC100000 and ip <= 0xAC1FFFFF:
        return True
    if ip >= 0xC0A80000 and ip <= 0xC0A8FFFF:
        return True
    return False