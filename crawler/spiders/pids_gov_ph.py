from crawler.spiders import BaseSpider
# 此文件包含的头文件不要修改
import scrapy
from utils.util_old import *
from crawler.items import *
from bs4 import BeautifulSoup
from scrapy.http import Request, Response

from datetime import datetime
import time
import re
import requests


# author:魏芃枫


class Pids(BaseSpider):
    name = 'pids_gov_ph'
    allowed_domains = ['pids.gov.ph']
    start_urls = ['https://pids.gov.ph/press-releases/']
    website_id = 1256  # 网站的id(必填)
    language_id = 1866  # 所用语言的id
    sql = {  # sql配置
        'host': '192.168.235.162',
        'user': 'dg_admin',
        'password': 'dg_admin',
        'db': 'dg_crawler'
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }

    def parse(self, response):  # 获取最新发布新闻的页码 并生成所有页码的网页的访问
        soup = BeautifulSoup(response.text, "html.parser")
        latest_page = soup.select_one('.text-block a').attrs['href'].split('/')[2]
        for i in range(1, latest_page + 1):
            head_url = "https://pids.gov.ph/press-releases/" + str(i)
            try:
                print("url = " + head_url)
                yield Request(head_url, callback=self.parse_detail)
            except:
                self.logger.info("Page " + head_url + " not exist!")

    # def parse_page(self, response):
    #     date_english = {
    #         'January': 1,
    #         'February': 2,
    #         'March': 3,
    #         'April': 4,
    #         'May': 5,
    #         'June': 6,
    #         'July': 7,
    #         'August': 8,
    #         'September': 9,
    #         'October': 10,
    #         'November': 11,
    #         'December': 12
    #     }
    #     soup = BeautifulSoup('html.parser', response.text)
    #     menu = soup.find_all(attrs={'class': "large-9 columns"})
    #     print(menu)
    #     for i in menu:
    #         try:
    #             title = i.select_one("h4").text
    #             date = i.select_one('p').text.split(" ")
    #             month = str(date_english[date[1]])
    #             day = date[2].replace(',', " ")
    #             year = date[3]
    #             pub_time = ("{}-{}-{}".format(year, month, day) + "00:00:00")
    #             print(pub_time)
    #             href = "https://pids.gov.ph"+i.select_one(".icon-button").get('href')
    #             meta = {'title': title, 'pub_time': pub_time}
    #             yield Request(href, callback=self.parse_detail, meta=meta)
    #
    #         finally:
    #             continue

    def parse_detail(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.select_one('.capitalize').text
        span_list = soup.select('span')
        body = ''
        for i in span_list:
            span_content = i.text + '\n'
            body += span_content
        print("title = "+title)
        print("body = "+body)
        item = NewsItem()
        item['pub_time']=None
        item['image'] = None
        item['category1'] = None
        item['category2'] = None
        item['abstract'] = span_list[0].text
        item['title'] = title
        item['body'] = body
        return item
