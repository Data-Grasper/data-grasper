# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json


class WangyiproPipeline(object):
    def process_item(self, item, spider):
        print("类别：" + item["title"])
        print(item["content"])
        print("时间：" + item["time"])
        print("标签：" + item["tag"])
        print("url链接：" + item["url"])
        print("评论数" + item["comments"])
        return item


class AppPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        super().__init__()
        self.file = codecs.open('article.json', 'a', 'utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()
