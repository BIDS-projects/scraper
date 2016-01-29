# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.conf import settings
from items import LinkItem, TextItem

class MySQLPipeline(object):
    """Pipeline for saving to a MySQL database"""

    def __init__(self):
        """start connection to MySQL database"""

    def process_item(self, item, spider):
        """Process an item"""
        pass

class MongoDBPipeline(object):
    """Pipeline for saving to a MongoDB database"""

    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.link_collection = db[settings['MONGODB_LINK_COLLECTION']]
        self.text_collection = db[settings['MONGODB_TEXT_COLLECTION']]

    def process_item(self, item, spider):
        if isinstance(item, LinkItem):
            self.link_collection.insert_one(dict(item))
            return item
        elif isinstance(item, TextItem):
            self.text_collection.insert_one(dict(item))
            return item
        else:
            raise DropItem("Dropping item: {0}".format(item))

        #valid = True
        #for data in item:
            #if not data:
                #valid = False
                #raise DropItem("Missing {0}!".format(data))
        #if valid:
            #self.collection.insert(dict(item))
            #log.msg("Question added to MongoDB database!",
                    #level=log.DEBUG, spider=spider)
        #return item
        #for data in item:
            #if not data:
                #raise DropItem("Missing data!")
        #self.collection.update({'url': item['url']}, dict(item), upsert=True)
        #log.msg("Question added to MongoDB database!",
                #level=log.DEBUG, spider=spider)
        #return item
