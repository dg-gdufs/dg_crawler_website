from bs4 import BeautifulSoup
from crawler.spiders import BaseSpider
from crawler.items import *
from utils.date_util import DateUtil
from scrapy.http.request import Request
import json


# author：魏芃枫
# check: 魏芃枫
class moeSpider(BaseSpider):
    name = 'moe_gov'
    website_id = 400
    language_id = 2036
    start_urls = ['https://www.moe.gov.my/menumedia/media-elektronik/berita-dan-aktiviti']

    def parse(self, response):
        malay_month = {
            "Januari": "1",
            "Februari": "2",
            "Mac": "3",
            "April": "4",
            "Mei": "5",
            "Jun": "6",
            "Julai": "7",
            "Ogos": "8",
            "September": "9",
            "Oktober": "10",
            "November": "11",
            "Disember": "12"
        }
        soup = BeautifulSoup(response.text, features="lxml")
        trs = soup.select("tbody tr")
        for tr in trs:
            list_title = tr.select_one(".list-title a")
            title = list_title.text.strip()
            href = "https://www.moe.gov.my" + list_title.get('href')
            malay_time = tr.select_one('td:nth-child(2)').text.strip()
            format_time = malay_time[-4:] + "-" + malay_month[malay_time[3:-5]] + "-" + malay_time[0:2] + " 00:00:00"
            timestamp = DateUtil.formate_time2time_stamp(format_time)
            meta = {
                'pub_time': format_time,
                'title': title,
            }
            if self.time is None or int(timestamp) >= int(self.time):
                yield Request(url=href, callback=self.parse_item, meta=meta)
        next_url = "https://www.moe.gov.my" + soup.select(".next")[-1].get('href')
        yield Request(url=next_url, callback=self.parse)

    def parse_item(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, features='lxml')
        item['title'] = response.meta['title']
        item['category1'] = None
        item['category2'] = None
        item['body'] = soup.select_one(".uk-margin-medium-top").text.strip()
        item['abstract'] = None
        item['pub_time'] = response.meta['pub_time']
        item['images'] = None
        yield item
