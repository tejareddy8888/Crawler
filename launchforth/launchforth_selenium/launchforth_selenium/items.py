# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class LaunchforthSeleniumItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Project = Field()
    random = Field()
