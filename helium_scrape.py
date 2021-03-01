from helium import *
from bs4 import BeautifulSoup

url = 'http://cryptoslam.io/nba-top-shot/sales'
r = start_chrome(url, headless=True)
s = BeautifulSoup(r.page_source, 'html.parser')

table = s.find_all('table', {'class': 'table'})
cards = []

def cardlist():
    for item in table:
        try:
            card = item.find('tbody').find('tr').text
        except:
            card = ''
        cards.append(card)
    return cards

print(cardlist())