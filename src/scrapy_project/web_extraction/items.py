# models definition for scraped items
# Documentatio: https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class GeneralWebItem(Item):
    """It is the item class for the generic spider. 
    It doesn't format the data, it just retrieve the text content of the web page."""
    url = Field()
    content = Field()
    title = Field()
    pass

class TrustPilotItem(Item):
    """It is the item class for the trustpilot spider. 
    It is specific for the trustpilot website."""
    id=Field()
    title=Field()
    reviewBody=Field()
    reviewRating=Field()
    datePublished=Field()
    language=Field()
    pass