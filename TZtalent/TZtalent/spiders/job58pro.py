# -*- coding: utf-8 -*-
import scrapy
from selenium import  webdriver
from pypinyin import lazy_pinyin
from TZtalent.items import TztalentItem
import sys
sys.path.append('..')

import db

class A58jobproSpider(scrapy.Spider):
    name = '58jobpro'

    def __init__(self,table_name,keyword,webhook,site,*args,**kwargs):
        super(A58jobproSpider, self).__init__(*args,**kwargs)
        # 防止selenium识别
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
        #https://nj.58.com/job/?key=%E5%A4%96%E8%B4%B8&classpolicy=main_null,job_A&final=1&jump=1
        self.webhook_url = webhook
        self.mydb = db.MydbOperator(table_name)
        self.mydb.create_table()
        self.isInitialize = self.mydb.is_empty_table()
        print(self.isInitialize)

        # 中文转拼音
        pinyin = lazy_pinyin(site)
        print(pinyin)
        self.site = pinyin[0] + pinyin[1]
        self.start_urls =[f'https://{self.site}.58.com/job/?key={keyword}&classpolicy=main_null,job_A&final=1&jump=1']

    def parse(self, response):
        li_lidt = response.xpath("//ul[@id='list_con']/li")
        for li in li_lidt:
            item = TztalentItem()
            # 职位
            title = li.xpath(".//em[@class='fontOrange']/text()").extract_first()
            if title == None:
                continue
            # 地点
            site_list = li.xpath(".//div[@class='job_name clearfix']//a/text()").extract_first()
            #位置的数据清洗
            site = site_list.split('   ')[1]
            #公司名
            comapny_name = li.xpath(".//div[@class='comp_name']/a/text()").extract_first()
            #公司的url
            comapny_url = li.xpath(".//div[@class='comp_name']/a/@href").extract_first()
            item['title'] = title
            item['company_name'] = comapny_name.split(" ")[1]
            item['company_url'] = comapny_url
            item['site'] = site
            # print(title,comapny_name,comapny_url,site)
            # print(item)
            yield item

    def spider_close(self,spider):
        spider.driver.quit()
