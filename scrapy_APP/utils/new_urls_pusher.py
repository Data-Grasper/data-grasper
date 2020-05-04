import redis
import json
from scrapy_APP.settings import REDIS_URL

rd = redis.from_url(REDIS_URL)
demo = ("http://localhost/100", 10, "parse")
rd.rpush("demo:new_urls", json.dumps(demo))
