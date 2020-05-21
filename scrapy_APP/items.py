# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyiproItem(scrapy.Item):
    title = scrapy.Field()
    head = scrapy.Field()
    tag = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    comments = scrapy.Field()

    education = scrapy.Field()
    IT = scrapy.Field()
    animals = scrapy.Field()
    Medicine = scrapy.Field()
    famous = scrapy.Field()
    poetry = scrapy.Field()
    Sensitives = scrapy.Field()
    car_brand_part = scrapy.Field()
    law = scrapy.Field()
    financial = scrapy.Field()
    food = scrapy.Field()

    positives = scrapy.Field()
    negatives = scrapy.Field()

    def get_sql(self):
        insert_sql = "insert into wangyiitem (tag, head, content, time, comments, url, education, IT, animals, Medicine, famous, poetry, Sensitives, car_brand_part,law, financial, food, positives, negatives) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        # ,education,IT,animals,Medicine,famous,poetry,Sensitive,car_brand_part,law,financial,food   ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        params = []
        params.append(self.get('tag', ''))
        params.append(self.get('head', ''))
        params.append(self.get('content', ''))
        params.append(self.get('time', ''))
        params.append(self.get('comments', ''))
        params.append(self.get('url', ''))
        params.append(self.get('education', ''))
        params.append(self.get('IT', ''))
        params.append(self.get('animals', ''))
        params.append(self.get('Medicine', ''))
        params.append(self.get('famous', ''))
        params.append(self.get('poetry', ''))
        params.append(self.get('Sensitives', ''))
        params.append(self.get('car_brand_part', ''))
        params.append(self.get('law', ''))
        params.append(self.get('financial', ''))
        params.append(self.get('food', ''))
        params.append(self.get('positives', ''))
        params.append(self.get('negatives', ''))
        return insert_sql, params


    pass

class TianyaItem(scrapy.Item):
    item = scrapy.Field()
    item_name = scrapy.Field()
    id = scrapy.Field()
    count = scrapy.Field()
    top_count = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
    content = scrapy.Field()

    def get_sql(self):
        insert_sql = "insert into tianyaitem (id, item,item_name,count_data,top_count," \
                     "title,url,author_id,author_name,content) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        params = []
        params.append(self.get('id', ''))
        params.append(self.get('item', ''))
        params.append(self.get('item_name', ''))
        params.append(self.get('count', ''))
        params.append(self.get('top_count', ''))
        params.append(self.get('title', ''))
        params.append(self.get('url', ''))
        params.append(self.get('author_id', ''))
        params.append(self.get('author_name', ''))
        params.append(self.get('content', ''))
        return insert_sql, params

class TianyaDict(scrapy.Item):
    id = scrapy.Field()
    education = scrapy.Field()
    IT = scrapy.Field()
    animals = scrapy.Field()
    Medicine = scrapy.Field()
    famous = scrapy.Field()
    poetry = scrapy.Field()
    Sensitives = scrapy.Field()
    car_brand_part = scrapy.Field()
    law = scrapy.Field()
    financial = scrapy.Field()
    food = scrapy.Field()

    positives = scrapy.Field()
    negatives = scrapy.Field()

    def get_sql(self):
        insert_sql ="insert into tianyaDict (id, education, IT, animals, Medicine," \
                    " famous, poetry, Sensitives, car_brand_part,law, financial, food, positives, negatives) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        params = []
        params.append(self.get('id', ''))
        params.append(self.get('education', ''))
        params.append(self.get('IT', ''))
        params.append(self.get('animals', ''))
        params.append(self.get('Medicine', ''))
        params.append(self.get('famous', ''))
        params.append(self.get('poetry', ''))
        params.append(self.get('Sensitives', ''))
        params.append(self.get('car_brand_part', ''))
        params.append(self.get('law', ''))
        params.append(self.get('financial', ''))
        params.append(self.get('food', ''))
        params.append(self.get('positives', ''))
        params.append(self.get('negatives', ''))
        return insert_sql, params


class commentSensitive(scrapy.Item):
    id = scrapy.Field()
    item_id = scrapy.Field()
    comment = scrapy.Field()

    positives = scrapy.Field()
    negatives = scrapy.Field()

    def get_sql(self):
        insert_sql ="insert into tianyaSensitive (id, item_id,comment, positives, negatives) values(%s, %s,%s, %s, %s);"
        params = []
        params.append(self.get('id', ''))
        params.append(self.get('item_id', ''))
        params.append(self.get('comment', ''))
        params.append(self.get('positives', ''))
        params.append(self.get('negatives', ''))
        return insert_sql, params

class DesktopItem(scrapy.Item):
    src = scrapy.Field()


class DemoItem(scrapy.Item):
    url = scrapy.Field()
