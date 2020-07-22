# -*- coding: utf-8 -*-
'''
-*- coding: utf-8 -*-
@Author  : xbhog-Y
'''
import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .. import items
import sys
sys.path.append('..')

import db



class TzrcnSpider(scrapy.Spider):
    name = 'tzjobpro'
    allowed_domains = ['tzjob.com']
    start_urls = ['http://www.tzjob.com/']

    def __init__(self, table_name,webhook,keyword,*args, **kwargs):
        super(TzrcnSpider, self).__init__(*args, **kwargs)
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
        self.mydb = db.MydbOperator(table_name)
        self.mydb.create_table()
        self.isInitialize = self.mydb.is_empty_table()
        print(self.isInitialize)
        self.keyword = keyword
        self.webhook_url = webhook

    def parse(self, response):
        print(response.url)
        input = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/div/div/input")
        input.send_keys(self.keyword)
        search_but = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/form/div/div/div")
        search_but.click()
        try:
            item = items.TztalentItem()
            containers = self.driver.find_elements_by_xpath(
                "/html/body/form/div[2]/table[5]/tbody/tr/td/table/tbody/tr[position()>1]")
            for container in containers:
                item["company_name"] = container.find_element_by_xpath(".//td[1][@class='line_link']/a").get_attribute(
                    'title')
                item["company_url"] = container.find_element_by_xpath(".//td[1][@class='line_link']/a").get_attribute(
                    'href')
                item["site"] = container.find_element_by_xpath(".//td/table/tbody/tr/td[3]").text
                item["title"] = container.find_element_by_xpath(".//td[2][@class='line_link']/a").get_attribute('title')
                yield item
            self.driver.close()
        except:
            print("进入网站失败!")