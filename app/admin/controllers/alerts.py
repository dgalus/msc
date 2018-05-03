from .. import *

@app.route('/alerts', methods=['GET'])
def alerts():
    alerts = db.session.query(Alert).filter_by(admin_delete=False).all()
    for a in alerts:
        a.alert_type = str(AlertType(a.alert_type))
    return render_template('alerts/index.html', alerts=alerts)