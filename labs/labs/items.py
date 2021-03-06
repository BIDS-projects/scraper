from utils.items import BaseItem
import scrapy

class HTMLItem(scrapy.Item):
    """Raw HTML item"""
    url = scrapy.Field()
    body = scrapy.Field()
    request = scrapy.Field()
    links = scrapy.Field()

class LinkItem(scrapy.Item):
    """Many to Many item for linking"""
    base_url = scrapy.Field()
    src_url = scrapy.Field()
    dst_url = scrapy.Field()
    timestamp = scrapy.Field()

class ExternalLinkItem(LinkItem):
    non_filtered_url = scrapy.Field()

class InternalLinkItem(LinkItem):
    tier = scrapy.Field()

class TextItem(scrapy.Item):
    base_url = scrapy.Field()
    src_url = scrapy.Field()
    text = scrapy.Field()
    timestamp = scrapy.Field()
    tier = scrapy.Field()

class PaperItem(BaseItem):
    url = scrapy.Field()
    researcher = scrapy.Field()
    text = scrapy.Field()
    timestamp = scrapy.Field()
    department = scrapy.Field()

class JenkinsItem(scrapy.Item):
    base_url = scrapy.Field()
    src_url = scrapy.Field()
    text = scrapy.Field()
    timestamp = scrapy.Field()
