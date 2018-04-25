class ComputerBehaviourModel:
    def __init__(self, IP, default_gateway, open_ports, geolocations, sessions_count, addressess):
        self.IP = IP
        self.default_gateway = default_gateway
        self.open_ports = open_ports
        self.geolocations = geolocations
        self.sessions_count = sessions_count
        self.addresses = addresses
    
    