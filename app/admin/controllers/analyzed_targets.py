from .. import *

@app.route('/analyzed_targets/blocked_ip', methods=['GET'])
def blocked_ip():
    blocked_ips = db.session.query(UnsafeIP).all()
    return render_template('analyzed_targets/blocked_ip.html', blocked_ips=blocked_ips)

@app.route('/analyzed_targets/blocked_domains', methods=['GET'])
def blocked_domains():
    blocked_domains = db.session.query(UnsafeDomain).all()
    return render_template('analyzed_targets/blocked_domains.html', blocked_domains=blocked_domains)