from abc import ABC# 一些进阶笔记
## 为每个爬虫设置自定义的setting项
在spider类中，加入属性`custom_settings`即可
```python
from scrapy import Spider
class MySpider(Spider):
    custom_settings = {
        "COOKIE_ENABLED":True
    }
```
## 爬虫暂停
`scrapy crawl <name> -s JOB_DIR='some_dir'`

或者`custom_settings`中设置工作目录。

设置工作目录后，爬虫收到`ctrl+C`信号后会停止继续请求，完成已经发生的请求的下载并保存当前状态到工作目录。

下一次再从同一个工作目录启动同一个爬虫，就能继续进行爬取。

注意：每个爬虫每次启动的目录都不能一样

## Scrapy Telnet
Scrapy附带一个内置的telnet控制台，用于检查和控制Scrapy运行过程。telnet控制台只是一个运行在scrappy进程内部的常规python shell，因此您可以从中做任何事情。

telnet控制台侦听中定义的TCP端口 `TELNETCONSOLE_PORT` 设置，默认为 6023 . 要访问控制台，您需要键入：

`telnet localhost 6023`

默认用户名为 scrapy 密码是自动生成的。自动生成的密码可以在日志中看到，如下例所示：

2018-10-16 14:35:21 [scrapy.extensions.telnet] INFO: Telnet Password: 16f92501e8a59326

默认用户名和密码可以被设置覆盖 `TELNETCONSOLE_USERNAME` 和 `TELNETCONSOLE_PASSWORD` .

## 数据收集
### 通过stats对象进行数据的管理

设置统计值：
stats.set_value('hostname', socket.gethostname()

增量统计值：
stats.inc_value('custom_count')

仅当大于上一个值时设置stat值：：
stats.max_value('max_items_scraped', value)

仅当低于上一个时设置stat值：：
stats.min_value('min_free_memory_percent', value)

获取统计值：
stats.get_value('custom_count')
1

获取所有统计数据：
stats.get_stats()
{'custom_count': 1, 'start_time': datetime.datetime(2009, 7, 14, 21, 47, 28, 977139)}

### 如何获取stats？
stats对象会被IoC注入到每个Spider中，通过self.crawler.stats访问

## Scrapy信号
### 发送信号的主体：
1. scrapy engine
2. scrapy downloader
3. spider

### 信号的类型
所有的信号都在
`scrapy.signals.<signal_name>`
详情请查看官方文档

一些信号支持返回 Twisted deferreds ，一些不支持。
