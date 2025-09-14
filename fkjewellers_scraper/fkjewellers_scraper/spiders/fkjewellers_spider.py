import scrapy
import json
from PIL import Image
import math


class FkjewellersSpiderSpider(scrapy.Spider):
    name = "fkjewellers_spider"
    start_urls = ['https://ae.fkjewellers.com/']
    file_headers = ['Url', 'Brand', 'Variant', 'SKU', 'In_Stock', 'Offer_Code', 'Product_Title', 'Product_Actual_Price',
                    'Product_Discounted_Price', 'Product_Url', 'Sizes', 'Weight', 'Karat', 'Purity', 'Diameter',
                    'Category', 'Price_Saving', 'Discount_Text',
                    'Model_Number', 'Image_Urls', 'names', 'Description', 'Feature_Bullets', 'Specifications']
    custom_settings = {'ROBOTSTXT_OBEY': False,
                       'RETRY_TIMES': 5,
                       'DOWNLOAD_DELAY': 1,
                       'CONCURRENT_REQUESTS': 5,
                       'FEED_URI': 'output/fkjewellers.xlsx',
                       'FEED_EXPORT_FIELDS': file_headers,
                       'FEED_FORMAT': 'xlsx',
                       'FEED_EXPORT_ENCODING': 'utf-8',
                       'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
                       'ITEM_PIPELINES': {"fkjewellers_scraper.pipelines.ImageScraperPipeline": 300},
                       'IMAGES_STORE': 'IMAGES',
                       }
    headers = {
        'authority': 'ae.fkjewellers.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': 'secure_customer_sig=; localization=AE; _cmp_a=%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22merchant_geo%22%3A%22AE%22%2C%22sale_of_data_region%22%3Afalse%7D; _y=b753a583-c121-4f87-8b45-4577ddf3b367; _s=6bfdf2aa-c71d-4ced-981a-20a2300e5807; _shopify_y=b753a583-c121-4f87-8b45-4577ddf3b367; _shopify_s=6bfdf2aa-c71d-4ced-981a-20a2300e5807; _orig_referrer=; _landing_page=%2F; _clck=24nchw|2|ffd|0|1365; _shopify_sa_p=; _gid=GA1.2.1860992030.1695801748; _gcl_au=1.1.400022713.1695801748; cart=c1-7bf69e6655f0ca89b2dd52093570b6d4; _fbp=fb.1.1695801749488.1459596966; cart_sig=0a00704be386ee93760b742c32032864; _shopify_sa_t=2023-09-27T09%3A05%3A35.439Z; _clsk=1vyldl3|1695805536121|47|1|u.clarity.ms/collect; _ga_YJPTKCNS92=GS1.1.1695801750.1.1.1695805536.0.0.0; _ga=GA1.1.111776215.1695801748; cart_ts=1695805536; keep_alive=ffbb3e59-87b4-472a-b194-e98cbe074602; _ga_LZ2CY286G3=GS1.2.1695801750.1.1.1695805540.60.0.0',
        'dnt': '1',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }
    Image.MAX_IMAGE_PIXELS = 1000000000

    def parse(self, response, **kwargs):
        categories_urls = response.xpath("(//ul[@class='megamenu slide'])[1]/li[position()>=last()-7]/a/@href").getall()
        for category_url in categories_urls:
            category_url = category_url.split('?constraint')[0]
            yield response.follow(url=category_url, headers=self.headers, callback=self.listing,
                                  meta={'page': 1, 'url': 'https://ae.fkjewellers.com/' + category_url})

    def listing(self, response):
        listing_urls = response.css("h3[data-product-type='title']::attr(data-href)").getall() or response.css(
            "div#sandbox>div>div>div div.name>a::attr(href)").getall()
        if listing_urls:
            for url in listing_urls:
                yield response.follow(url=url, headers=self.headers, callback=self.detail_page)
            page = response.meta['page'] + 1
            yield scrapy.Request(url=response.meta['url'] + '?page={}'.format(page), headers=self.headers,
                                 callback=self.listing, meta={'page': page, 'url': response.meta['url']})

    def detail_page(self, response):
        print(response.url)
        item = dict()
        item['Category'] = ' > '.join(response.css("div.breadcrumb-content>ul>li span::text").getall())
        json_script = response.css('script#ProductJson-product-template::text').get('')
        json_data = json.loads(json_script)
        item['Url'] = json_data.get('handle', '')
        item['Weight'] = ''.join(response.xpath(
            "//ul[@class='short-desc']/li[contains(text(),'Weight') or contains(text(),'Grams')]/following-sibling::li//text()").getall()).strip()
        item['Karat'] = ''.join(response.xpath(
            "//ul[@class='short-desc']/li[contains(text(),'Karat')]/following-sibling::li//text()").getall()).strip()
        item['Purity'] = ''.join(response.xpath(
            "//ul[@class='short-desc']/li[contains(text(),'Purity')]/following-sibling::li//text()").getall()).strip()
        item['Sizes'] = ''.join(response.xpath(
            "//ul[@class='short-desc']/li[contains(text(),'Size')]/following-sibling::li//text()").getall()).strip()
        item['Diameter'] = ''.join(response.xpath(
            "//ul[@class='short-desc']/li[contains(text(),'Diameter')]/following-sibling::li//text()").getall()).strip()
        item['Brand'] = ''.join(
            response.xpath("//td[contains(text(),'Brand')]/following-sibling::td//text()").getall()).strip()
        table = response.css('table.prod-desc tr')
        item['Product_Url'] = response.url
        description = []
        for tr in table:
            field = tr.css("td:first-child::text").get('').strip()
            if field:
                value = ''.join((tr.css("td:last-child ::text").getall())).strip()
                des = field + ':     ' + value
                description.append(des)
        item['Description'] = '\n'.join(description)
        images = []
        image_urls = response.css('div.thumbnails>div::attr(data-href)').getall()
        for image in image_urls:
            if not image.startswith('http'):
                image = 'https:{}'.format(image)
            images.append(image)
        item['image_urls'] = images
        item['Image_Urls'] = ','.join(images)
        variant = json_data.get('variants', [])
        price = json_data.get('price', '')
        compare_at_price = json_data.get('compare_at_price', '')
        if len(variant) > 1:
            item['Variant'] = '\n'.join(['title: ' + variant.get('title', '') +
                                         ', price: ' + str(variant.get('price', '')) +
                                         ', weight: ' + str(variant.get('weight', '')) +
                                         ',SKU: ' + variant.get('sku', '')
                                         for variant in json_data.get('variants', [])])
            price = variant[0].get('price', '')
            compare_at_price = variant[0].get('compare_at_price', '')
        title = json_data.get('title', '')
        item['Product_Title'] = title
        item['Product_Actual_Price'] = price / 100
        item['Product_Discounted_Price'] = price / 100
        item['Price_Saving'] = ''
        item['Discount_Text'] = ''
        if compare_at_price:
            item['Product_Actual_Price'] = int(compare_at_price / 100)
            item['Price_Saving'] = math.ceil(int(compare_at_price - price) / 100)
            discount = math.ceil(((compare_at_price - price) / compare_at_price) * 100)
            if discount != 0:
                item['Discount_Text'] = str(discount) + '%Off'
        item['SKU'] = title.split('-')[-1].strip()
        item['In_Stock'] = json_data.get('available', '')
        yield item
