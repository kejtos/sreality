import scrapy
from sreality_scraper.items import SrealityItem

class FlatSpider(scrapy.Spider):
    name = 'sreality'
    allowed_domains = ['sreality.cz']
    start_urls = ['https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=500']

    def parse(self, response):
        resp_json = response.json()
        for item in resp_json['_embedded']['estates']:
            flat = SrealityItem()
            name = item['name']
            name = name.replace('\xa0', ' ')
            flat['title'] = name
            flat['image_url'] = item['_links']['images'][0]['href']
            yield flat