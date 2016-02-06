# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings

class AbstractMySQLPipeline(object):
    """Pipeline for saving to a MySQL database"""

    def __init__(self):
        """start connection to MySQL database"""
        from sqlalchemy import create_engine
        self.db = create_engine(
            'mysql+pymsql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'.format(settings))

    def process_item(self, item, spider):
        """Process an item"""
        raise NotImplementedError()

class AbstractMongoDBPipeline(object):
    """Pipeline for saving to a MongoDB database"""

    def __init__(self):
        from pymongo import MongoClient
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.link_collection = db[settings['MONGODB_LINK_COLLECTION']]
        self.text_collection = db[settings['MONGODB_TEXT_COLLECTION']]
        # self.paper_collection = db[settings['MONGODB_PAPER_COLLECTION']]

    def process_item(self, item, spider):
        raise NotImplementedError()
