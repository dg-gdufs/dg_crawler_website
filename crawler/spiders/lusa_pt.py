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

global null
null = ''


# author:魏芃枫


class Lusa(BaseSpider):
    name = 'lusa_pt'
    start_urls = ['https://www.lusa.pt/']
    website_id = 683  # 网站的id(必填)
    language_id = 2122  # 所用语言的id
    proxy = '02'

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        category1 = soup.find(attrs={'id': 'main-menu'}).select('li a')
        for i in category1[1:8]:
            category1_title = i.text
            category1_href = i.get("href")
            meta1 = {'category1': category1_title}
            yield Request(category1_href, callback=self.parse_pagelist, meta=meta1)

    def parse_pagelist(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        page_num = len(soup.find(attrs={'class': 'pagination pagination-sm'}).select("li"))
        print(page_num)
        for i in range(1, page_num + 1):
            data = {'hdPageNumber': str(i)}
            yield FormRequest(response.url, formdata=data, callback=self.parse_page, meta=response.meta)

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        article_list = soup.find(attrs={'class': 'article-category col-sm-12 m-bottom30'}).select('div .row .col-sm-12')
        for i in article_list:
            e_time = i.select_one('ul li').text.split(' ')
            date = e_time[0].split('-')
            pub_time = date[2] + '-' + date[1] + '-' + date[0] + " " + e_time[1] + ":00"
            timestamp = utils.date_util.DateUtil.formate_time2time_stamp(pub_time)
            try:
                if self.time == None or timestamp >= int(self.time):
                    title = i.select_one('h3').text
                    href = i.select_one('a').get('href')
                    abstract = i.select('a')[-1].text
                    meta1 = response.meta  # 含category1
                    meta2 = {'title': title, 'abstract': abstract, 'pub_time': pub_time}
                    meta2.update(meta1)
                    yield Request(href, callback=self.parse_detail, meta=meta2)
                else:
                    self.logger.info('时间截止！')
            except:
                continue

    def parse_detail(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 检查该页有无图片
        image_flag = 1
        try:
            src = soup.find(attrs={'class': "article col-md-12 m-bottom20"}).select_one('img').get("src")
        except:
            image_flag = 0
            self.logger.info("No Image")

        # 检查该页为静态文章(try)还是动态渲染文章(except)
        try:
            article = soup.select_one('.article-content .lt-text')
            paragraph = article.select_one('p').text
        except:
            a = eval(re.findall("var EncryptedText = \S+;", str(article))[0].split()[3][:-1])
            ashx_path = "https://www.lusa.pt/Handlers/a.ashx"
            response_p = requests.post(ashx_path, data={'a': a})
            soup_p = BeautifulSoup(response_p.text, "html.parser")
            paragraph = soup_p.select_one('p').text

        item = NewsItem()
        item['title'] = response.meta['title']
        item['pub_time'] = response.meta['pub_time']
        item['body'] = paragraph
        item['abstract'] = response.meta['abstract']
        item['category1'] = response.meta['category1']
        item['category2'] = None
        if image_flag == 1:
            item['images'] = src
        else:
            item['images'] = None
        yield item
