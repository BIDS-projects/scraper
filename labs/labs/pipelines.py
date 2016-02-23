from utils.pipelines import AbstractMySQLPipeline
from labs.items import *
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from db.models_mysql import HTML, Link

class MySQLPipeline(AbstractMySQLPipeline):

    def process_item(self, item, spider):
        """Save data to database"""
        item = spider.html # hack
        if isinstance(item, HTMLItem):
            source = HTML.get_or_create(url=item['url']).update(
                domain=spider.domain(item['url']),
                url=item['url'],
                # body=item['body'],
                request=item['request']).save()
            for link in item['links']:
                target = HTML.get_or_create(url=link.url).save()
                Link(from_html=source.id,
                    to_html=target.id).save()
            return item
        else:
            raise DropItem("Dropping item: {0}".format(item))

class MongoDBPipeline(object):
    """Pipeline for saving to a MongoDB database, with given models"""

    def process_item(self, item, spider):
        """Save data to database"""
        pass


class MongoDBPipelineFlexible(object):
    """Pipeline for saving to a MongoDB database, with flexible format"""

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
        # self.paper_collection = db[settings['MONGODB_PAPER_COLLECTION']]

    def process_item(self, item, spider):
        if isinstance(item, ExternalLinkItem):
            self.external_link_collection.insert_one(dict(item))
            return item
        elif isinstance(item, InternalLinkItem):
            self.internal_link_collection.insert_one(dict(item))
            return item
        elif isinstance(item, TextItem):
            self.text_collection.insert_one(dict(item))
            return item
        elif isinstance(item, PaperItem):
            pass
            #self.paper_collection.insert_one(dict(item))
            #return item
        else:
            raise DropItem("Dropping item: {0}".format(item))
