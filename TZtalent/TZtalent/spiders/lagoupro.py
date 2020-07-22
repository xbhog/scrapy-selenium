# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver import  ActionChains
import time
from pypinyin import lazy_pinyin
from TZtalent.items import TztalentItem
from lxml import etree
import sys
sys.path.append('..')

import db

class LagouproSpider(scrapy.Spider):
    name = 'lagoupro'

    def __init__(self, table_name, keyword, site, webhook, *args, **kwargs):
        super(LagouproSpider, self).__init__(*args, **kwargs)

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
        self.keyword = keyword
        self.webhook_url = webhook
        self.mydb = db.MydbOperator(table_name)
        self.mydb.create_table()
        self.isInitialize = self.mydb.is_empty_table()
        print(self.isInitialize)
        #中文转拼音
        pinyin = lazy_pinyin(site)
        print(pinyin)
        self.site = pinyin[0]+pinyin[1]
        print(self.site)
        #字符串拼接---得到地域URL
        self.start_urls =[f"https://www.lagou.com/{self.site}-zhaopin/"]


    def parse(self, response):
        self.driver.find_element_by_id("keyword").send_keys(self.keyword)
        #鼠标移动到点击位置
        ac = self.driver.find_element_by_id("submit")
        ActionChains(self.driver).move_to_element(ac).perform()
        time.sleep(2)
        ActionChains(self.driver).move_to_element(ac).click(ac).perform()
        time.sleep(2)
        # 解析selenium发过来的response数据
        str_html= self.driver.page_source
        html = etree.HTML(str_html)
        try:
            # 父标签---所需要信息标签上的父标签
            div_list = html.xpath("//ul[@class='item_con_list']/li")
            item = TztalentItem()
            for div in div_list:
                item['title'] = div.xpath(".//h3/text()")[0]
                # 判断title是否为空
                if item['title'] == None:
                    continue
                item['company_name'] = div.xpath(".//div[@class='company_name']/a/text()")[0]
                item['company_url'] = div.xpath(".//div[@class='company_name']/a/@href")[0]
                item['site'] = div.xpath(".//span[@class='add']/em//text()")[0]
                yield item
                # print(item)

        except:
            print('没有数据')

    def spider_close(self, spider):
        # 退出驱动并关闭所有关联的窗口
        self.driver.quit()