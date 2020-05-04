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
+ zrange key min max # 按照下标取值，-1是最后一个。zset根据score增序排列

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

## 创建项目(使用bloomfilter算法进行url去重)
1. 克隆`scrapy-redis`项目，将核心包`scrapy_redis`复制到scrapy项目下
2. 下载`utils.bloomfilter.py`文件
3. `scrapy_redis.dupefilter.py`中导入`bloomfilter.py`中的`conn`, `PyBloomFilter`
4. `scrapy_redis.dupefilter.py`中`__init__`方法中进行实例化：`self.bf = PyBloomFilter(conn=conn, key=key)`
5. `scrapy_redis.dupefilter.py`中重写`request_seen`方法
    ```python
    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if self.bf.is_exist(fp):
            return True
        else:
            self.bf.add(fp)
            return False
    ```
   
## 常见问题
+ Q: (error) MISCONF Redis is configured to save RDB snapshots, but is currently not able to persist on disk. Commands that may modify the data set are disabled. Please
check Redis logs for details about the error.
+ A: 在redis-cli中`config set stop-writes-on-bgsave-error no`
