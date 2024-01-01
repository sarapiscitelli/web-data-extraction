from .WebPageParser import WebPageParser

from typing import List


class PDFParser(WebPageParser):

    def __init__(self, url: str, bytes_page: bytes) -> None:
        self.url = url
        self.bytes_page = bytes_page

    def get_title(self) -> str:
        pass

    def get_content(self) -> str:
        pass

    def get_next_urls(self) -> List[str]:
        pass