import scrapy


class ApoteaSpiderSpider(scrapy.Spider):
    name = "apotea_spider"
    start_urls = ["https://www.apotea.se"]
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'RETRY_TIMES': 5,
        'CONCURRENT_REQUESTS': 1,
        'FEEDS': {'output/apotea_data_final.csv': {'format': 'csv', 'overwrite': True}},
        "ZYTE_API_EXPERIMENTAL_COOKIES_ENABLED": True,
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        'DOWNLOADER_MIDDLEWARES': {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
        },
        'REQUEST_FINGERPRINTER_CLASS': "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        'ZYTE_API_KEY': "please enter you api key here",
        "ZYTE_API_TRANSPARENT_MODE": True,
    }
    headers = {
        'authority': 'www.apotea.se',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': 'shopper=41e2314a-987d-470b-ba01-1dca320b671c; _culture=sv; rc=1; cc_cookie={"level":["necessary","analytics","marketing"],"revision":0}; _gcl_au=1.1.595182694.1701349380; _ga=GA1.1.1567254372.1701349355; FPID=FPID2.2.nkfkXnFxG4yaDKbmxneklEfp3WtsJ8VMW7kRnygRy24%3D.1701349355; FPAU=1.1.595182694.1701349380; FPLC=3kaKN7rYBs4ZNzYZJ2OqNIEWFyBua5AM%2BXAG3emn9QNmAU2A88b0cUIG7Fz%2FNJrz4xQTD4rcqyqqxwKE2LSMCl7%2BgPPpqMk7aRddA6QWyxy7%2F61QKtoZHdw1xE5T8g%3D%3D; imbox={"imboxUid":"2YtecboRkg9hbjEcfC79ceWAdUu"}; selected-view-type=double; cf_clearance=LRFRHDKqjWXv4LxtX0yg4U70BuMk__x_qqN_ynJsfk4-1701351636-0-1-9daecaaa.dc3db4c8.caaf954a-150.0.0; ASP.NET_SessionId=01uequasxpci3pw3rjysyjoa; _uetsid=df48faa08f8011eea2932ddee711e279; _uetvid=df4947a08f8011eeaecc5bacd36be156; _ga_RL16N5C15T=GS1.1.1701349354.1.1.1701351698.0.0.0',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://www.apotea.se/foralder-barn',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=self.headers, meta={"zyte_api": {"browserHtml": True,
                                                                                              "geolocation": "US"}})

    def parse(self, response, **kwargs):
        for top_category in response.css("div#sidebar-categories>div>a, div#sidebar-categories>div>div>a"):
            top_category_url = top_category.css("::attr(href)").get('').strip()
            yield response.follow(url=top_category_url, headers=self.headers, callback=self.listing_page,
                                  meta={"zyte_api": {"browserHtml": True, "geolocation": "US"}})

    def listing_page(self, response):
        for url in response.css("div.article-list-responsive>div div.name>a::attr(href)").getall():
            yield response.follow(url=url, headers=self.headers, callback=self.detail_page,
                                  meta={"zyte_api": {"browserHtml": True, "geolocation": "US"}})
        next_page = response.xpath(
            "//li[contains(@class,'arrow-btn') and not(contains(@class,'hidden'))][not(following-sibling::li)]/a/@href").get(
            '').strip()
        if next_page:
            yield response.follow(url=next_page, headers=self.headers, callback=self.listing_page,
                                  meta={"zyte_api": {"browserHtml": True, "geolocation": "US"}})

    def detail_page(self, response):
        item = dict()
        item['Name'] = response.css("h1#product-name::text").get('').strip()
        item['Price'] = response.css("div#price-info>span::text").get('').strip()
        item['Old Price'] = response.css("div.before-price::text").get('No').rsplit(':')[-1].strip()
        item['In stock'] = ''.join(response.xpath("//div[@id='stock-info']//span//text()").getall()).strip()
        item['Beskrivning'] = '\n'.join(response.xpath("//div[@id='product-description']//text()").getall()).strip()
        item['Dosering & användning'] = '\n'.join(
            response.xpath("//div[@id='product-dosage']//text()").getall()).strip()
        item['Product Image URL'] = ' , '.join(response.css("div#gallery>a::attr(href)").getall()).strip()
        item['categories'] = response.xpath(
            "//div[@id='product-facts']//div[@class='key' and contains(.,'Kategori:')]/following-sibling::div[@class='value'][1]//text()").getall()
        item['facts'] = ''
        try:
            facts = dict()
            for spec in response.xpath("//div[@id='product-facts']//div[@class='key']"):
                facts[spec.xpath('./text()').get('').replace(':', '').strip()] = ''.join(
                    spec.xpath('./following-sibling::div[@class="value"][1]//text()').getall()).strip()
            item['facts'] = facts
        except:
            pass
        item['Page URL'] = response.url
        if 'Kategori' in item:
            item.pop('Kategori')
        yield item
