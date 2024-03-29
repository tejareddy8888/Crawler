# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging
from urllib.parse import quote_plus
#import dnspython

class  Mongodbpipeline(object):

    def __init__(self,MongoURI,MongoDbTableName):
        self.MongoURI = MongoURI
        self.collection_name = MongoDbTableName

    @classmethod
    def from_crawler(cls, crawler):
        MongoURI = "mongodb+srv://sreddy:"+ quote_plus("Ziggo1020@") +"@cluster0-dp43v.mongodb.net/test"
        MongoDbTableName = crawler.settings['MONGODB_COLLECTION']
        return cls(MongoURI,MongoDbTableName)

    def open_spider(self,spider):
        logging.warning("Trying to connect to MongoDB")
        self.client = pymongo.MongoClient(self.MongoURI)
        try:
            self.db = self.client["Launchforth"]
            logging.warning("Created Db with name Launchforth")
        except pymongo.errors.InvalidOperation:
            logging.warning("unable to create launchforth collection") 

    def process_item(self, item, spider):
        try:
            self.db[self.collection_name].insert(item['content'])
            logging.info("data inserted")

        except pymongo.errors.WriteError:
            logging.warning("Error while inserting Item") 

        except pymongo.errors.NetworkTimeout:
            logging.warning("Error while inserting Item") 


    def close_spider(self,spider):
        logging.warning("Closing MongoDb connection")
        self.client.close()


class LaunchforthJsonextractionPipeline(object):
    def process_item(self, item, spider):
        return item
