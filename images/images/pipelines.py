# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request

class ImgPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_path = url.split('/')[-1]
        return file_path

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Image download failed")
        return item

    def get_media_requests(self, item, info):
        yield Request(item['url'])


class MongoPipeline(object):
    def __init__(self, MONGO_URI, MONGO_DB):
        self.mongo_uri = MONGO_URI
        self.mongo_db = MONGO_DB

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            MONGO_URI=crawler.settings.get("MONGO_URI"),
            MONGO_DB=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item ,spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()


class MysqlPipeline(object):
    def __init__(self, HOST, USER, PASSWORD, DATABASE, PORT):
        self.host = HOST
        self.user = USER
        self.password = PASSWORD
        self.database = DATABASE
        self.port = PORT

    @classmethod
    def from_crawler(cls, crawler):        #用于从settings中取出相关的params
        return cls(
            HOST=crawler.settings.get("MYSQL_HOST"),
            USER=crawler.settings.get("MYSQL_USER"),
            PASSWORD=crawler.settings.get("MYSQL_PASSWORD"),
            DATABASE=crawler.settings.get("MYSQL_DATABASE"),
            PORT=crawler.settings.get("MYSQL_PORT")
        )

    def open_spider(self, spider):       #启动爬虫时自动执行
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port,
                                  charset='utf8')

        self.cursor = self.db.cursor()

    def close_spider(self, spider):  #爬虫结束时自动执行
        self.db.close()

    def process_item(self, item, spider):       #爬取数据经过这一段，用于保存数据
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s(%s) values (%s)' %(item.table, keys, values)
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
        except:
            self.db.rollback()
        return item
