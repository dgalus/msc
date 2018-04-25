import GeoIP
import requests
import shutil
import gzip
import os

URL = "http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz"
GEOIP_DB_FILE = './GeoIP.dat'

class GeoLocation:
    @staticmethod
    def initialize():
        response = requests.get(URL, stream=True)
        with open('GeoIP.dat.gz', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        f = gzip.open('GeoIP.dat.gz', 'rb')
        file_content = f.read()
        f.close()
        with open(GEOIP_DB_FILE, 'wb') as extracted:
            extracted.write(file_content)
        os.remove('GeoIP.dat.gz')
    
    @staticmethod
    def get_country_by_name(name):
        gi = GeoIP.open(GEOIP_DB_FILE, GeoIP.GEOIP_STANDARD)
        return gi.country_code_by_name(name)

    @staticmethod
    def get_country_by_address(address):
        gi = GeoIP.open(GEOIP_DB_FILE, GeoIP.GEOIP_STANDARD)
        return gi.country_code_by_addr(address)