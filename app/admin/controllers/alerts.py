from .. import *

@app.route('/alerts', methods=['GET'])
def alerts():
    alerts_db = db.session.query(Alert).filter_by(admin_delete=False).all()
    alerts = []
    for a in alerts_db:
        d = {}
        d['timestamp'] = a.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        d['alert_type'] = str(AlertType(a.alert_type))
        d['description'] = a.description
        d['rank'] = str(a.rank)
        alerts.append(d)
    return render_template('alerts/index.html', alerts=alerts)