import scrapy
from selenium import webdriver
from scrapy_APP.items import WangyiproItem
from scrapy_APP.scrapy_redis.spiders import RedisSpider
from scrapy_APP.utils.domaindict import *
class WangyiSpider(RedisSpider):
    name = 'wangyi'
    allowed_domains = ['news.163.com']
    redis_key = 'wangyi:start_urls'

    # start_urls = ['https://news.163.com/']

    def __init__(self):
        # 实例化一个浏览器，只需要执行一次
        self.bro = webdriver.Chrome(executable_path='chromedriver.exe')

    def parse(self, response):
        lis = response.xpath("//div[@class='ns_area list']/ul/li")
        indexs = [3, 4, 6, 7]
        li_list = []
        for index in indexs:
            li_list.append(lis[index])
        # 获取四个板块中的链接和文字标题
        for li in li_list:
            url = li.xpath("./a/@href").extract_first()
            title = li.xpath("./a/text()").extract_first()
            # 对每个板块对应的url发起请求，获取页面数据(标题，缩略图，关键字，发布时间，url，评论数)
            yield scrapy.Request(url=url, callback=self.parseSecond, meta={"title": title}, dont_filter=True)

    def parseSecond(self, response):
        # 解析每个类页面中的新闻链接和相关信息
        div_list = response.xpath('//div[@class="ndi_main"]/div')
        for div in div_list:
            head = div.xpath(".//div[@class='news_title']/h3/a/text()").extract_first()
            url = div.xpath(".//div[@class='news_title']/h3/a/@href").extract_first()
            img_url = div.xpath("./a/img/@src").extract_first()
            tag = ",".join(div.xpath(".//div[@class='keywords']//a/text()").extract())
            time = div.xpath(".//div[@class='news_tag']/span/text()").extract_first()
            comments = div.xpath(".//div[@class='post_recommend_tie_wrap']/span/text()").extract_first()
            # 实例化item对象，将解析到的值存储到item中
            item = WangyiproItem()
            item["head"] = head
            item["url"] = url
            item["img_url"] = img_url
            item["tag"] = tag
            item["title"] = response.meta["title"]
            item["time"] = time
            item["comments"] = comments
            yield scrapy.Request(url=url, callback=self.getContent, meta={"item": item}, dont_filter=True)

    def getContent(self, response):
        # 解析新闻文本内容
        item = response.meta.get("item")
        content_list = response.xpath("//div[@class='post_text']/p/text()").extract()
        content = "\n".join(content_list)
        item["content"] = content
        yield item

        domainDicts = getDomainDicts()
        sensitiveDicts = getSensitiveDicts()
        sentence =content
        sentence = sentenceProcess(sentence)
        domainDicts_definate = getSentenceDomain(domainDicts, sentence)
        sensitiveDicts_definate = getSentenceSensitive(sensitiveDicts, sentence)
        print(domainDicts_definate)
        print(sensitiveDicts_definate)

    def closed(self, spider):
        # 实现父类方法，爬虫结束时调用
        print("爬虫结束")
        self.bro.quit()
