from ..database import *
from ..search_engines import DuckDuckGo, Google
from ..geolocation import GeoLocation
from ..bayes import is_bayes_safe
import json
import requests
import datetime

def analyze_http_sites():
    config = json.load(open("config.json"))
    db = Database(config["database"]["user"], 
                  config["database"]["password"], 
                  config["database"]["host"], 
                  config["database"]["port"], 
                  config["database"]["db"])
    
    unsafe_ip = db.session.query(UnsafeIP.ip).all()
    unsafe_domain = db.session.query(UnsafeDomain.domain).all()
    unsafe_url = db.session.query(UnsafeURL.url).all()
    
    sites = db.session.query(AnalyzedHTTPSite).filter(AnalyzedHTTPSite.analyze_timestamp==None).all()
    for s in sites:
        s.analyze_timestamp = datetime.datetime.now()
        s.geolocation = GeoLocation.get_country_by_address(s.ip)
        s.google_rank = Google.get_position(s.domain)
        s.duckduckgo_rank = DuckDuckGo.get_position(s.domain)
        s.is_blacklisted = False
        if s.ip in unsafe_ip or s.domain in unsafe_domain:
            s.is_blacklisted = True
        urls = s.urls.split()
        for url in urls:
            if s.domain + url in unsafe_url:
                s.is_blacklisted = True
        
        if s.domain.startswith("http://"):
            domain = s.domain
        else:
            domain = "http://"+s.domain
        r = requests.get(domain)
        if r.url.startswith("https"):
            s.https = True
        else:
            s.https = False
        
        r = requests.get(domain, allow_redirects=False)
        if "Strict-Transport-Security" in r.headers:
            s.hsts = True
        else:
            s.hsts = False
        if "Access-Control-Allow-Origin" in r.headers:
            s.cors = True
        else:
            s.cors = False
        
        s.bayes_safe = is_bayes_safe(r.text)
        s.rank = 0
    db.session.commit()