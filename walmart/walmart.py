import requests
from bs4 import BeautifulSoup
import csv
import re
import time
from random import randint
import json

class WalmartScraper:
    results = []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7,ar-PS;q=0.6,ar;q=0.5',
        'cookie': 'DL=94066%2C%2C%2Cip%2C94066%2C%2C; vtc=dQ2h6-f9-HKFg2MQ0k4kXI; TS013ed49a=01538efd7c145c63a2c79f468084508a9df33930737501eabc8a7aaf1987afb06164c9a36d924447e0d8a50470bde1465ad5587b59; adblocked=false; TS012c809b=01538efd7c79105567516cdc8b616ef993b3572793fa9453a775d663c0586cb5f2a6cbadafe834800d8fa8bb3374e09da26663c29a; TS01af768b=01538efd7c79105567516cdc8b616ef993b3572793fa9453a775d663c0586cb5f2a6cbadafe834800d8fa8bb3374e09da26663c29a; TBV=7; _pxvid=9ca9c478-6bac-11eb-80f9-0242ac120007; tb_sw_supported=true; _gcl_au=1.1.1199497370.1612967468; GCRT=8558bd07-8afb-46a5-b634-ad0ff40b5f1d; hasGCRT=1; ACID=9d094730-6bac-11eb-a836-63b1183baffa; hasACID=1; s_vi=[CS]v1|3011F716E582404F-400008BB425C158E[CE]; TB_Latency_Tracker_100=1; TB_Navigation_Preload_01=1; TB_SFOU-100=1; TS01bae75b=01538efd7c932d0d23c8e478cdc2f071c9aa681e09c810b00ead5a4d7808bd79734b0ecfa1e55a92ee8bb3a877c84f26d41c4749da; wm_mystore=Fe26.2**36166245316fc6236781cacbd6b33c2a237dc06097d0984f7aa21671874cbd80*AVQpUVdJf7D_2-F_vNHY7g*sKud85XE0B7Pa3A9IUMQ68ZWsPzY28hfTBFt3ZkrP8Doaoml6lwyUjQD5kmq70ZLoZs6fgZXNZPKYl0ey--NyP8KST5gdsZu11y1FOQFviWwJujjq7TGHi0eMDkPDmRsrGRUffARWOlrcOlpRCsSeQ**96b6c689ae44f883e060a8b3f31ae7bda3af6cf5bfe65996a1acf2cacc50429b*4nrNeAUNkgjbIAqGR8Bge4dUr6SOdgpukbq0OnRZsZU; viq=Walmart; x-csrf-jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiY29va2llIiwidXVpZCI6IjE2YzJhMTYwLTcxYjctMTFlYi04ZDdhLTI3MjcxNWQ1NTUwMyIsImlhdCI6MTYxMzYzMTY3MywiZXhwIjoxNjE0NzExNjczfQ.WpOHWM3BlhVSh8gfpokWs_18ucjbYUpG2ze7DPwI6qc; s_sess=%20ent%3D8268%2522returnedbadstatus400%3B%20cp%3DY%3B%20cps%3D1%3B%20chan%3Dorg%3B%20v59%3DFruits%2520%2526%2520Vegetables%3B%20v54%3D400%253Ahttps%253A%252F%252Fwww.walmart.com%252Fgrocery%252Fbrowse%252FOrganic-Fruits-%2526-Vegetables%253Faisle%253D1256653758154_1256653758268%2526page%253D0%3B%20s_sq%3D%3B; akavpau_p14=1613632278~id=2c3285d186c31d112537bf508bdf0a46; s_pers=%20s_cmpstack%3D%255B%255B%2527seo_un%2527%252C%25271612969754763%2527%255D%255D%7C1770736154763%3B%20s_fid%3D26CC0B0E5A68294D-3CF66F07F21BD51A%7C1676703678619%3B%20s_v%3DY%7C1613633478627%3B%20gpv_p11%3DHealth%2520%2526%2520Nutrition%253AShop%2520All%2520Health%2520%2526%2520Nutrition%253ADP%253AHealth%2520%2526%2520Nutrition%7C1613633478673%3B%20gpv_p44%3Dno%2520value%7C1613633478681%3B%20s_vs%3D1%7C1613633478697%3B; s_pers_2=+s_cmpstack%3D%255B%255B%2527seo_un%2527%252C%25271612969754763%2527%255D%255D%7C1770736154763%3B+s_fid%3D26CC0B0E5A68294D-3CF66F07F21BD51A%7C1676703678619%3B+s_v%3DY%7C1613633478627%3B+gpv_p11%3DHealth%2520%2526%2520Nutrition%253AShop%2520All%2520Health%2520%2526%2520Nutrition%253ADP%253AHealth%2520%2526%2520Nutrition%7C1613633478673%3B+gpv_p44%3Dno%2520value%7C1613633478681%3B+s_vs%3D1%7C1613633478697%3BuseVTC%3DN%7C1676746882; cart-item-count=0; _fbp=fb.1.1613631687582.1650975869; adblocked=false; _ga=GA1.2.527089068.1613638312; _gid=GA1.2.1265283024.1613638312; cbp=206750547-1613633694025|422095935-1613644019657; athrvi=RVI~h1928ac3f-hc52c353; s_sess_2=c32_v%3DS2H%2Cnull%3B%20prop32%3DS2H-V%2CS2H; TS01b0be75=01538efd7c2a1d9da1be660469f85cebc5f93da6baa7b38c35cca51db6517d985ec7e54c2c876a10d16ede62c501d502a30fc8e7de; next-day=1613685600|true|false|1613736000|1613648032; location-data=94066%3ASan%20Bruno%3ACA%3A%3A0%3A0|21k%3B%3B15.22%2C46y%3B%3B16.96%2C1kf%3B%3B19.87%2C1rc%3B%3B23.22%2C46q%3B%3B25.3%2C2nz%3B%3B25.4%2C2b1%3B%3B27.7%2C4bu%3B%3B28.38%2C2er%3B%3B29.12%2C1o1%3B%3B30.14|2|7|1|1xun%3B16%3B0%3B2.44%2C1xtf%3B16%3B1%3B4.42%2C1xwj%3B16%3B2%3B7.04%2C1ygu%3B16%3B3%3B8.47%2C1xwq%3B16%3B4%3B9.21; TB_DC_Flap_Test=0; bstc=d1tBdJ5adPatdM9PV424o0; mobileweb=0; xpa=-MWXw|5Z16k|9Kguz|DRlBy; exp-ck=-MWXw29Kguz1; xpm=1%2B1613648032%2BdQ2h6-f9-HKFg2MQ0k4kXI~%2B0; com.wm.reflector="reflectorid:0000000000000000000000@lastupd:1613648186685@firstcreate:1612969302657"; _px3=bb38c3778095bc645c42d6858fe0e59e6977414622631d9c58b734176d2e3038:5v07WlcfkuW24+zPG5L6LfJPxVkIuf/+TlcxeeGywkhz72jH0gGAnC/NqOWnz4W4Zq6PxYNCrTQMdnZ5XjnIDA==:1000:PMPWL6+OBM1FmFTuklrXMxMvSMSr7SfUieJCFtw/CP/2B2VIPBPUewbTbUI8cwCU59aLzIdjYCBq32ZSe5DPj/vPc3BoyuaQm3lWzHxUB1Nayeox1gDuqMGHy8fW2PI9diO/3caQvMY3Tpa65ThObP1iWaNRaQNob/v+hVq4pRU=; akavpau_p8=1613648798~id=194f90bfead6dc04e2ae47fca4493d93; _uetsid=1e80075071b711eba4fc01ab3d60e304; _uetvid=1e81fce071b711eba865f98622cf4ebf; _pxde=07d62bedecb7a506524d74b70911df307c1473db98eb3d4f2c9bd354bf508603:eyJ0aW1lc3RhbXAiOjE2MTM2NDgyMDIyNDcsImZfa2IiOjAsImlwY19pZCI6W119',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'service-worker-navigation-preload': 'true',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
    }

    def fetch(self, url):
        req = requests.get(url, headers=self.headers)
        print(f'PAGE STATUS CODE {req.status_code}')
        return req

    def parse(self, html):
        content = BeautifulSoup(html, 'html.parser')
        cards = content.find_all('div', {'class': 'search-result-gridview-item-wrapper'})
        people = ' people'
        for card in cards:
            details = card.find('div', {'class': 'search-result-product-shipping-details'}).text.strip()
            img = card.find('div', {'class': 'orientation-square'}).find('img')['data-image-src']

            try:
                price = card.find('span', {'class': 'price-group'}).text
                rateby = card.find('span', {'class': 'stars-reviews-count'}).text.replace('ratings', ' people').strip()
                image = re.findall('(.+?)\?', img)[0]
            except:
                price = 'N/A'
                rateby = 'N/A'
                image = 'https://e7.pngegg.com/pngimages/807/613/png-clipart-computer-icons-jpeg-sold-out-text-warning-sign-thumbnail.png'
                

            items = {
                'description': card.find('a', {'class': 'truncate-title'}).find('span').text.replace('"', ' inch').strip(),
                'price': price,
                'details': re.sub('\u00a0', ' ', details),
                'rating': card.find('span', {'class': 'seo-avg-rating'}).text.strip(),
                'rate_by': rateby,
                'image': image
            }
            self.results.append(items)
            # json.dumps(items, indent=2)
        return self.results

    def output(self):
        with open('walmart.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

    def run(self):
        for page in range(1, 26):
            url = f'https://www.walmart.com/browse/electronics/all-laptop-computers/3944_3951_1089430_132960?page={page}'
            res = self.fetch(url)
            self.parse(res.text)
            time.sleep(randint(2, 5))

        self.output()
        print('FINISH!')

if __name__ == '__main__':
    scraper = WalmartScraper()
    scraper.run()
