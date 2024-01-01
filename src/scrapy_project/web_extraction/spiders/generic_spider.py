import scrapy
import fire

from typing import List
from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent

from scrapy.settings import Settings
from scrapy_project.web_extraction.parsers.WebPageParser import WebPageParser
from scrapy_project.web_extraction.items import GeneralWebItem


class GenericSpider(scrapy.Spider):
    # identify the spider
    name = "generic_spider"

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.urls: List[str] = []
        self.max_next_pages = 0
        self.count_next_pages = self.max_next_pages

    def set_urls(self, urls: List[str]):
        self.urls = urls

    def set_max_next_pages(self, max_next_pages: int = 0):
        self.max_next_pages = max_next_pages
        self.count_next_pages = max_next_pages
        # if max_next_pages is set to 0, the navigation is disabled
        # this counter is used to stop the navigation

    def start_requests(self):
        ua = UserAgent()
        for url in self.urls:
            headers = {"User-Agent": str(ua.random)}
            yield scrapy.Request(url=url, headers=headers, callback=self.parse_page)
            # reset for next url
            self.count_next_pages = self.max_next_pages
    
    def parse_page(self, response):
        """Define how to parse the retrieved page in the response."""
        
        def parse_additional_urls(page_scraper):
            """Look for additional urls (the next pages or linked url) in the page and parse them recursively."""
            if self.count_next_pages > 0:
                other_urls = page_scraper.get_next_urls()
                for url in other_urls:
                    # Keep only the urls of the same domain
                    if url.startswith(page_scraper.domain_url):
                        next_page = response.urljoin(url)
                        self.count_next_pages -= 1
                        if self.count_next_pages == 0:
                            return
                        yield scrapy.Request(next_page, callback=self.parse_page)

        page_scraper = WebPageParser.get_parser(url=response.url, bytes_page=response.body)
        # create output item
        item = GeneralWebItem()
        item["content"] = page_scraper.get_content()
        item["title"] = page_scraper.get_title()
        item["url"] = page_scraper.get_url()
        yield item
        if self.count_next_pages == 0:
            return
        # recursive call to navigate through next pages (if enabled)
        yield from parse_additional_urls(page_scraper)


def start_spider(urls_to_query: List[str],
                 max_next_pages: int = 10) -> List[GeneralWebItem]:
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
    process.crawl(GenericSpider)
    # set the parameters for this crawler process (generic_spider)
    for crawl_spider in process.crawlers:
        if crawl_spider.spider.name == "generic_spider":
            crawl_spider.spider.set_urls(urls_to_query)
            crawl_spider.spider.set_max_next_pages(max_next_pages)

    process.start()  # the script will block here until the crawling is finished
    # the results are printed in the console, so we need to retrieve them from the main process
    return None


if __name__ == "__main__":
    fire.Fire(start_spider)