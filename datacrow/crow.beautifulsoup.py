# Python3 

import requests
from bs4 import BeautifulSoup
url = 'http://www.tobuzoo.com/zoo/list/'
strhtml = requests.get(url)
soup = BeautifulSoup(strhtml.text, 'lxml')

# 以東武動物公園網站為例
# 使用開發者工具選擇html路徑 參考圖(2.4.crow.beautifulsoup.001.png)
# '#tab1 > ul > li:nth-child(1) > a > img'
# 去除li之冒號後方
# #tab1 > ul > li > a > img

data = soup.select('#tab1 > ul > li > a > img')

data_list = []
for item in data:
    # <img alt="ホンドテン" src="/zoo/list/details/pc/0_an_414_02.jpg"/>
    hash = {
        'title' : item.get('alt'),
        'url' : item.get('src')
    }
    print(hash)
    data_list.append(hash)

'''
example
{'url': '/zoo/list/details/pc/0_an_43_02.jpg', 'title': 'シナガチョウ'}
{'url': '/zoo/list/details/pc/0_an_36_02.jpg', 'title': 'アライグマ'}
{'url': '/zoo/list/details/pc/0_an_38_02.jpg', 'title': 'エジプトルーセットオオコウモリ'}
{'url': '/zoo/list/details/pc/0_an_39_02.jpg', 'title': 'アフリカタテガミヤマアラシ'}
{'url': '/zoo/list/details/pc/0_an_7_02.jpg', 'title': 'キリン'}
{'url': '/zoo/list/details/pc/0_an_9_02.jpg', 'title': 'ダチョウ'}
{'url': '/zoo/list/details/pc/0_an_10_02.jpg', 'title': 'シロサイ'}
{'url': '/zoo/list/details/pc/0_an_8_02.jpg', 'title': 'シマウマ'}
{'url': '/zoo/list/details/pc/0_an_411_02.jpg', 'title': 'バーバリーシープ'}
'''

# 存檔
import urllib.request
import time
import datetime
import os
from random import randint

# 目錄
directory = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
if not os.path.exists(directory):
    os.makedirs(directory)

# 儲存
for u in data_list:
    if u.get('url') == None:
        next
    if u.get('title') == None:
        next
    urllib.request.urlretrieve('http://www.tobuzoo.com' + u['url'], directory + '/' + u['title']+'.jpg')
    time.sleep(1 + randint(0, 3))
