import scrapy

class WhiskySpider(scrapy.Spider):
    name = 'whisky'
    start_urls = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    def parse(self, response):
        products = response.css('div.product-item-info')
        for product in products:
            try:
                yield {
                    'name': product.css('a.product-item-link::text').get(),
                    'price': product.css('span.price::text').get().replace('£', ''),
                    'link':  product.css('a.product-item-link').attrib['href']
                }
            except:
                yield {
                'name': product.css('a.product-item-link::text').get(),
                'price': 'sold out',
                'link':  product.css('a.product-item-link').attrib['href']
                }
        
        next_page = response.css('a.action.next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        