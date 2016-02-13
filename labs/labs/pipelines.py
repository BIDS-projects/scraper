from utils.pipelines import AbstractMongoDBPipeline, AbstractMySQLPipeline
from labs.items import LinkItem, TextItem, PaperItem

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


class MongoDBPipeline(AbstractMongoDBPipeline):

    def process_item(self, item, spider):
        if isinstance(item, ExternalLinkItem):
            self.link_collection.insert_one(dict(item))
            return item
        elif isinstance(item, InternalLinkItem):
            self.link_collection.insert_one(dict(item))
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
