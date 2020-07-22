# -*- coding: utf-8 -*-
import scrapy
from selenium import  webdriver
import sys
sys.path.append('..')
import db
from pypinyin import lazy_pinyin

class Job51proSpider(scrapy.Spider):
    name = 'job51pro'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://www.xxx.com/']
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
        self.webhook_url = webhook
        self.mydb = db.MydbOperator(table_name)
        self.mydb.create_table()
        self.isInitialize = self.mydb.is_empty_table()
        print(self.isInitialize)

        # 中文转拼音
        pinyin = lazy_pinyin(site)
        print(pinyin)
        self.site = pinyin[0] + pinyin[1]
        # self.start_urls =[f'https://{self.site}.58.com/job/?key={keyword}&classpolicy=main_null,job_A&final=1&jump=1']
        self.start_urls = [
            'https://search.51job.com/list/070500,000000,0000,00,2,99,%25E5%25A4%2596%25E8%25B4%25B8,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=1&dibiaoid=0&line=&welfare=']
    def parse(self, response):
        pass
