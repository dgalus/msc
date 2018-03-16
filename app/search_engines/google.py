import requests
import bs4

class Google:
    def get_position(domain):
        r = requests.get('https://www.google.com/search?q=' + domain)
        print(r.text)
        
Google.get_position('radio.opole.pl')