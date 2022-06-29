from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
import json
from common.date import *


# author：魏芃枫
# check: 魏芃枫
class siiaonlineSpider(BaseSpider):
    name = 'siiaonline'
    website_id = 712
    language_id = 1866
    start_urls = ['https://www.siiaonline.org']

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        hrefs = soup.select("#nav-menu-item-1180 .second .inner ul li a")
        for href in hrefs:
            yield Request(url=href.get("href"), callback=self.parse_page)

    def parse_page(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.select("article")
        for article in articles:
            article_title = article.select_one("h5").text
            article_time = article.select_one(".time").text
            article_href = article.select_one("h5 a").get("href")
            article_format_time = article_time[-4:]+"-"+str(ENGLISH_MONTH[article_time[3:-6]])+"-"+article_time[0:2]+" 00:00:00"
            article_timestamp = DateUtil.formate_time2time_stamp(article_format_time)
            meta = {
                "title": article_title,
                "pub_time": article_format_time
            }
            if self.time is None or int(article_timestamp) >= int(self.time):
                yield Request(url=article_href, callback=self.parse_item, meta=meta)

        next_url = soup.select_one(".next a").get("href")
        yield Request(url=next_url, callback=self.parse_page)

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, "html.parser")
        item['title'] = response.meta['title']
        item['category1'] = None
        item['category2'] = None
        item['body'] = soup.select_one(".post_text_inner").text.strip()
        item['abstract'] = None
        item['pub_time'] = response.meta['pub_time']
        item['images'] = None
        yield item