import scrapy

from scrapy_APP.items import DemoItem
from scrapy_APP.scrapy_redis.spiders import RedisSpider

from urllib.parse import urljoin
import time


class DemoSpider(RedisSpider):
    name = "demo"

    allowed_domains = ['localhost']
    redis_key = 'demo:start_urls'
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_APP.pipelines.JsonWithEncodingPipeline': 300
        }
    }

    def parse(self, response):
        item = DemoItem()
        item['url'] = response.url
        # yield item
        print("scraping:", response.url)
        xpath = response.xpath("//a/@href").extract()
        if xpath:
            for x in xpath:
                next_url = urljoin(response.url, x)
                time.sleep(2)
                yield scrapy.Request(url=next_url)


