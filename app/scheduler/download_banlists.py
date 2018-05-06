from ..banlist import initialize_unsafe_connections_list
from ..database import *
import json

def download_banlists():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    db.session.query(UnsafeDomain).delete()
    db.session.query(UnsafeIP).delete()
    db.session.query(UnsafeURL).delete()
    db.session.commit()
    initialize_unsafe_connections_list()