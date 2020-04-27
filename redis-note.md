# Redis基本用法

## 字符串命令

+ set mykey value
+ get mykey
+ getrange mykey start end # 字符串切片，仅针对string类型
+ incr/decr mykey # 值+1/-1，仅针对int类型
+ append mykey afterfix # 字符串添加后缀

## 哈希命令

+ hset key field value
+ hget key field
+ hgetall key # 获取所有的field和value，单数是field，双数是value
+ hexists key field
+ hdel key field [field ...]
+ hkeys key
+ hvals key

## 列表命令

+ lpush/rpush list val [val ...] # 按顺序左右push进列表，若为空则创建
+ lrange list start end # 列表切片
+ blpop/brpop key [key ...] timeout # 从列表左右阻塞删除一个元素，如果为空会等待timeout秒
+ lpop/rpop key [key ...] # 非阻塞删除一个元素
+ llen key
+ lindex key idx # 取元素

## 集合命令

+ sadd key val # 成功返回1，否则返回0
+ scard key # 集合内元素数量
+ sdiff key key2 key3... # key1 - key2 - key3 差集
+ sinter key1 key2 # 交集
+ spop key # 随机删除一个元素，并返回那个删除的元素
+ srandmember key number # 随机获取number个元素
+ smembers key # 获取set内所有元素

## 有序集合命令

+ zadd key score val [score val ...] # 添加元素和分数，重复val会覆盖分数
+ zrangebyscore key min max # 获取分数在某范围内的所有元素
+ zcount key min max # 分数范围内的元素数量

# 使用Scrapy-redis编写分布式爬虫
## 配置
```python
# settings.py
# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Store scraped item in redis for post-processing.
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}
```

## 定义爬虫
```python
from scrapy_APP.scrapy_redis.spiders import RedisSpider

class MySpider(RedisSpider):
    name = 'myspider'

    def parse(self, response):
        # do stuff
        pass
```

## 启动爬虫
+ run the spider:

`scrapy runspider myspider.py`

+ push urls to redis:

`redis-cli lpush myspider:start_urls http://google.com`