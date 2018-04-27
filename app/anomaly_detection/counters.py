from ..database import *
from ..alert import  generate_alert, AlertType

def analyze_counters():
    c = db.session.query(Counter).order_by(Counter.id.desc()).first()
    if c:
        pass