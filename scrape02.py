import requests
from bs4 import BeautifulSoup
import csv

joblist = []
job = 'java+developer'
location = 'DKI+Jakarta'

def extract(job, location, page):
    url = f'https://id.indeed.com/lowongan-kerja?q={job}&l={location}&start={page}'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def transform(soup):
    items = soup.find_all('div', class_ = 'jobsearch-SerpJobCard')
    for item in items:
        href = f"https://id.indeed.com{item.find('a')['href']}"
        try:
            salary = item.find('span', class_ = 'salaryText').text.strip()
        except:
            salary = ''

        try: 
            location = item.find('span', class_ = 'location').text
        except:
            location = ''

        job = {
            'title': item.find('a').text.strip(),
            'company': item.find('span', class_ = 'company').text.strip(),
            'location': location,
            'salary': salary,
            'link': href,
            'summary': item.find('div', class_ = 'summary').text.strip().replace('\n', '')
        }
        joblist.append(job)
    return joblist

def get_pages():
    for i in range(0, 20, 10):
        print(f'Get {i} pages')
        get_data = extract(job, location, i)
        jobs = transform(get_data)
    return

get_pages()
# def to_csv(job, joblist):
#     p = get_pages()
#     with open(f'{job}-ebay.csv', 'w') as csv_file:
#         writer = csv.DictWriter(csv_file, fieldnames=joblist[0].keys())
#         writer.writeheader()

#         for row in joblist:
#             writer.writerow(row)
    
#     print('Work Done!')

# to_csv(job, joblist)