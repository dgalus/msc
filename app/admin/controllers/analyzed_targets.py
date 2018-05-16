from .. import *

@app.route('/analyzed_targets/blocked_ip', methods=['GET'])
def blocked_ip():
    blocked_ips = db.session.query(UnsafeIP).all()
    return render_template('analyzed_targets/blocked_ip.html', blocked_ips=blocked_ips)

@app.route('/analyzed_targets/blocked_domains', methods=['GET'])
def blocked_domains():
    blocked_domains = db.session.query(UnsafeDomain).all()
    return render_template('analyzed_targets/blocked_domains.html', blocked_domains=blocked_domains)

@app.route('/analyzed_targets/website_security_rate', methods=['GET'])
def website_security_rate():
    sites_db = db.session.query(AnalyzedHTTPSite).filter(AnalyzedHTTPSite.analyze_timestamp != None).all()
    sites = []
    for s in sites_db:
        d = {}
        d['domain'] = s.domain
        d['url'] = s.urls.split()
        d['ip'] = s.ip
        d['analyze_timestamp'] = s.analyze_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        d['geolocation'] = s.geolocation
        d['google_rank'] = s.google_rank
        d['duckduckgo_rank'] = s.duckduckgo_rank
        d['last_visited'] = s.last_visited.strftime("%Y-%m-%d %H:%M:%S")
        #d['admin_safe'] =
    return render_template('analyzed_targets/website_security_rate.html', sites=sites)

@app.route('/analyzed_targets/geolocation', methods=['GET'])
def geolocation():
    return render_template('analyzed_targets/geolocation.html')