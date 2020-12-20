# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from scrapy import Selector  
from doubanmovie.items import DoubanmovieItem
import time


class DoubanspiderSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    # 起始URL列表
    start_urls = ['https://movie.douban.com/subject/30346025/comments']
    def start_requests(self):
        for i in range(0, 8):
            url = f'https://movie.douban.com/subject/30346025/comments?start={i*20}'
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):  
        # 爬取网站得到response后，自动回调parse方法                            
        item = DoubanmovieItem()
        info_list = response.xpath('//div[@class="comment"]')
        # print(info_list)

        for info in info_list:
            item['author'] = info.xpath('.//span[@class="comment-info"]/a/text()').extract_first()
            rate_raw = info.xpath('.//span[@class="comment-info"]/span/@class').extract_first()
            rate_re = 'allstar(.+)0'
            item['rate'] = re.findall(rate_re, rate_raw)[0]
            item['content'] = info.xpath('.//p[@class=" comment-content"]/span/text()').extract_first().replace('\n', '').replace('\r', '')
            item['date'] = info.xpath('.//span[@class="comment-info"]/span[@class="comment-time "]/@title').extract_first()
            yield item
