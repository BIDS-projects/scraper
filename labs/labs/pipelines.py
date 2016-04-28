from utils.pipelines import AbstractMySQLPipeline
from labs import items
from scrapy.conf import settings
from etl import preprocessor

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


class PreprocessPipeline(object):
    """Pipeline that purifies raw data and saves to the database"""
    mongodb = preprocessor.MongoDBLoader()

    def process_item(self, item, spider):
        if isinstance(item, items.HTMLItem):
            self.mongodb.transform_and_load(item)
    
class MongoDBPipeline(object):
    """Pipeline for saving to a MongoDB database"""

    def __init__(self):
        from pymongo import MongoClient
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.html_collection = db[settings['MONGODB_HTML_COLLECTION']]

    def process_item(self, item, spider):
        if isinstance(item, items.HTMLItem):
            self.html_collection.replace_one({"url": item['url']},dict(item), upsert=True)
        else:
            raise DropItem("Dropping item: {0}".format(item))
