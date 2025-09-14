# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

import random


class AutopartscatScraperPipeline:
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_urls = item['Image URL']
        for image_url in image_urls:
            if image_url:
                yield scrapy.Request(image_url, meta={'Merken': item['Merken'], 'Types': item['Types'],
                                                      'Serial Number': item['Serial Number']})

    def file_path(self, request, response=None, info=None, **kwargs) -> str:
        types = re.sub('[^A-Za-z0-9]+', '', request.meta['Types']).strip()
        if request.meta['Serial Number']:
            return f"Images_with_serial_number/{request.meta['Merken']}_{types}_{request.meta['Serial Number']}.jpg"
        else:
            number = random.randint(100000000000, 999999999999)
            return f"Images_with_random_number/{request.meta['Merken']}_{types}_{number}.jpg"


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        # if not image_paths:
        #     raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item
