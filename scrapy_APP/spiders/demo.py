import scrapy

from scrapy_APP.scrapy_redis.spiders import RedisSpider

from urllib.parse import urljoin


class DemoSpider(RedisSpider):
    name = "demo"
    redis_key = 'demo:start_urls'
    allowed_domains = ['localhost']

    def parse(self, response):
        xpath = response.xpath("//a/@href").extract()
        if xpath:
            for x in xpath:
                next_url = urljoin(response.url, x)
                print("Scraped: {}".format(next_url))
                yield scrapy.Request(url=next_url)


