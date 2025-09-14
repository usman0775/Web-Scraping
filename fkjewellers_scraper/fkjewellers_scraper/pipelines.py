import scrapy.exceptions
import os
from itemadapter import ItemAdapter
import scrapy.exceptions
from scrapy.pipelines.images import ImagesPipeline


class ImageScraperPipeline(ImagesPipeline):
    max_size = 197 * 1024 * 1024
    loc = 'IMAGES_1'
    folder_no = 1

    def get_media_requests(self, item, info):
        if item['image_urls']:
            for index, image in enumerate(item['image_urls'], start=1):
                yield scrapy.Request(image, meta={'sku': item['SKU'], 'rank': index})
        folder_path = f'IMAGES/{self.loc}'
        folder_size = get_folder_size(folder_path)
        if folder_size > self.max_size:
            self.folder_no += 1
            self.loc = self.loc.split('_')[0] + '_' + str(self.folder_no)

    def file_path(self, request, response=None, info=None, *, item=None):
        sku = request.meta['sku']
        rank = request.meta['rank']
        image_name = f"{self.loc}/{sku}/{sku}_{rank}.jpg"
        return image_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        # if not image_paths:
        #     raise scrapy.DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        names = []
        for name in image_paths:
            names.append(name.split('/')[-1])
        adapter['names'] = names
        return item


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size
