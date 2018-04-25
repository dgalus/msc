from .. import *

@app.route('/analyzed_targets/blocked_ip', methods=['GET'])
def blocked_ip():
    blocked_ips = db.session.query(UnsafeIP).all()
    print(blocked_ip)
    return render_template('analyzed_targets/blocked_ip.html')