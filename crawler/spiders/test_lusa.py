import socket

import common.date
import utils.date_util
from crawler.spiders import BaseSpider
# 此文件包含的头文件不要修改
import scrapy
from utils.util_old import *
from crawler.items import *
from bs4 import BeautifulSoup
from scrapy.http import Request, Response
from utils import date_util
from scrapy.http import FormRequest
from datetime import datetime
import time
import re
import requests

# parse_category1 OK
# headers = {'proxy': 'http://192.168.235.5:8888'}
# url = "https://www.lusa.pt/"
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "html.parser")
# category1 = soup.find(attrs={'id': 'main-menu'}).select('li a')
# for i in category1[1:8]:
#     category1_title = i.text
#     category1_href = i.get("href")
#     print(category1_title)
#     print(category1_href)
# 需要下标 1-6

# parse_pages
# headers = {'proxy': 'http://192.168.235.5:8888',
#            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#            }
# url = "https://www.lusa.pt/national"
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "html.parser")
# page_num = len(soup.find(attrs={'class': 'pagination pagination-sm'}).select("li"))
# print(page_num)
# for i in range(1, page_num+1):
#     data = {'hdPageNumber': i}
# yield Request(url,callback=xxx,data=data)

# parse_page OK
# headers = {'proxy': 'http://192.168.235.5:8888',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }
# url = "https://www.lusa.pt/national"
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "html.parser")
# article_list = soup.find(attrs={'class': 'article-category col-sm-12 m-bottom30'}).select('div .row .col-sm-12')
# # print(article_list)
# for i in article_list:
#     title = i.select_one('h3').text
#     href = i.select_one('a').get('href')
#     abstract = i.select('a')[-1].text
#     e_time = i.select_one('ul li').text.split(' ')
#     date = e_time[0].split('-')
#     pub_time = date[2] + '-' + date[1] + '-' + date[0]+" " + e_time[1] + ":00"
#     timestamp = utils.date_util.DateUtil.formate_time2time_stamp(pub_time)
#     print('title = '+title)
#     print("abstract = "+abstract)
#     print("href = " + href)
#     print('pub_time = ' + pub_time)
#     print('timestamp = '+ str(timestamp))
#     print('\n')

# parse_article
# headers = {'proxy': 'http://192.168.235.5:8888',
#            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#            }
# url = "https://www.lusa.pt/national/article/2022-01-13/35226971/alargamento-de-hor%C3%A1rios-permitiu-mais-cerca-de-130-mil-atendimentos-nas-lojas-e-espa%C3%A7os-cidad%C3%A3o"
# # url = "https://www.lusa.pt/article/35209905/legislativas-ahresp-apresenta-20-propostas-para-novo-governo-relan%C3%A7ar-economia"
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, "html.parser")
# try:
#     src = soup.find(attrs={'class': "article col-md-12 m-bottom20"}).select_one('img').get("src")
# except:
#     print("no image")
# try:
#     article = soup.select_one('.article-content .lt-text')
#     paragraph =article.select_one('p').text
#     print(paragraph)
# except:
#     a = eval(re.findall("var EncryptedText = \S+;",str(article))[0].split()[3][:-1])
#     ashx_path = "https://www.lusa.pt/Handlers/a.ashx"
#     response_p = requests.post(ashx_path, data={'a': a})
#     soup_p = BeautifulSoup(response_p.text, "html.parser")
#     paragraph = soup_p.select_one('p').text
#     print(paragraph)
