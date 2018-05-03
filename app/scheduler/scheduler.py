import time
import schedule
from ..anomaly_detection import analyze_counters
from ..email_sender import send_alerts
from ..geolocation import fix_unknown_geolocations
from .close_sessions import close_sessions
from .look_for_unsafe_ip import look_for_unsafe_ip
from .add_computers import add_computers_and_last_active
from .check_host_up import check_host_up
from .delete_old import delete_old

class Scheduler:
    @staticmethod
    def run():
        schedule.every(1).minutes.do(fix_unknown_geolocations)
        schedule.every(1).minutes.do(close_sessions)
        schedule.every(1).minutes.do(analyze_counters)
        schedule.every(1).minutes.do(look_for_unsafe_ip)
        schedule.every(1).minutes.do(add_computers_and_last_active)
        schedule.every(1).minutes.do(check_host_up)
        schedule.every(1).day.do(delete_old)
        
        schedule.every(1).minutes.do(send_alerts)
        while 1:
            schedule.run_pending()
            time.sleep(1)