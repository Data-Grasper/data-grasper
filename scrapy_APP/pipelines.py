# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from MySQLdb.cursors import DictCursor
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline
from scrapy_APP.config import MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER, MYSQL_DB, MYSQL_CHARSET

class WangyiproPipeline(object):
    def process_item(self, item, spider):

        print("类别：" + item["title"])
        print("标题：" + item["head"])
        print(item["content"])
        print("时间：" + item["time"])
        print("标签：" + item["tag"])
        print("url链接：" + item["url"])
        print("评论数" + item["comments"])
        print(item["education"])
        print(item["IT"])
        print(item["animals"])
        print(item["Medicine"])
        print(item["famous"])
        print(item["poetry"])
        print(item["Sensitives"])
        print(item["car_brand_part"])
        print(item["law"])
        print(item["financial"])
        print(item["food"])
        print(item["positives"])
        print(item["negatives"])
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

class ArticleImagesPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            image_file_path = ''
            for ok, value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path
        return item

class MysqlTwistedPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            passwd=settings['MYSQL_PASSWORD'],
            user=settings['MYSQL_USER'],
            db=settings['MYSQL_DB'],
            charset=settings['MYSQL_CHARSET'],
            cursorclass=DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def __init__(self, dbpool):
        super().__init__()
        self.dbpool = dbpool

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)  # runInteraction(function, **params),自动注入cursor
        query.addErrback(self.handle_error)  # 自动注入failure

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_sql()
        cursor.execute(insert_sql, tuple(params))