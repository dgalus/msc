from .. import *

@app.route('/alerts', methods=['GET'])
def alerts():
    alerts = db.session.query(Alert).filter_by(Alert.admin_delete == False).all()
    return render_template('alerts/index.html', alerts=alerts)