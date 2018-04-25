import time
import schedule
from ..geolocation import fix_unknown_geolocations

class Scheduler:
    @staticmethod
    def run():
        schedule.every(1).minutes.do(fix_unknown_geolocations)
        while 1:
            schedule.run_pending()
            time.sleep(1)