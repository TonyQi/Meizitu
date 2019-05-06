# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class CrawlmeiziwangItem(scrapy.Item):
    image_refers = Field()
    image_urls = Field()
    image_name = Field()
    image_paths = Field()
    pass

