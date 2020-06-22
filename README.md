# spider-distributed
基于redis的分布式增量爬虫
[redis和scrapy-redis的笔记](redis-note.md)
## 被gitignore的文件
因为有一些不便于上传GitHub的信息，所以需要手动创建这些文件并写入数据。列举如下：
1. `scrapy_APP/config.py`
    + redis_url: redis服务器的标准url
## 环境配置：
python3.6，需要pip安装的包有：
+ scrapy
+ redis
+ mmh3
+ selenium
+ pillow

## 用法
1. 按照scrapy-redis的用法创建爬虫
2. 往redis中lpush start urls开始运行。start url格式：http url字符串
3. 往redis中rpush new urls进行增量。new urls格式：当前是(url, priority, callback function name)，可以后续按照需求进行调整。

## 笔记
[scrapy-redis & redis](redis-note.md)

[scrapy-advancd](scrapy-advance.md)

[增量抓取](more.md)