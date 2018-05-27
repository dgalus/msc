from app.database import *

from app.scheduler import create_geolocation_statistics, analyze_geolocations
from app.geolocation import fix_unknown_geolocations

#fix_unknown_geolocations()
#create_geolocation_statistics()
analyze_geolocations()

