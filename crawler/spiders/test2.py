import socket

import common.date
from crawler.spiders import BaseSpider
# 此文件包含的头文件不要修改
import scrapy
from utils.util_old import *
from crawler.items import *
from bs4 import BeautifulSoup
from scrapy.http import Request, Response
from utils import date_util

from datetime import datetime
import time
import re
import requests
global null
null = ''

# parse
# url = "http://filipino.cri.cn/balita.html"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")
# category1 = soup.select('.card-c-nav a')
# for i in category1:
#     print(i.text)  # 国家标题 共三个Tsina Daigdig ASEAN
# more_href = soup.select('.more-b a')
# print(len(more_href))
# for i in more_href:
#     print(i.get('href'))


# parse_pagelist
# url = "http://filipino.cri.cn"+"/b480c0dc-5236-47f5-bef1-a8240087bd2e.html"
# url="http://filipino.cri.cn/0aa226e5-932a-4d9b-b571-a8240089af76.html"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")
# pagedata = soup.find(attrs={'class':'list-box txt-listUl'}).select_one('ul').get('pagedata')
#
# pagedata_dict = eval(pagedata)
# print(pagedata_dict)
# total_page = pagedata_dict["total"]
# print(total_page)
# urls = pagedata_dict["urls"]
# print(urls)

# parse_page
# url = "http://filipino.cri.cn/0aa226e5-932a-4d9b-b571-a8240089af76.html"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")
# articles = soup.find(attrs={'class':'list-box txt-listUl'}).select('ul li h4')
# for i in articles:
#     href = i.select_one('a').get('href')
#     title = i.select_one('a').text
#     pub_time = i.select_one('i').text
#     print(href)
#     print(title)
#     print(pub_time)

# parse_article
# url = "http://filipino.cri.cn/20220111/bb9e11ac-e33f-4f40-faf3-d53bd4caa3e4.html"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")
# body = soup.select_one('#abody').text
# abstract = soup.select_one('#abody p').text
# print("abstract = "+abstract)
# print(body)

