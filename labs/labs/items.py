from utils.items import BaseItem
import scrapy


class LinkItem(BaseItem):
    base_url = scrapy.Field()
    url = scrapy.Field()
    dst_url = scrapy.Field()
    timestamp = scrapy.Field()

class ExternalLinkItem(LinkItem):
    pass

class InternalLinkItem(LinkItem):
    tier = scrapy.Field()

class TextItem(BaseItem):
    base_url = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    timestamp = scrapy.Field()

class PaperItem(BaseItem):
    url = scrapy.Field()
    researcher = scrapy.Field()
    text = scrapy.Field()
    timestamp = scrapy.Field()

class JenkinsItem(BaseItem):
    base_url = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    timestamp = scrapy.Field()
