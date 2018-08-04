# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy import Request
from images.items import ImgItem
import json

class ImgSpider(scrapy.Spider):
    name = 'img'
    allowed_domains = ['image.so.com']  #允许域名，不在该域名下的URL自动排除
    start_urls = ['https://image.so.com/']


    def start_requests(self):  #该方法可以用于启动时设置起始URL
        data = {'ch' : 'beauty', 'listtype': 'new', 'temp': '1'}
        base_url = 'https://image.so.com/zj?'
        for page in range(1, self.settings.get('MAX_PAGE')+1):
            data['sn'] = page * 30
            url = base_url + urlencode(data)
            yield Request(url, self.parse)

    def parse(self, response):      #解析json数据
        results = json.loads(response.text)
        for result in results.get('list'):
            item = ImgItem()
            item['id'] = result.get('id')
            item['title'] = result.get('group_title')
            item['url'] = result.get('qhimg_url')
            item['thumb'] = result.get('qhimg_thumb_url')

            yield item

