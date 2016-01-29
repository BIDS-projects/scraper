import scrapy


class LinkItem(scrapy.Item):
    base_url = scrapy.Field()
    url = scrapy.Field()
    link = scrapy.Field()
    timestamp = scrapy.Field()

class TextItem(scrapy.Item):
    base_url = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    timestamp = scrapy.Field()
