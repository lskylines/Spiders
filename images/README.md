使用Scrapy爬取妹子图，将其id, url, title, thumb(缩略图)字段图保存到MongoDB， MYSQL中，并且将图片下载到当前目录的beauty目录下

MYSQL的用户user, password在Settings.py中进行设置， ITEM_PIPELINES中三个设置分别是图片下载，数据保存到MONGODB开启，MYSQL开启。

MYSQL保存字段开启之前需要现在MYSQL中创建数据库和表结构，之后在ITEM_PIPRLINES中将注释取消，即可开启

设置完成后启动爬虫:scrapy crawl img

