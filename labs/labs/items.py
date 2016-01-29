from utils.items import BaseItem

class LinkItem(BaseItem):
    base_url = scrapy.Field()
    url = scrapy.Field()
    link = scrapy.Field()
    timestamp = scrapy.Field()

class TextItem(BaseItem):
    base_url = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    timestamp = scrapy.Field()
