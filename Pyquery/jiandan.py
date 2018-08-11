import requests
import gevent
import time
from gevent import monkey
from pyquery import PyQuery as pq
import json

class Jiandan(object):
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def Getpage(self):                 #获取HTML文本
        try:
            response = requests.get(url=self.url, headers=self.headers)
            data = response.text
            self.Parser(data)
        except RuntimeError as e:
            print(e)
        except Exception as e:
            print('Failure:',e)

    def Parser(self, data):             #Pyquery解析文本
        doc = pq(data)
        docs = doc('#content div.post.f.list-post')
        for item in docs.items():
            name = item('.indexs h2 a').text()
            contribute = item('.time_s strong a').text()

            data = {'name': name, 'contribute':contribute}
            print(data)
            self.WriteDown(data)

            
    def WriteDown(self, data):      #保存为TXT文件                         
        with open('jiandan.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False)+'\n')



def main(i):
    url = 'http://jandan.net/page/'+str(i)          #构造url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'}
    spider = Jiandan(url, headers)
    spider.Getpage()

if __name__ == "__main__":
    #同步爬取
##    start_time = time.time()
##    for i in range(1,20):
##        main(i)
##    end_time = time.time()


    #异步爬取
    async_time = time.time()
    monkey.patch_all()
    jobs = [gevent.spawn(main, i )for i in range(1,20)]
    gevent.joinall(jobs)
    async_end_time = time.time()
    print("异步爬取时间:",async_end_time - async_time)
##    print("同步爬取时间:", end_time - start_time)
