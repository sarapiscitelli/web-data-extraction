import scrapy
import fire

from typing import Dict, List
from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent

from scrapy.settings import Settings
from scrapy_project.web_extraction.items import TrustPilotItem
from scrapy_project.web_extraction.parsers.html_parsers import TrustPilotParser



class TrustpilotSpider(scrapy.Spider):
    # identify the spider
    name = "trustpilot_spider"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.domain_url = "https://www.trustpilot.com/review/"
        self.urls = []
        self.first_page = None

    def set_url(self, suffix: str, language: str = "all"):
        self.domain_url = f"{self.domain_url}{suffix}?languages={language}"

    def set_max_next_pages(self, max_next_pages: int = 0):
        self.urls = [f"{self.domain_url}&page={i+1}" for i in range(0, max_next_pages+1)]

    def start_requests(self):
        ua = UserAgent()
        for url in self.urls:
            headers = {"User-Agent": str(ua.random)}
            yield scrapy.Request(url=url, headers=headers, callback=self.parse_page)
    
    def parse_page(self, response):
        """Define how to parse the retrieved page in the response."""
        bytes_page = response.body
        parser = TrustPilotParser(url=response.url, bytes_page=bytes_page)
        for item in parser.get_item():
            yield TrustPilotItem(**item)

def start_spider(suffix: str,
                 language: str = "all",
                 max_next_pages: int = 0) -> List[TrustPilotItem]:
    """Main function to start the spider.

    Args:
        urls_to_query (List[str]): urls to query
        max_next_pages (int): maximum number of next pages to navigate. 
            If set to 0 (default), the navigation is disabled.
    """
    from scrapy_project.web_extraction import settings as my_settings

    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(TrustpilotSpider)
    # set the parameters for this crawler process (trustpilot_spider)
    for crawl_spider in process.crawlers:
        if crawl_spider.spider.name == "trustpilot_spider":
            crawl_spider.spider.set_url(suffix, language)
            crawl_spider.spider.set_max_next_pages(max_next_pages)

    process.start()  # the script will block here until the crawling is finished
    # the results are printed in the console, so we need to retrieve them from the main process
    return None

if __name__ == "__main__":
    fire.Fire(start_spider)
