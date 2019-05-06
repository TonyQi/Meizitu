# coding=UTF_8

import scrapy
from bs4 import BeautifulSoup
import random
import time
import os
from CrawlMeiziwang.items import CrawlmeiziwangItem


class MeiziwangCrawer(scrapy.Spider):



    name = "MeiziwangCrawer"

    start_urls = ['https://www.mzitu.com/']

    base_url = ['https://www.mzitu.com/', 'https://www.mzitu.com/all/']

    delay = 0




    # @classmethod
    # def from_crawler(cls, crawler):
    #     delay = 10
    #     if not isinstance(delay, int):
    #         raise ValueError("RANDOM_DELAY need a int")
    #     return cls(delay)
    #
    # def process_request(self, request, spider):
    #     delay = random.randint(0, self.delay)
    #     time.sleep(delay)



    def parse(self, response):
        soup = BeautifulSoup(response.body)
        print(soup.contents)
        header = soup.find('ul', class_="menu")
        print(header)
        com_a_list = header.find_all('a', attrs={'href': True})
        for tag_a in com_a_list:
            url = tag_a['href']
            if  url not in self.base_url:
                print(url)
                # handles_request()
                yield scrapy.Request(url=url, callback=self.parse_sub_html)


    def parse_sub_html(self, response):
        soup = BeautifulSoup(response.body)
        # print(soup.contents)
        pins = soup.find('ul', id="pins")
        if pins:
            pin_items = pins.find_all('a', attrs={'href': True})
            for pin in pin_items:
                yield scrapy.Request(url=pin['href'], callback=self.parse_image_html)
        next = soup.find('a', class_="next page-numbers")
        if next:
            print(response._url+" next page url is "+ next['href'])
            yield scrapy.Request(url=next['href'], callback=self.parse_sub_html)
        else:
            print(response._url+ " next page url is none")


    def parse_image_html(self, response):
        soup = BeautifulSoup(response.body)
        title = soup.find('div', class_="currentpath").text
        titles = title.split("»")
        title = titles[len(titles) - 1]
        title = title.strip()
        # 创建文件夹
        image_dir = '/Volumes/MyPassport/images/' + title
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        images = soup.find('div', class_="main-image").find_all('img')
        for image in images:
            item = CrawlmeiziwangItem()
            src = image['src']
            names = src.split("/")
            item['image_name'] = names[len(names) - 1]
            item['image_urls'] = image['src']
            item['image_paths'] = image_dir
            item['image_refers'] = response._url
            dest_dir = item['image_paths'] + '/' + item['image_name']
            if not os.path.exists(dest_dir):
                yield item
        pages = soup.find('div', class_="pagenavi").find_all('a', attrs={'href': True})
        for page in pages:
            if '下一页' in page.text:
                yield scrapy.Request(url=page['href'], callback=self.parse_image_html)
