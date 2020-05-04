# 增量抓取
使用scrapy-redis进行增量抓取

## 基本思想
请求队列使用优先队列，每隔一段时间往redis中放高优先级的增量页面

## 实现过程
1. 在settings中设置`SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.PriorityQueue"`

2. 重写`scrapy_redis.scheduler`的`enqueue_requests`方法：
```python
import redis
import json
import scrapy
rd = redis.Redis("your_url", decode_responses=True)
list_name = "url_list_name" 
# 自定义的一个Redis控制队列。list。
# 用第三方脚本往这个队列中放url，在enqueue的时候先把这个队列中的url放到爬虫的Request队列中
# 再继续原来的enqueue_requests操作。

def enqueue_requests(self, request):
    while rd.llen(list_name):
        data = json.loads(rd.lpop(list_name))
        # 队列中每一项是我们自己放的元组，为(value, score)。取出这个队列
        req = scrapy.Request(url=data[0], dont_filter=False, callback=self.spider.parsefunc, priority=data[1])
        self.queue.push(req)
        
    # ... 原来的代码
```

3. 脚本中往控制队列中放url。队列中放的tuple可以更加复杂，比如(url, score, callback, dont_filter)之类的。通过字符串处理，可以达到控制的效果
```python
# in script
import json
import redis

rd = redis.Redis("your_url", decode_responses=True)
demo = ("http://www.baidu.com", 10, "parse_demo")
rd.rpush("your_list", json.dumps(demo))

# in scheduler
callback_func = getattr(self.spider, data[2]) # 获得回调函数

```
