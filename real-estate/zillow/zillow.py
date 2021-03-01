import requests
from bs4 import BeautifulSoup
import csv

class ZillowScraper:
    results = []

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7,ar-PS;q=0.6,ar;q=0.5',
        'cache-control': 'no-cache',
        'cookie': 'zguid=23|%2458f94af8-3335-4481-a55d-3a3e096a9edb; zgsession=1|1de2c82c-4e6c-4fa0-893c-7cc36f6f9d0e; _ga=GA1.2.430083103.1612876442; _gid=GA1.2.1042360239.1612876442; _pxvid=addd9cf4-6ad8-11eb-b0fb-0242ac120008; zjs_user_id=null; zjs_anonymous_id=%2258f94af8-3335-4481-a55d-3a3e096a9edb%22; _gcl_au=1.1.983082546.1612876443; KruxPixel=true; DoubleClickSession=true; _fbp=fb.1.1612876444429.1190264926; KruxAddition=true; _pin_unauth=dWlkPU1ETTVZelZqTWpBdFpHWXdOeTAwWldVNUxXRXpaall0WWpJM016STNZVGczT0RBeg; ki_r=; g_state={"i_p":1612890056893,"i_l":1}; ki_s=; ki_t=1612882855701%3B1612882855701%3B1612882865921%3B1%3B3; JSESSIONID=FFB0DDA88ACEB54B23C01871F720E8B6; _uetsid=ae70d2a06ad811eba9a75357ac0f2052; _uetvid=ae7191606ad811eb9727c7de4f56c801; _px3=5631c5c5a8c2f3bb1e0bd12cf73d8c108c66d2a60aee25136bb243b8b5218f53:j9hq+hW1kRxuLxA4fSk45n2Qu6g/Q+aNA8hUzTxSB96C2TkuCR+6HBActqofpyVL2aS7AnYfz9hjwSODSiRU4Q==:1000:cXvc9Tbfcyqtn2XQssIW1UJerLyjduVOv35u/QxctZ+xyfbjQ3ybd8lC+ai8kWWLe4sN89B7yjM0iFoje15pKlD+KjEJoKnVte5DdG6JsTqEJE0tH+hJbKwxhHzGVCB+OqQwt98Y6MiD0Zb4ZUooh8Bc7CmzKx/HpKr0dTeNaLg=; AWSALB=OnnGEplW3wj95FJxX3uzWOaK5X3lueTD3K5wFTWlH0samY7h2Wmc3e1SoWch9hNbLKR7noROX2udjFWgZfcfje3oeN5gAFEmTD8l0CZ1ZMzwyWYy8D4vj8QEXjqK; AWSALBCORS=OnnGEplW3wj95FJxX3uzWOaK5X3lueTD3K5wFTWlH0samY7h2Wmc3e1SoWch9hNbLKR7noROX2udjFWgZfcfje3oeN5gAFEmTD8l0CZ1ZMzwyWYy8D4vj8QEXjqK; search=6|1615478845219%7Crect%3D41.00142206321784%252C-73.61403438085938%252C40.40906711857083%252C-74.34187861914063%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D2%26z%3D1%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%096181%09%09%09%09%09%09; _gat=1',
        'pragma': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    }

    def fetch(self, url, params):
        print(f'HTTP GET request to URl: {url}', end='')
        res = requests.get(url, params=params, headers=self.headers)
        print(f' | Status code: {res.status_code}')
        
        return res

    def save_response(self, res):
        with open('res.html', 'w') as html_file:
            html_file.write(res)

    def load_response(self):
        html = ''

        with open('res.html', 'r') as html_file:
            for line in html_file:
                html += line

        return html

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        cards = content.find_all('article', {'class': 'list-card'})
        
        for card in cards:
            try:
                ba = card.find('ul', {'class': 'list-card-details'}).find_all('li')[1].text.replace(',','').strip()
            except:
                ba = 'N/A'
            
            try:
                sqft = card.find('ul', {'class': 'list-card-details'}).find_all('li')[2].text.replace('-- sqft', 'N/A').strip()
            except:
                sqft = 'N/A'
            
            try:
                img = card.find('img')['src'].replace('data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7', 'N/A').strip()
            except:
                img = 'N/A'

            self.results.append({
                'price': card.find('div', {'class': 'list-card-price'}).text,
                'address': card.find('address', {'class', 'list-card-addr'}).text,
                'bds': card.find('ul', {'class': 'list-card-details'}).find_all('li')[0].text.replace(',','').strip(),
                'ba': ba,
                'sqft': sqft,
                'img': img
            })

    def to_csv(self):
        with open('zillow.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

    def run(self):
        for page in range(1, 21):
            params = {
                'searchQueryState': '{"pagination":{"currentPage":%s},"mapBounds":{"west":-74.40093013281245,"east":-73.55498286718745,"south":40.4487909557045,"north":40.96202658306895},"regionSelection":[{"regionId":6181,"regionType":6}],"isMapVisible":false,"filterState":{"isForSaleByAgent":{"value":false},"isNewConstruction":{"value":false},"isForSaleForeclosure":{"value":false},"isComingSoon":{"value":false},"isAuction":{"value":false}},"isListVisible":true}' % page
            }
            
            res = self.fetch(f'https://www.zillow.com/new-york-ny/{page}_p/', params)
            self.parse(res.text)

        self.to_csv()


if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()