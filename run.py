import argparse
import os
import sys
import schedule
from app.banlist import initialize_unsafe_connections_list
from app.geolocation import GeoLocation
from app.database import RethinkDB
from app.sniffer import Counters

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--clear_db", action="store_true", help="Clear database")
    parser.add_argument("-d", "--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("-g", "--initialize_geolocation", action="store_true", help="(Re-)Initialize geolocation module")
    parser.add_argument("-u", "--initialize_unsafe", action="store_true", help="Initialize a new set of unsafe URLs, domains and IPs")

    args = parser.parse_args()
    
    if args.clear_db:
        RethinkDB().clear_db()
        RethinkDB.create_all_tables()
    if args.initialize_unsafe:
        initialize_unsafe_connections_list()
    if args.initialize_geolocation:
        GeoLocation.initialize()
    if args.daemon:
        c = Counters()
        schedule.every(1).minutes.do(c.store_counters())

        while 1:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
    main()