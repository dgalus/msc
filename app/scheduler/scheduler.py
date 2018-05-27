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
from .analyze_http_sites import analyze_http_sites
from .download_banlists import download_banlists
from .analyze_new_computers import analyze_new_computers
from .rebuild_computer_behavior import rebuild_computer_behavior
from .execute_admin_tasks import execute_admin_tasks
from .create_geolocation_statistics import create_geolocation_statistics
from .analyze_geolocations import analyze_geolocations
from .scan_ports import scan_ports

class Scheduler:
    @staticmethod
    def run():
        schedule.every(1).minutes.do(fix_unknown_geolocations)
        schedule.every(1).minutes.do(close_sessions)
        schedule.every(1).minutes.do(analyze_counters)
        schedule.every(1).minutes.do(look_for_unsafe_ip)
        schedule.every(1).minutes.do(add_computers_and_last_active)
        schedule.every(1).minutes.do(check_host_up)
        schedule.every(1).minutes.do(analyze_http_sites)
        schedule.every(1).minutes.do(rebuild_computer_behavior)
        schedule.every(2).minutes.do(execute_admin_tasks)
        schedule.every(10).minutes.do(analyze_new_computers)
        schedule.every(10).minutes.do(scan_ports)
        schedule.every(1).hours.do(create_geolocation_statistics)
        schedule.every(1).hours.do(analyze_geolocations)
        schedule.every(1).day.do(delete_old)
        schedule.every(1).day.do(download_banlists)
        schedule.every(1).minutes.do(send_alerts)
        while 1:
            schedule.run_pending()
            time.sleep(1)