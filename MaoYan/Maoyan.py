import json
import requests
from requests.exceptions import RequestException
import re
import time
from multiprocessing import Pool


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)      #使用正则提取相关字段
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],               #缩略图
            'title': item[2],               #电影名称
            'actor': item[3].strip()[3:],   #导演
            'time': item[4].strip()[5:],    #上映时间
            'score': item[5] + item[6]      #评分
        }


def write_to_file(content):                #写入到文件中
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset): 
    url = 'http://maoyan.com/board/4?offset=' + str(offset)      #构造URL
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
##    pool = Pool()          #多进程爬取
##    pool.map(main, [i for i in range(10)])
