# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from db import MySQL, MySQLConfig

class AbstractMySQLPipeline(object):
    """Pipeline for saving to a MySQL database"""

    def __init__(self):
        """start connection to MySQL database"""
        # Initialize database connections
        self.mysql = MySQL(config=MySQLConfig)

    def process_item(self, item, spider):
        """Process an item"""
        raise NotImplementedError()

class AbstractMongoDBPipeline(object):
    """Pipeline for saving to a MongoDB database"""

    def __init__(self):
        # Initialize database connections
        self.mongo = Mongo(config=MongoConfig)

    def process_item(self, item, spider):
        raise NotImplementedError()
