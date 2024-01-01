from .WebPageParser import WebPageParser

from typing import Dict, Iterable, List, Union, Set
from bs4 import BeautifulSoup
from trafilatura import extract


class HTMLParser(WebPageParser):
    """Generic parser for any html page.
    It just retrieves the text content of the page (no formatting is applied)
    """

    def __init__(self, url: str, bytes_page: bytes) -> None:
        super().__init__(url=url, bytes_page=bytes_page)
        self.parser = BeautifulSoup(bytes_page, "html.parser")
        self.domain_url: str = (
            url.split("//")[0] + "//" + url.split("//")[1].split("/")[0]
        )
        pass

    def get_title(self) -> str:
        """Returns the title of the html page ans set self.title to it."""
        title: Union[str, None] = self.parser.title
        if title is None:
            return ""
        return str(title.string)  # type: ignore

    def get_content(self) -> str:
        """Returns the text content of the html page and set self.content to it."""
        # Extract all content
        content: str = extract(self.bytes_page, include_links=False)
        return content

    def get_next_urls(self) -> List[str]:
        """Returns urls of additional pages in the html page and set self.urls_to_navigate to it."""
        urls_to_navigate: Set[str] = set()
        # Find all a elements
        a_elements = self.parser.find_all("a")
        for a in a_elements:
            if "href" in a.attrs:
                url_tmp: str = a.attrs.get("href", "")
                if url_tmp.startswith("http"):
                    urls_to_navigate.add(url_tmp)
                elif url_tmp.startswith("/"):
                    urls_to_navigate.add(self.domain_url + url_tmp)
                else:
                    urls_to_navigate.add(self.domain_url + "/" + url_tmp)
        return list(urls_to_navigate)


class TrustPilotParser:
    """This is a parser for specific for TrustPilot pages.
    Not implemented the general interface WebPageParser, as it will return a dictionary just suitable for TrustPilot web site.
    """
    
    def __init__(self, url: str, bytes_page: bytes) -> None:
        self.parser = BeautifulSoup(bytes_page, "html.parser")
        self.url = url
        self.item = None
        pass
    
    def get_item(self) -> Iterable[Dict[str, str]]:
        """The retuned dictionary is bonded to the scrapy_project.web_extraction.items.TrustPilotItem.

        Returns:
            None: if no reviews are found in the page.
            A dictionary with the following keys:
                'id': the id of the review,
                'title': the title of the review,
                'reviewBody': the text content of the review,
                'reviewRating': the rating of the review (from 1 to 5),
                'datePublished': the date of the review (in string format),
                'language': the language of the review (in string format).
        """
        script_tags = self.parser.find_all("script", {"type": "application/ld+json"})
        for script in script_tags:
            script_item = eval(script.get_text())
            if '@graph' not in script_item:
                continue
            for item in script_item['@graph']:
                if not isinstance(item, dict):
                    continue
                if item['@type'] == 'Review':
                    yield {
                        'id': item['@id'],
                        'title': item['headline'],
                        'reviewBody': item['reviewBody'],
                        'reviewRating': item['reviewRating']['ratingValue'],
                        'datePublished': item['datePublished'],
                        'language': item['inLanguage']
                    }
