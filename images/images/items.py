# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ImgItem(scrapy.Item):
    #定义字段
    collection = table = 'beauty'  #MONGODB的集合 AND MYSQL的表名
    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    thumb = scrapy.Field()
