import csv
import requests
import json
import re
import time
from random import randint

results = []
headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'Referer': 'https://www.walmart.com/browse/electronics/all-laptop-computers/3944_3951_1089430_132960',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'wm_client_ip': ''
}

def fetch(url):
    req = requests.get(url, headers=headers)
    data = json.loads(req.text)

    for i in range(1, 40):
        product_regex = data['items'][i]['productPageUrl']
        desc = data['items'][i]['description']

        try:
            title = data['items'][i]['title']
            description = re.sub('<.*?>', '', desc)
            image = data['items'][i]['imageUrl']
            product = re.findall('(.+?)\??', product_regex)
        except:
            title = 'N/A'
            description = 'N/A'
            image = 'N/A'
            product = 'N/A'
        
        print(f'Get item {i}...')
    
        items = {
            'title': title,
            'description': description,
            'image': image,
            'product': product,
        }
        results.append(items)   
    return json.dumps(results, indent=2)


def output():
    with open('wm.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=results[0].keys())
        writer.writeheader()

        for row in results:
            writer.writerow(row)

def run():
    for page in range(1, 3):
        url = f'https://www.walmart.com/search/api/preso?cat_id=3944_3951_1089430_132960&prg=desktop&page={page}'
        fetch(url)
        time.sleep(randint(2, 5))
        print(f'Scraping Page {page}')
    # output()
    print('Work Done!')

if __name__ == '__main__':
    render = run()