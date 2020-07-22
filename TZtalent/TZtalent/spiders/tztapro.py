# -*- coding: utf-8 -*-
'''
-*- coding: utf-8 -*-
@Author  : xbhog-Y
'''
import scrapy
from selenium import webdriver
from urllib.parse import quote
from TZtalent.items import TztalentItem
import sys
sys.path.append('..')

import db

class TztaproSpider(scrapy.Spider):
    name = 'tztapro'

    def __init__(self, table_name, keyword, webhook, *args, **kwargs):
        super(TztaproSpider, self).__init__(*args, **kwargs)
        # 防止selenium识别
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # 谷歌的无头模式
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                  """
        })
        #灵活变动，该网站是统一是gb2312编码，需要将URL进行转换--urlencode编码
        self.keyword = quote(keyword.encode("gb2312"))
        # print(self.keyword)
        self.webhook_url = webhook
        self.mydb = db.MydbOperator(table_name)
        self.mydb.create_table()
        self.isInitialize = self.mydb.is_empty_table()
        print(self.isInitialize)
        self.start_urls = [f"https://www.0523rc.cn/sousuo/Company.asp?Position_b=&Position_s=&Qualification=&Province=&City=&County=&ValidityDate=&qiyess=1&keyword={self.keyword}"]

    def parse(self, response):
        # 解析selenium发过来的response数据
        try:
            # 父标签---所需要信息标签上的父标签
            div_list = response.xpath("//div[@class='zxzwlbz']/div")
            item = TztalentItem()
            for div in div_list:
                item['title'] = div.xpath(".//li[@class='zwa2']/a/text()").extract_first()
                # 判断title是否为空
                if item['title'] == None:
                    continue
                item['company_name'] = div.xpath(".//li[@class='zwa3']/a/text()").extract_first()
                item['company_url'] = div.xpath(".//li[@class='zwa3']/a/@href").extract_first()
                item['site'] = div.xpath(".//li[@class='zwa7']/span[1]/text()").extract_first()
                yield item

        except:
            print('没有数据')


    def spider_close(self,spider):
        #退出驱动并关闭所有关联的窗口
        self.driver.quit()
