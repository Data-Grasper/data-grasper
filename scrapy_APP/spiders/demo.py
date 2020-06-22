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
        }  # 选择我们提供的数据持久化pipeline
    }

    def parse(self, response):
        item = DemoItem()  # 根据感兴趣的字段生成的item
        item['url'] = response.url  # 将数据包装成item
        yield item  # 提交Item
        print("scraping:", response.url)  # 做些别的事情
        xpath = response.xpath("//a/@href").extract()  # 解析新的待抓取url
        if xpath:
            for x in xpath:
                next_url = urljoin(response.url, x)
                time.sleep(0.5)
                yield scrapy.Request(url=next_url, callback=self.parse)  # 提交Request并指定解析器
