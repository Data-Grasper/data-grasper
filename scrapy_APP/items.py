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


class DesktopItem(scrapy.Item):
    src = scrapy.Field()


class DemoItem(scrapy.Item):
    url = scrapy.Field()
    like1 = scrapy.Field()
    like2 = scrapy.Field()

