import scrapy

from scrapy_APP.items import DesktopItem
from scrapy_APP.scrapy_redis.spiders import RedisSpider
from scrapy_APP.utils.SeleniumUtils import DesktopLinkExtractor

from urllib.parse import urljoin


class SimpleDesktopSpider(RedisSpider):
    name = 'simple_desktop'
    redis_key = 'simple:start_urls'
    allowed_domains = ['simpledesktops.com']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.extractor = DesktopLinkExtractor()

    def parse(self, response):
        image_details = response.xpath("//div[@class='desktop']/a/@href").extract()
        # img = response.xpath("//div[@class='desktop']/a/@href").extract_first()
        for img in image_details:
            url = urljoin(response.url, img)

            link = self.extractor.extract_download_link(url)

            item = DesktopItem()
            item['src'] = [link]
            yield item





