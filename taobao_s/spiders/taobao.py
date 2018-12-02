# -*- coding: utf-8 -*-
import scrapy
import random
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from taobao_s.tools import data_cleaning,register
from taobao_s.items import TaobaoSItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    # allowed_domains = ['www.taobao.com']
    base_url = ['https://s.taobao.com/search?q=']
    pages = 100
    re_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'referer': 'https://www.taobao.com/',
        'accept-encoding': 'gzip, deflate, b',
    }
    i = 1

    def start_requests(self):
        keys = self.settings.get('KEYS')
        self.browser,list = register()
        self.browser.get(self.base_url[0]+keys)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        url_i = self.browser.current_url
        html = self.browser.page_source
        yield scrapy.Request(url=self.base_url[0]+keys,headers=self.re_headers,cookies=list,callback=self.parse,meta={'html':html,'i':self.i,'url':url_i})

    def parse(self, response):
        time.sleep(5)
        html = response.meta.get('html')
        i = response.meta.get("i")
        url_i = response.meta.get("url")
        i +=1
        if i > 100:
            return
        try:
            soup = BeautifulSoup(html,'html.parser')
            lists = soup.select('#mainsrp-itemlist > div > div > div > div')
            for list in lists:
                item = TaobaoSItem()
                url = list.select('a[class="pic-link J_ClickStat J_ItemPicA"]')[0].attrs.get('href','')
                name = list.select("a[class='J_ClickStat']")[0].get_text().strip()
                name = data_cleaning(name)
                price = list.select('div[class="price g_price g_price-highlight"] strong')[0].get_text()
                num = list.select('div[class="deal-cnt"]')[0].get_text()
                shop_name = list.select("a[class='shopname J_MouseEneterLeave J_ShopInfo']")[0].get_text().strip()
                shop_name = data_cleaning(shop_name)
                item['url'] = url
                item['name'] = name
                item['price'] = price
                item['num'] = num
                item['shop_name'] = shop_name
                yield item
            button = self.browser.find_elements(By.XPATH,'//a[@class="J_Ajax num icon-tag"]')[-1]
            button.click()
            time.sleep(random.random()*2)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            html = self.browser.page_source
            yield scrapy.Request(url=response.url,headers=self.re_headers,callback=self.parse,meta={'html':html,'i':i,'url':url_i},dont_filter=True)
        except Exception as e:
            time.sleep(10)
            print(e)
            self.browser.close()
            self.browser,list = register()
            self.browser.get(url=url_i)
            time.sleep(random.random()*2)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            html = self.browser.page_source
            yield scrapy.Request(url=response.url,headers=self.re_headers,callback=self.parse,meta={'html':html,'i':i,'url':url_i},dont_filter=True)

    def close(spider, reason):
        spider.browser.close()