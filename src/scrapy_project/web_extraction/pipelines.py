# pipelines definition for scraped items
# Documentatio: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem

class WebExtractionPipeline(object):
    """Pipeline definition for scraped items"""

    def open_spider(self, spider):
        """called when the spider is opened."""
        # save the id of the items already collected in the current session to avoid duplicates
        self.collected_items: set = set()

    def close_spider(self, spider):
        """called when the spider is closed"""
        self.collected_items.clear()

    def process_item(self, item, spider):
        """
        Method is called for every item pipeline component 
        Returns:
            an item object from the items defined. 
                raise a DropItem exception to discard the item.
        """
        if spider.name == "generic_spider":
            text_field = "content"
            id_field = "url"
        elif spider.name == "trustpilot_spider":
            text_field = "reviewBody"
            id_field = "id"
        if text_field not in item or item[text_field] is None or item[text_field] == "":
            raise DropItem(f"Content is empty for item: {item}")
        if item[id_field] in self.collected_items:
            raise DropItem(f"Item already collected: {item}")
        self.collected_items.add(item[id_field])
        print(json.dumps(dict(item)))
        return item
