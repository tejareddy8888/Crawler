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
    table_name = "Project_details"
    def open_spider(self,spider):
        logging.warning("Trying to connect to MongoDB")
        self.client = pymongo.MongoClient("mongodb+srv://sreddy:"+ quote_plus("Ziggo1020@") +"@cluster0-dp43v.mongodb.net/test")
        try:
            self.db = self.client["Launchforth"]
            logging.warning("Created Db with name Launchforth")
        except pymongo.errors.InvalidOperation:
            logging.warning("unable to create launchforth collection") 

    def process_item(self, item, spider):
        try:
            self.db[self.table_name].insert(item)

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
