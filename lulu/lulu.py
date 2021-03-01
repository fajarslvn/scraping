import requests
from bs4 import BeautifulSoup
import re
import csv
# import json

# Bikin module yg belum dinamis: url, header, parse (content)

class LuluScraper:
    def __init__(self):
        self.results = []
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7,ar-PS;q=0.6,ar;q=0.5',
            'cache-control': 'max-age=0',
            'cookie': 'XSRF-TOKEN=bfea419f-6356-40cf-8b55-d4943e742f93; __cfduid=d6bdbfd960182d69c51defaeed2974ac81612973576; JSESSIONID=Y2-7987b0e9-4275-40c4-81fa-e3d2d26b2d87.accstorefront-58794cff9d-fsc9p; ROUTE=.accstorefront-58794cff9d-fsc9p; anonymous-consents=%5B%7B%22templateCode%22%3A%22PROFILE%22%2C%22templateVersion%22%3A1%2C%22consentState%22%3Anull%7D%5D; profile.consent.given=false; _gid=GA1.2.709702664.1612973583; visid_incap_1362943=U0q9EzL2TNeHgOjeyWL0AyEGJGAAAAAAQUIPAAAAAACGM5NSxW57vJqrmjyo25WY; incap_ses_1117_1362943=+269YtZDv1ZtHGGE0WGADyEGJGAAAAAAAA534veF6KKRpd8Xbm7PxA==; _fbp=fb.1.1612973630773.2063079043; WGuy9gYF=ID; cookie-notification=ACCEPTED; _ga=GA1.2.1743868858.1612973583; _gat_UA-138574541-1=1; _ga_XK00CLKQ26=GS1.1.1612973627.1.1.1612974160.0',
            'service-worker-navigation-preload': 'true',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }

    def fetch(self, url, s):
        print(f'HTTP GET request to URL: {url}', end='')
        req = s.get(url, headers=self.headers)
        print(f' | Status Code: {req.status_code}')
        return req

    def parse(self, html):
        content = BeautifulSoup(html, 'html.parser')
        cards = content.find_all('div', {'class': 'product-tile-main'})
        for card in cards:
            rgx = card.find('div', {'class': 'plp-prod-name'}).text
            title = re.sub(r'\d+\.?\d?\s?\w+|Packet?|(Approx|approx)+\.?\s?|(weight|Weight)+', '', rgx).strip()
            try:
                weight = re.findall(r'\d+\.?\d?\s?\w+|Packet?', rgx)[0].strip()
            except:
                weight = ''
            price = card.find('div', {'class': 'price'}).find('span').text.replace('QAR\u00a0', '').strip()
            image = 'https://www.luluhypermarket.com'+str(card.find('div', {'class': 'plp-prod-img'}).find('img')['src'])

            items = {'title': title, 'weight': weight, 'price': price, 'image': image}
            self.results.append(items)
        return self.results
        # return print(json.dumps(self.results, indent=2))

    def output(self, name):
        with open(f'{name}.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

    def run(self, s, name, r1, r2):
        for page in range(r1, r2):
            url = f'https://www.luluhypermarket.com/en-qa/fruits-vegetables-fresh-food-grocery/c/HY00216090?q=%3Adiscount-desc&page={page}'
            fetching = self.fetch(url, s)
            self.parse(fetching.text)
        
        self.output(name)
        print('Work Done!')


if __name__ == '__main__':
    scraper = LuluScraper()
    s = requests.Session()
    scraper.run(s, 'lulu-01', 0, 5)