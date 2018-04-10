import argparse
import os
import sys
import rethinkdb as r
from app import *
from app.banlist import initialize_unsafe_connections_list

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from config import *

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--clear_db", action="store_true", help="Clear database")
parser.add_argument("-u", "--initialize_unsafe", action="store_true", help="Initialize a new set of unsafe URLs, domains and IPs")

args = parser.parse_args()

if args.clear_db:
    pass
if args.initialize_unsafe:
    pass

initialize_unsafe_connections_list()