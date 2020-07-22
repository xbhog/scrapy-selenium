# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TztalentItem(scrapy.Item):
    title = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    site = scrapy.Field()
