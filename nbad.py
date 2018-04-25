import argparse
import json
import sys
from app.banlist import initialize_unsafe_connections_list
from app.geolocation import GeoLocation
from app.database import Database
from app.scheduler import Scheduler

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--clear_db", action="store_true", help="Clear database")
    parser.add_argument("-d", "--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("-g", "--initialize_geolocation", action="store_true", help="(Re-)Initialize geolocation module")
    parser.add_argument("-u", "--initialize_unsafe", action="store_true", help="Initialize a new set of unsafe URLs, domains and IPs")

    args = parser.parse_args()
    
    if args.clear_db:
        config = json.load(open("config.json"))
        db = Database(config["database"]["user"], 
                      config["database"]["password"], 
                      config["database"]["host"], 
                      config["database"]["port"], 
                      config["database"]["db"]) 
        db.clear_db()
    if args.initialize_unsafe:
        initialize_unsafe_connections_list()
    if args.initialize_geolocation:
        GeoLocation.initialize()
    if args.daemon:
        Scheduler.run()

if __name__ == '__main__':
    main()