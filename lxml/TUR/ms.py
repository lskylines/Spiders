import requests
from lxml import etree
from requests.exceptions import ConnectionError
import pymongo
import pandas as pd
from pandas import DataFrame
import csv


client = pymongo.MongoClient('localhost', 27017)  
db = client['stocks']

'''
爬取TUR的stock数据
'''

def get_page():       #获取源码
    url = 'https://cn.investing.com/instruments/HistoricalDataAjax'       #请求URL
    headers = '''
    Accept: text/plain, */*; q=0.01
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9
    Connection: keep-alive
    Content-Length: 190
    Content-Type: application/x-www-form-urlencoded
    Host: cn.investing.com
    Origin: https://cn.investing.com
    Referer: https://cn.investing.com/etfs/ishares-msci-turkey-historical-data
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36
    X-Requested-With: XMLHttpRequest
    '''
    headers = str_to_dict(headers)         #字符串转化为字典
    form_data = {
        'curr_id': '9244',
        'smlID': '2622629',
        'header': 'TUR历史数据',
        'st_date': '2008/08/13',
        'end_date': '2018/08/13',
        'interval_sec': 'Daily',
        'sort_col': 'date',
        'sort_ord': 'DESC',
        'action': 'historical_data'
        }
    try:
        response = requests.post(url=url, headers=headers, data=form_data)
        if response.status_code == 200:
           return response.text
        else:
            return None
    except ConnectionError as e:
        print("连接失败")
    except Exception as e:
        print("Failure")



def str_to_dict(headers):       #将headers字符串转化为字典
    header_dict = dict()
    headers = headers.split('\n')
    for h in headers:
        h = h.strip()
        if h:
            k, v = h.split(':', 1)
            header_dict[k] = v.strip()

    return header_dict





def parse_data(data):                 #解析数据,保存数据到csv文件中
    data = etree.HTML(data)
    items = data.xpath('//*[@id="curr_table"]/tbody/tr')
    with open('stocks.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['date', 'closing', 'opening', 'high', 'low', 'traper', 'rate']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            text = item.xpath('./td/text()')
            data_dict = {
                'date': text[0],
                'closing': text[1],
                'opening': text[2],
                'high': text[3],
                'low': text[4],
                'traper': text[5],
                'rate': text[6]
                }
            print(data_dict)
            writer.writerow(data_dict)
    f.close()

    
        #save_mongodb(data_dict)#保存到MongoDB

        
    
def save_mongodb(data):     #保存到MongoDB
    db['stock'].insert_one(data



if __name__ == "__main__":
    datas = get_page()
    parse_data(datas)
    
        
