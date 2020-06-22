import sys
import os

from scrapy_APP.settings import PROJECT_ROOT
from scrapy.cmdline import execute

sys.path.append(PROJECT_ROOT)

# try:
#     spider_name = sys.argv[1]
#     execute(["scrapy", "crawl", spider_name])
# except Exception as e:
#     if isinstance(e, IndexError):
#         e = "Too few or too many args entered."
#     print("\033[1;31;40mAn ERROR happened:\033[0m", e)
#     print("Please assign a correct spider name in dir:", os.path.join(PROJECT_ROOT, "spiders"))
spider_name = sys.argv[1]
print("client launched.")
execute(["scrapy", "crawl", spider_name])