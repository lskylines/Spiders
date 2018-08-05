import requests
from bs4 import BeautifulSoup
import time
import pymongo
from utils import headers

client = pymongo.MongoClient("localhost", 27017)
bj = client['bj']
itemlink = bj['itemlink']
info = bj['info']




#抓取商品的链接
def get_links(channel, pages):
    #http://bj.58.com/diannao/pn2/
    list_view = '{}/pn{}'.format(channel, str(pages))
    web_data = requests.get(url=list_view, headers=headers)
    time.sleep(1)
    soup = BeautifulSoup(web_data.text, 'lxml')
    if soup.find('td', 't'):
        for link in soup.select('td.t a.t'):
            item_link = link.get('href').split('?')[0]
            itemlink.insert_one({'item_url': item_link})  #商品详情页URL保存到MongoDB
            print(item_link)
    else:
        pass      #Nothing

def get_item_info(info_url):  #商品详情页抓取
    try:
        response = requests.get(url=info_url)
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.select('h1.info_titile')[0]
        price = soup.select('span.price_now > i')[0]
        area = soup.select('div.palce_li > span > i')[0] if soup.find('div', 'palce_li') else None
        data = {
            'title': title.get_text(),    #标题
            'price': price.get_text(),    #价格
            'area': area.get_text()       #地域
        }
        print(data)
    except IndexError as e:
        print(e)
        pass
    except Exception as  e:
        print(e)
        pass
    # info.insert_one(data)
# get_links('http://bj.58.com/diannao/', 2)
# get_item_info('http://zhuanzhuan.58.com/detail/1023863913739583491z.shtml')
