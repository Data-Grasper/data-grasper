from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait

from scrapy_APP.settings import DRIVER_FILE
from scrapy_APP.utils.ClassUtils import synchronized


class Extractor:
    """
    解析动态站点的工具类基类。
    如果要进行动态站点解析，请另开一个py文件并像 DesktopLinkExtractor 一样继承该类并实现解析方法。
    """
    timeout = 5
    _instance = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        """
        单例模式
        """
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        """
        以无头模式运行chrome
        """
        chrome_opt = ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_opt.add_experimental_option("prefs", prefs)
        chrome_opt.add_argument('headless')
        chrome_opt.add_argument('--disable-gpu')
        self.driver = Chrome(executable_path=DRIVER_FILE, chrome_options=chrome_opt)

    def __del__(self):
        """
        关闭浏览器
        """
        self.driver.quit()

    def wait_an_element_by_xpath(self, xpath):
        """阻塞获取元素"""
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                lambda driver: driver.find_element_by_xpath(xpath)
            )
            return element
        except Exception as e:
            print("ERROR:", e)
            return None


class DesktopLinkExtractor(Extractor):
    def extract_download_link(self, detail_url):
        """图片详情页面获取下载url"""
        self.driver.get(detail_url)
        downloadObj = self.wait_an_element_by_xpath("//div[@class='desktop']/a")
        if not downloadObj:
            return None
        link = downloadObj.get_attribute('href')

        self.driver.get(link)
        imgObj = self.wait_an_element_by_xpath("//img")
        if not imgObj:
            return None
        src = imgObj.get_attribute('src')
        return src


if __name__ == '__main__':
    extractor = DesktopLinkExtractor()
    # ext1 = DesktopLinkExtractor()
    # print(id(extractor) == id(ext1))
    # link = extractor.extract_download_link("http://simpledesktops.com/browse/desktops/2020/apr/08/tardis/")
    # print(link)
