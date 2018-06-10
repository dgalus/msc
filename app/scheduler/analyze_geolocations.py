from ..database import *
from ..alert import generate_alert, AbnormallyManyConnectionsToGeolocation, AlertType
import json
import datetime

def analyze_geolocations():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    all_last_max_values = {}
    current_values = {}
    last = db.session.query(GeolocationStatistics).order_by(GeolocationStatistics.id.desc()).first()
    if last:
        all_gs = db.session.query(GeolocationStatistics).order_by(GeolocationStatistics.id.asc()).all()
        all_gs = all_gs[:-1]
        if len(all_gs) > 1:
            curr = json.loads(last.geolocation_statistics)
            for g in curr["statistics"]:
                current_values[g['geolocation']] = g['perc']
            for ags in all_gs:
                jags = json.loads(ags.geolocation_statistics)
                for s in jags["statistics"]:
                    dict_val = all_last_max_values.get(s["geolocation"], 0)
                    if s["perc"] > dict_val:
                        all_last_max_values[s["geolocation"]] = s["perc"]
            print(all_last_max_values)
            for geolocation, perc in current_values.items():
                if perc/2 > all_last_max_values.get(geolocation, 0):
                    amc = AbnormallyManyConnectionsToGeolocation(geolocation)
                    generate_alert(AlertType.ABNORMALLY_MANY_CONNECTIONS_TO_GEOLOCATION, str(amc), config["system"]["ranks"]["abnormally_many_connections_to_geolocation"])