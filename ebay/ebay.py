import requests
from bs4 import BeautifulSoup
import csv

class EbayScraper:
  product_list = []
  searchitem = 'canon+m50'
  headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7,ar-PS;q=0.6,ar;q=0.5',
    'cache-control': 'max-age=0',
    'cookie': 'JSESSIONID=FBB2DB4B2A4E4A529007BE81C85D6E9C; ak_bmsc=61BB9CE3D4BDF1B5ACBA47416DC0BE5E76627124544E00003DD92360906F0B41~plZ8Rg7PwrCtL7nVxsQGqnvFMdY1aqvHu8eGF9bIedOS2WKutoqTCYu8RIpXPtJTiPyCraZy3jTgXBzKg4Z4IOvyDFMwBLWwBUW+S/U/iy3sLw7m7VrI6ErLjISOZFV96ExnP6kaxsyxiWCITPJlppmCVOsjnCrdPsSaw/8v8H+X7Z+ZWKVN5aTHVpXVGa4dGXJfe8n+o6Ya3nt6CjKOgkAN6Mcndk9rk/AVxxKiT9mUQ=; dp1=bpbf/%23600020000001000200000062050d79^u1p/QEBfX0BAX19AQA**63e640f9^bl/ID63e640f9^; ns1=BAQAAAXdgCei2AAaAANgASmIFDXljNjl8NjAxXjE2MTI5Mzg3ODQ3ODleXjFeM3wyfDV8NHw3fDExXl5eNF4zXjEyXjEyXjJeMV4xXjBeMV4wXjFeNjQ0MjQ1OTA3NefeO54ojZ/wQHZyx1xR/GaXwV9y; s=CgAD4ACBgJSt5OGFhNGFmZWUxNzcwYWM3N2MzMjYyODE0ZmZmNTVjMjUA7gCuYCUreTMGaHR0cHM6Ly93d3cuZWJheS5jb20vc2NoL2kuaHRtbD9fZnJvbT1SNDAmX3Rya3NpZD1wMjMzNDUyNC5tNTcwLmwxMzEzJl9ua3c9c29ubnkrY2FtZXJhJl9zYWNhdD0wJkxIX1RpdGxlRGVzYz0wJl9vZGt3PXNvbnkmX29zYWNhdD0wJkxIX0NvbXBsZXRlPTEmTEhfU29sZD0xI2l0ZW00NDZiNzNhOGZmB7LvizU*; nonsession=BAQAAAXdgCei2AAaAAAgAHGBLZvkxNjEyOTQ3NDI0eDI5Mzg2MDUxODE0M3gweDJOAMoAIGPmQPk4YWE0YWZlZTE3NzBhYzc3YzMyNjI4MTRmZmY1NWMyNQAzAAViBQ15MTE0MzAAywABYCPhATZyyirgtfAaf0QarxjJYX9y2MRSEg**; bm_sv=2FBD38C8A8FC051622B6A61AD3616D92~MAL2chEgkLU7G72INZZ0WT1eLOTfdeB5goJpuowFlvGFp6HlcOh7HyA9iyVRb6tpl2br35PB+/gedz6tANpgd26rWXi34dr69jTDuLGZiYPLdjXjGpq2pUc2rKeowZPxBnaIyfiWM6pn+Ma2jYHO1C4U2ANRIsMgnvREs0/CFRA=; npii=btguid/8aa4afee1770ac77c3262814fff55c2563e6418d^cguid/8aa4c1461770a77d0a2110adfc36be0163e6418d^; ebay=%5Ejs%3D1%5Esbf%3D%23%5Epsi%3DACQ5fDPs*%5E; ds2=sotr/b8_5az10JNfz^',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
  }

  def get_data(self, url):
    res = requests.get(url, headers=self.headers)
    return res

  def parse(self, html):
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find_all('div', {'class': 's-item__wrapper clearfix'})

    for item in results:
      try:
          bids = float(item.find('span', {'class': 's-item__bids'}).text.replace('bids', '').strip())
      except:
          bids = 'N/A'

      self.product_list.append({
        'title': item.find('h3', {'class': 's-item__title s-item__title--has-tags'}).text,
        'desc': item.find('div', {'class': 's-item__subtitle'}).text,
        'soldprice': float(item.find('span',{'class': 's-item__price'}).text.replace('IDR','').replace(',','').strip()),
        'solddate': item.find('span', {'class': 's-item__title--tagblock__COMPLETED'}).find('span', {'class': 'POSITIVE'}).text.replace('Sold  ', '').strip(),
        'bids': bids,
        'thumbnail': item.find('img', {'class': 's-item__image-img'})['src']
      })

  def to_csv(self):
    with open(f'{self.searchitem}+ebay.csv', 'w') as csv_file:
      writer = csv.DictWriter(csv_file, fieldnames=self.product_list[0].keys())
      writer.writeheader()

      for row in self.product_list:
        writer.writerow(row)

  def run(self):
    for page in range(1, 11):
      print(f'Scraping Page {page}')
      url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={self.searchitem}&_sacat=0&LH_TitleDesc=0&LH_All=1&LH_Complete=1&rt=nc&LH_Sold=1&_pgn={page}'
      get_items = self.get_data(url)
      self.parse(get_items.text)
    
    self.to_csv()
    print('Work Done!')


if __name__ == '__main__':
  scraper = EbayScraper()
  scraper.run()