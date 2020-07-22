##!/usr/bin/python3
'''
-*- coding: utf-8 -*-
@Author  : xbhog-Y
'''

import scrapy
from selenium import webdriver
from TZtalent.items import TztalentItem
import sys
sys.path.append('..')
import db


class TzcodeSpider(scrapy.Spider):
    #泰州就业人才网
    name = 'tzcode'
    # allowed_domains = ['www.xxx.com']
    def __init__(self,table_name,keyword,webhook,*args,**kwargs):
        super(TzcodeSpider, self).__init__(*args, **kwargs)
        #防止selenium识别
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        #谷歌的无头模式
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        # self.driver = webdriver.Chrome()
        self.keyword = keyword
        self.webhook_url = webhook
        self.mydb = db.MydbOperator(table_name)
        self.mydb.create_table()
        self.isInitialize = self.mydb.is_empty_table()
        print(self.isInitialize)
        self.start_urls =[f"http://www.910091.com/job/list/0-12-0-0_0_0_0_0_0_0_0-0-0-0-1.html?{self.keyword}"]

    def parse(self, response):
        # print(response.url)
        #父标签
        div_list = response.xpath("//div[@class='job_left_sidebar']/div")
        item = TztalentItem()
        for div in div_list:
            item['title'] = div.xpath(".//a/font/text()").extract_first()
            #判断title是否为空
            if item['title'] == None:
                break
            item['company_name'] = div.xpath(".//div[1]/div[3]/a/text()").extract_first()
            item['company_url'] = div.xpath(".//div[1]/div[3]/a/@href").extract_first()
            item['site'] = div.xpath('.//div[1]/div[1]/span[1]/em/text()').extract_first()
            yield item


    def spider_close(self,spider):
        #退出驱动并关闭所有关联的窗口
        self.driver.quit()