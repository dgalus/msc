from ..database import Database, Alert
from ..alert import AlertType
from .email_sender import send_email
import json

def send_alerts():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"]) 
    alerts = db.session.query(Alert).filter_by(notification_sent=False).all()
    for alert in alerts:
        subject = "New Alert from NBAD system"
        txt = "Type: " + str(AlertType(alert.alert_type)) + "\n\n"
        txt += "Description: \n" + alert.description + "\n\n"
        txt += "Rank: " + str(alert.rank) + "\n"
        txt += "Time: " + alert.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        txt_html= "<b>Type:</b> " + str(AlertType(alert.alert_type)) + "<br/>"
        txt_html += "<b>Description:</b><br />" + alert.description + "<br />"
        txt_html += "<b>Rank:</b>" + str(alert.rank) + "<br />"
        txt_html += "<b>Time:</b>" + alert.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        alert.notification_sent = True
        send_email(txt, txt_html, subject)
    db.session.commit()