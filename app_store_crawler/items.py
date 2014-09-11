# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class CrawlerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class AppItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=Field()
    url=Field()
#    description=Field()
#    current_rating=Field()
#    all_rating=Field()
#    price=Field()
#    category=Field()
#    update=Field()
#    version=Field()
#    lang=Field()
#    app_link_first=Field()
#    app_link_second=Field()
#    pass
