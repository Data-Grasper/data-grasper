import scrapy
from selenium import webdriver
from scrapy_APP.scrapy_redis.spiders import RedisSpider
from scrapy_APP.utils.domaindict import *
from scrapy_APP.items import TianyaItem,TianyaDict
class TianyaSpider(RedisSpider):
    name = 'tianya'
    allowed_domains = None
    redis_key = 'tianya:start_urls'

    #start_urls = ['https://www.tianya.cn']

    def __init__(self):
        # 实例化一个浏览器，只需要执行一次
        self.bro = webdriver.Chrome()

    def parse(self, response):
        url = "https://bbs.tianya.cn/api?method=bbs.ice.getHotArticleList&params.pageSize=40&params.pageNum=1&var=apiData"
        yield scrapy.Request(
                url=url,
                callback=self.parseSummary
            )



    def parseSummary(self, response):
        # 解析每个类页面中的新闻链接和相关信息
        context = (response.text)[14:]
        context = json.loads(context)["data"]["rows"]
        for item in context:
            itemData = TianyaItem()
            list_keys = ["item","item_name","id","count","top_count","title",\
                    "url","author_id","author_name","content"]
            for key in list_keys:
                itemData[key] = item[key]
            yield itemData

            itemDict = TianyaDict()
            sentence = itemDict["content"]
            sentence = sentenceProcess(sentence)
            domainDicts_definate = getSentenceDomain(domainDicts, sentence)
            sensitiveDicts_definate = getSentenceSensitive(sensitiveDicts, sentence)
            itemDict["id"] = item["id"]
            itemDict["education"] = domainDicts_definate["教育"]
            itemDict["IT"] = domainDicts_definate["IT"]
            itemDict["animals"] = domainDicts_definate["动物"]
            itemDict["Medicine"] = domainDicts_definate["医学"]
            itemDict["famous"] = domainDicts_definate["历史名人"]
            itemDict["poetry"] = domainDicts_definate["古诗"]
            itemDict["Sensitives"] = domainDicts_definate["敏感词"]
            itemDict["car_brand_part"] = domainDicts_definate["汽车品牌、零件"]
            itemDict["law"] = domainDicts_definate["法律"]
            itemDict["financial"] = domainDicts_definate["财经"]
            itemDict["food"] = domainDicts_definate["食物"]
            itemDict["positives"] = sensitiveDicts_definate["positive"]
            itemDict["negatives"] = sensitiveDicts_definate["negative"]



        '''
        for i in context:
            item = TianyaItem()
            for key in i.keys():
                if key != "pics":
                    item[key] = i[key]

            url = "http://bbs.tianya.cn/post-develop-" + str(i["artId"])+"-1.shtml"
            print(url)
            yield scrapy.Request(url=url, callback=self.getContent, meta={"item": item}, dont_filter=True)
        '''

    def getContent(self, response):
        # 解析新闻文本内容
        item = response.meta.get("item")


        
    def closed(self, spider):
        # 实现父类方法，爬虫结束时调用
        print("爬虫结束")
        self.bro.quit()
