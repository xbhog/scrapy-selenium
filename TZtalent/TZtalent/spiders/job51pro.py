# -*- coding: utf-8 -*-
import scrapy
from selenium import  webdriver
from selenium.webdriver import  ActionChains
import sys
sys.path.append('..')
import db
from TZtalent.items import TztalentItem
from pypinyin import lazy_pinyin
import time
from lxml import etree

class Job51proSpider(scrapy.Spider):
    name = 'job51pro'

    def __init__(self,table_name,keyword,webhook,site,*args,**kwargs):
        super(Job51proSpider, self).__init__(*args,**kwargs)
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
        self.keyword = keyword
        self.webhook_url = webhook
        self.mydb = db.MydbOperator(table_name)
        self.mydb.create_table()
        self.isInitialize = self.mydb.is_empty_table()
        # 中文转拼音
        pinyin = lazy_pinyin(site)
        # print(pinyin)
        self.site = pinyin[0] + pinyin[1]
        self.start_urls = [f"https://www.51job.com/{self.site}/"]


    def parse(self, response):
        time.sleep(2)
        #找到文本框
        self.driver.find_element_by_id("kwdselectid").send_keys(self.keyword)
        # 鼠标移动到点击位置
        ac = self.driver.find_element_by_xpath('//*[@id="supp"]/div[1]/div/div[1]/button')
        ActionChains(self.driver).move_to_element(ac).click(ac).perform()
        time.sleep(2)
        # 解析selenium发过来的response数据
        str_html = self.driver.page_source
        html = etree.HTML(str_html)
        #找到数据的父标签
        div_list = html.xpath("//*[@class='dw_table']/div")
        for div in div_list:
            item = TztalentItem()
            title = div.xpath(".//p/span/a/@title")
            #返回前三个数据是[],如果使用的extract_first返回的是None
            if title == []:
                continue
            item["title"] = title[0]
            item['company_name'] = div.xpath(".//span[@class='t2']//a/text()")[0]
            item['company_url'] = div.xpath(".//span[@class='t2']/a/@href")[0]
            item['site'] = div.xpath(".//span[@class='t3']/text()")[0]

            # print(item)
            yield item


    def close_spider(self,spider):
        self.driver.quit()
