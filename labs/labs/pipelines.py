from utils.pipelines import AbstractMySQLPipeline
from labs.items import *
from scrapy.conf import settings

class MySQLPipeline(AbstractMySQLPipeline):

    def process_item(self, item, spider):
        pass
        # if isinstance(item, LinkItem):
        #     Link(
        #         url=item.url,
        #
        # elif isinstance(item, TextItem):
        #
        # else:
        #     raise DropItem("Dropping item: {0}".format(item))


class MongoDBPipeline(object):
    """Pipeline for saving to a MongoDB database"""

    def __init__(self):
        from pymongo import MongoClient
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.external_link_collection = db[settings['MONGODB_EXTERNAL_LINK_COLLECTION']]
        self.internal_link_collection = db[settings['MONGODB_INTERNAL_LINK_COLLECTION']]
        self.text_collection = db[settings['MONGODB_TEXT_COLLECTION']]
        self.html_collection = db[settings['MONGODB_HTML_COLLECTION']]
        # self.paper_collection = db[settings['MONGODB_PAPER_COLLECTION']]

    def process_item(self, item, spider):
        if isinstance(item, ExternalLinkItem):
            self.external_link_collection.replace_one(dict(item), upsert=True)
            return item
        # elif isinstance(item, InternalLinkItem):
        #     self.internal_link_collection.replace_one(dict(item), upsert=True)
        #     return item
        # elif isinstance(item, TextItem):
        #     self.text_collection.replace_one(dict(item), upsert=True)
        #     return item
        elif isinstance(item, HTMLItem):
            self.html_collection.replace_one({"url": item['url']},dict(item), upsert=True)
            return item
        # elif isinstance(item, PaperItem):
        #     pass
            #self.paper_collection.replace_one(dict(item), upsert=True)
            #return item
        else:
            raise DropItem("Dropping item: {0}".format(item))
