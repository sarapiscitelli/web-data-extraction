from abc import ABC, abstractmethod
from typing import List

class WebPageParser(ABC):
    """Base interface for all web page parsers.
    It defines the methods that all the parsers must implement.
    TODO: Should be checked for image and pdf parsers, once implemented... 
    """

    def __init__(self, url: str, bytes_page: bytes) -> None:
        self.url = url
        self.bytes_page = bytes_page

    def get_url(self):
        return self.url

    @abstractmethod
    def get_title(self) -> str:
        pass

    @abstractmethod
    def get_content(self) -> str:
        pass

    @abstractmethod
    def get_next_urls(self) -> List[str]:
        pass

    @classmethod
    def get_parser(cls, url: str, bytes_page: bytes):
        if url.endswith(".pdf"):
            from .pdf_parsers import PDFParser
            
            return PDFParser(url=url, bytes_page=bytes_page)
        elif url.endswith(".jpg") or url.endswith(".png"):
            from .image_parsers import ImageParser
            
            return ImageParser(url=url, bytes_page=bytes_page)
        else:
            from .html_parsers import HTMLParser
            
            return HTMLParser(url=url, bytes_page=bytes_page)
