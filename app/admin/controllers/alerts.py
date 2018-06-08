from .. import *

@app.route('/alerts', methods=['GET'])
def alerts():
    alerts_db = db.session.query(Alert).filter_by(admin_delete=False).all()
    alerts = []
    for a in alerts_db:
        d = {}
        d['id'] = a.id
        d['timestamp'] = a.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        d['alert_type'] = str(AlertType(a.alert_type))
        d['description'] = a.description
        d['rank'] = str(a.rank)
        alerts.append(d)
    return render_template('alerts/index.html', alerts=alerts)

@app.route('/mark_alert_as_viewed', methods=['POST'])
def mark_alert_as_viewed():
    try:
        alert_id = int(request.form['alert_id'])
        alert = db.session.query(Alert).filter_by(id=alert_id).first()
        alert.admin_delete = True
        db.session.commit()
    except:
        pass
    return redirect('/alerts')