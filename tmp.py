from app.database import *
from app.scheduler import *
import json
import datetime
from sqlalchemy import and_

config = json.load(open("config.json"))
db = Database(config["database"]["user"], 
              config["database"]["password"], 
              config["database"]["host"], 
              config["database"]["port"], 
              config["database"]["db"])

analyze_geolocations()