import time
import schedule
from ..anomaly_detection import analyze_counters
from ..email_sender import send_alerts
from ..geolocation import fix_unknown_geolocations
from .close_sessions import close_sessions

class Scheduler:
    @staticmethod
    def run():
        schedule.every(1).minutes.do(fix_unknown_geolocations)
        schedule.every(1).minutes.do(close_sessions)
        schedule.every(1).minutes.do(analyze_counters)
        
        schedule.every(1).minutes.do(send_alerts)
        while 1:
            schedule.run_pending()
            time.sleep(1)