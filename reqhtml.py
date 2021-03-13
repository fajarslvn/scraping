from requests_html import HTMLSession

url = 'https://www.amazon.com/HP-24mh-FHD-Monitor-Built/dp/B08BF4CZSV'

def get_price(url):
  s = HTMLSession()
  r = s.get(url)
  r.html.render(sleep=.2)

  product = {
      'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
      'price': r.html.xpath('//*[@id="priceblock_ourprice"]', first=True).text
  }
  print(product)
  return product

get_price(url)