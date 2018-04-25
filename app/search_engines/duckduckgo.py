import requests
from bs4 import BeautifulSoup

class DuckDuckGo:
    def get_position(domain):
        r = requests.post('https://duckduckgo.com/html/', data={'q':domain})
        soup = BeautifulSoup(r.text, 'html.parser')
        elements = soup.find_all("a", class_="result__a")
        for i in range(0, len(elements)):
            if "//" + domain in str(elements[i]):
                return i
        return None