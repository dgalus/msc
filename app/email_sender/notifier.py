import smtplib
from email.message import EmailMessage
from email.utils import make_msgid

def send_email(txt, txt_html, subject):
    with open("../config.json", "r") as f:
        config = json.loads(f.read())["notifications"]["mail"]
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = config['sender']
        msg['To'] = config['recipient']
        msg.preamble = subject
        msg.set_content(txt)
        msg.add_alternative("""<html><head></head><body>""" + txt_html + """</body></html>""", subtype="html")
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as s:
            s.send_message(msg)