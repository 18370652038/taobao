# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    # allowed_domains = ['qtotes.toscrape.com']
    start_urls = ['http://qtotes.toscrape.com/']
    start_url = 'https://s.taobao.com/search?q=%E8%93%9D%E7%89%99%E8%80%B3%E6%9C%BA&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'

    def parse(self, response):

        pass
