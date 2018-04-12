import argparse
import os
import sys
import rethinkdb as r
from app import config
from app.banlist import initialize_unsafe_connections_list
from app.geolocation import GeoLocation

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--clear_db", action="store_true", help="Clear database")
parser.add_argument("-d", "--daemon", action="store_true", help="Run as daemon")
parser.add_argument("-g", "--initialize_geolocation", action="store_true", help="(Re-)Initialize geolocation module")
parser.add_argument("-u", "--initialize_unsafe", action="store_true", help="Initialize a new set of unsafe URLs, domains and IPs")

args = parser.parse_args()

if args.clear_db:
    pass
if args.initialize_unsafe:
    initialize_unsafe_connections_list()
if args.initialize_geolocation:
    GeoLocation.initialize()
if args.daemon:
    pass



