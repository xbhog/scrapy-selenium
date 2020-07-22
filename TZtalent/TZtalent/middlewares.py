# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.http import HtmlResponse
import time


#设置selenium的中间件
class SelemiumSpiderMiddleware(object):

    def process_request(self, request, spider):
        spider.driver.get(request.url)
        time.sleep(1)
        #获得渲染后的网页源代码
        page_text = spider.driver.page_source
        # spider.driver.close()
        #创建响应对象
        return HtmlResponse(url=request.url, body=page_text, request=request, encoding='utf-8')


