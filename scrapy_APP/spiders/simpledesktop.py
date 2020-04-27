from scrapy_APP.scrapy_redis.spiders import RedisSpider


class SimpleDesktopSpider(RedisSpider):
    name = 'simple_desktop'
    redis_key = 'simple_desktop:start_urls'
    allowed_domains = ['http://simpledesktops.com/']


    def parse(self, response):
        # do stuff
        image_details = response.xpath("//div[@class='desktop']/a/@href").extract()
        print(image_details)
        pass
