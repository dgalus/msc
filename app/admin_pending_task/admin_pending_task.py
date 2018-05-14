import json

class AddNewSafeGeolocationTask:
    def __init__(self, geolocation):
        self.geolocation = geolocation
        
    def __str__(self):
        d = {}
        d["geolocation"] = self.geolocation
        d["task"] = "add_new_safe_geolocation"
        return json.dumps(d)
    

class AddNewSafePortTask:
    def __init__(self, port):
        self.port = port
        
    def __str__(self):
        d = {}
        d["port"] = self.port
        d["task"] = "add_new_safe_port"
        return json.dumps(d)