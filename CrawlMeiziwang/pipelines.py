# -*- coding: utf-8 -*-

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import os,shutil
import urllib.request
import CrawlMeiziwang.settings as settings
class CrawlmeiziwangPipeline(object):
    def process_item(self, item, spider):
        return item


class MeizituDownloadPieline(ImagesPipeline):
    def get_media_requests(self, item, info):
        headers = {}
        headers['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        headers['Referer']=item['image_refers']
        yield Request(item['image_urls'], headers=headers)

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            print("Item contains no files")
        else:
            dest_dir = item['image_paths'] + '/' +item['image_name']
            if not os.path.exists(dest_dir):
                shutil.move(settings.IMAGES_STORE+'/'+file_paths[0], dest_dir)
                print(item['image_urls'] + ' has download finished')
            else:
                os.remove(settings.IMAGES_STORE + '/' + file_paths[0])
                print(item['image_urls']+' exists')



