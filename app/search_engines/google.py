import requests
from bs4 import BeautifulSoup

class Google:
    def get_position(domain):
        r = requests.get('https://www.google.com/search?q=' + domain)
        soup = BeautifulSoup(r.text, "html.parser")
        elements = soup.find_all("h3", class_="r")
        for i in range(0, len(elements)):
            if domain in str(elements[i]):
                return i
        return None