from utils.pipelines import AbstractMongoDBPipeline, AbstractMySQLPipeline
from .models import Domain, Link, Text
from urllib.parse import url_parse

class MySQLPipeline(AbstractMySQLPipeline):

    def process_item(self, item, spider):
        if isinstance(item, LinkItem):
            Link(
                url=item.url,
                
        elif isinstance(item, TextItem):

        else:
            raise DropItem("Dropping item: {0}".format(item))


class MongoDBPipeline(AbstractMongoDBPipeline):

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
