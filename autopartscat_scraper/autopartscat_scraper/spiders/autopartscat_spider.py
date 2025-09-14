import re

import scrapy
from scrapy.utils.response import open_in_browser


class AutopartscatSpiderSpider(scrapy.Spider):
    name = "autopartscat_spider"
    start_urls = ["https://example.com"]
    custom_settings = {'ROBOTSTXT_OBEY': False,
                       'RETRY_TIMES': 5,
                       'CONCURRENT_REQUESTS': 3,
                       'FEEDS': {'output/autopartscat3.csv': {'format': 'csv'}},
                       'FEED_EXPORT_ENCODING': 'utf-8',
                       'DOWNLOAD_DELAY': 0.5,
                       'IMAGES_STORE': 'images',
                       'ITEM_PIPELINES': {'autopartscat_scraper.pipelines.MyImagesPipeline': 300}
                       # 'DOWNLOAD_HANDLERS': {
                       #     "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
                       #     "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
                       # },
                       # 'DOWNLOADER_MIDDLEWARES': {
                       #     "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
                       # },
                       # 'REQUEST_FINGERPRINTER_CLASS': "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
                       # 'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
                       # 'ZYTE_API_KEY': "b30c393ec17f4cb591cf5db33e62ec40",
                       # "ZYTE_API_TRANSPARENT_MODE": True,
                       }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'ARRAffinity=132c4094174e7a951c55c033ca04ea3ebfca6e0553c9b2a2ff1aadef48825802; ASP.NET_SessionId=ytwtfxgj3khfqpzc1jtidujr; VWANLuserInfo=carAmarqu1=11A1&carBrand1=ABARTH&carType1=500,595    -15&carImage1=https://images.autopartscat.com/catalogic/i0180000.jpg&lastVisit1=30/11/2023 9:35:47&carAmarqu2=1001&carBrand2=.UNIVERSAL&carType2=HAGUS&carImage2=https://images.autopartscat.com/catalogic/i9900001.jpg&lastVisit2=30/11/2023 9:33:03',
        # 'Referer': 'https://www.fiverr.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    url = 'https://vwa.autopartscat.com/pgm.NET/Account/Home.aspx?enc=Y2F0YWxvZz1WV0E='

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse, headers=self.headers)

    def parse(self, response, **kwargs):
        data = {
            '__LASTFOCUS': '',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwUKMTk1MjM2NzAyMQ9kFgJmD2QWAgIDDxYEHgZvbmxvYWQFJmRpc2FibGVCYWNrQnV0dG9uKCk7IHJlZGlyZWN0VG9QYWdlKCk7HgpvbnBhZ2VzaG93BSdpZihldmVudC5wZXJzaXN0ZWQpZGlzYWJsZUJhY2tCdXR0b24oKTsWAmYPZBYCAgEPZBYEAgEPZBYEAgMPEA8WAh4LXyFEYXRhQm91bmRnZBAVBgJubAJmcgJlbgJkZQJpdAJlcxUGAm5sAmZyAmVuAmRlAml0AmVzFCsDBmdnZ2dnZxYBZmQCCQ8PFgIeB1Zpc2libGVoZGQCAw9kFgICAQ9kFgQCAQ9kFgICAQ9kFgxmDw8WAh8DaGRkAgEPDxYCHwNoZGQCAg8PFgIfA2hkZAIDDw8WAh8DaGRkAgQPDxYCHwNoZGQCBQ8PFgIfA2hkZAIFDw8WBB4IQ3NzQ2xhc3MFI2JhY2tncm91bmRfaG9tZSBiYWNrZ3JvdW5kX25vc2Nyb2xsHgRfIVNCAgJkZBgBBRRjdGwwMCROYXZpZ2F0aW9uTWVudQ8PZAUESG9tZWTPsL+P4Jyze7qabdR3QLhvV3cF+A==',
            '__VIEWSTATEGENERATOR': '933C8FC1',
            '__EVENTVALIDATION': '/wEdAAzbeCjSia1Pxj+HdX4Ej73s9ujVgWofHonLQRvGjKwIT5royTR6og+DOGn4EWS5DyRaFF6pnn60VeVIGNG9t6UUZwsA71k6QpYzl7Dn4ThRntYsWmWCxMvyCgTQ04iUqvTpUgSw5VSzWQ3kRD7k1K0FZnon2Imyf46B7PVi6ekvFK1Scw/XqbYRpjlq3MVyj+7tb6rsnAf7OviCSWuIYHfoCQtH8leGQTiMCnhMu4O3EW0Fr8yIsd4HO1/NkIALxMPbvtZ61ZtVEzT49hgX7wZP8jYLsg==',
            'ctl00$RadioButtonList1': 'nl',
            'ctl00$MainContent$LoginUser$UserName': '268188',
            'ctl00$MainContent$LoginUser$Password': '7242',
            'ctl00$MainContent$LoginUser$LoginButton': 'Log In',
        }
        url = 'https://vwa.autopartscat.com/pgm.NET/Account/Home.aspx?enc=Y2F0YWxvZz1WV0E%3d'
        yield scrapy.FormRequest(url=url, formdata=data, headers=self.headers, callback=self.parse_dashboard)

    def parse_dashboard(self, response):
        catalog_url = response.xpath("//a[@title='Catalogus']/@href").get('')
        yield scrapy.Request(url=response.urljoin(catalog_url), callback=self.parse_catalog, headers=self.headers)

    def parse_catalog(self, response):
        brands = response.xpath(
            "//select[@id='MainContent_tree_treemenu1_brands']/option[not(text()='.UNIVERSAL') and not(@selected)]")
        for brand in brands[6:]:
            brand_name = brand.xpath("./text()").get('')
            brand_value = brand.xpath("./@value").get('')
            data = {
                '__EVENTTARGET': 'ctl00$MainContent$tree$treemenu1_brands',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': '/wEPDwUKLTk3MTEwMDUxOA9kFgJmD2QWAgIDDxYEHgZvbmxvYWQFJmRpc2FibGVCYWNrQnV0dG9uKCk7IHJlZGlyZWN0VG9QYWdlKCk7HgpvbnBhZ2VzaG93BSdpZihldmVudC5wZXJzaXN0ZWQpZGlzYWJsZUJhY2tCdXR0b24oKTsWAmYPZBYCAgEPDxYEHghDc3NDbGFzcwUScGFnZSBmaXhlZHBhZ2VzaXplHgRfIVNCAgJkFgQCAQ9kFgICAw8QDxYCHgtfIURhdGFCb3VuZGdkEBUCAm5sAmVuFQICbmwCZW4UKwMCZ2cWAWZkAgMPDxYEHwIFEm1haW4gZml4ZWRtYWluc2l6ZR8DAgJkFgICAQ9kFh4CAQ8PFgQfAgUSdHJlZSBmaXhlZG1lbnVzaXplHwMCAmQWAgIBD2QWAmYPZBYGAgEPDxYCHgdWaXNpYmxlZ2RkAgMPDxYCHwVnZBYGAgEPZBYCZg9kFgJmDw9kFgQeB29uZm9jdXMFGGphdmFzY3JpcHQ6dGhpcy5zZWxlY3QoKR4KT25LZXlQcmVzcwV4amF2YXNjcmlwdDpzZWFyY2hfYXJ0aWNsZTEoJ2N0bDAwJE1haW5Db250ZW50JHRyZWUkYnRuU2VhcmNoQXJ0aWNsZScsICdjdGwwMCRNYWluQ29udGVudCR0cmVlJHR4dFNlYXJjaEFydGljbGUnLCBldmVudCk7ZAICD2QWAmYPZBYCZg8QZA8WAmYCARYCBQxWV0EgLSBOdW1tZXIFC09FIC0gTnVtbWVyFgFmZAIDD2QWAmYPZBYCZg8PFgIeBFRleHQFBlpvZWtlbmRkAgcPZBYCAgEPZBYCZg9kFgJmD2QWAgIBDxAPFgIfBGdkEBUCB0tvcnRpbmcQS29ydGluZyBncm9zc2llchUCBXByaWNlBnByaWNlMhQrAwJnZxYAZAICDw8WAh8FZ2RkAgQPZBYCAgEPDxYCHwVoZGQCBQ9kFgQCAQ8PFgIfCAUFTW90b3JkZAIHDw8WAh8IBQZGaWx0ZXJkZAIGDw8WBB8CZR8DAgJkZAIHDw8WBB8CZR8DAgJkZAILDw8WAh8IBQtBcnRpa2VsbnIuOmRkAgwPDxYCHwgFDUJlc2NocmlqdmluZzpkZAINDw8WAh8IBR1WZXJ2YW5nZGVlbDxici8+cGFzc2VuZCB2b29yOmRkAg4PDxYCHwgFCUNyaXRlcmlhOmRkAg8PDxYCHwgFC0luYmVncmVwZW46ZGQCEA8PFgIfCAUOT29rIGxldmVyYmFhcjpkZAIRDw8WAh8IBQdFQU4gMTM6ZGQCEg8PFgIfCAUNR2V3aWNodCAoa2cpOmRkAhMPDxYCHwgFEFZlcnBha2tpbmcgKGNtKTpkZBgEBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUYY3RsMDAkbG9naW5fc3RhdHVzJGN0bDAxBRhjdGwwMCRsb2dpbl9zdGF0dXMkY3RsMDMFJmN0bDAwJE1haW5Db250ZW50JHRyZWUkdHJlZW1lbnUxX3R5cGVzDw9kFgBkBSdjdGwwMCRNYWluQ29udGVudCR0cmVlJHRyZWVtZW51MV9icmFuZHMPD2QWAWZkBRRjdGwwMCROYXZpZ2F0aW9uTWVudQ8PZAUJQ2F0YWxvZ3VzZL8ISmQsXad6gK8Y8UEios3MEPc/',
                '__VIEWSTATEGENERATOR': '32C7FC91',
                '__EVENTVALIDATION': '/wEdAEWD6b6WOcZkiUGcrJUNgNcH9ujVgWofHonLQRvGjKwIT1oUXqmefrRV5UgY0b23pRRmeifYibJ/joHs9WLp6S8UbNwd0OMs5k3adfrEhj+WqRYty9LAgvBaZiOS+X9RS5jCmZOiGaFpxZFeoMGR0jOuSBKgAMD96+leGQotcAGK1ZDsFJnV0pNQRc/TJXzo7j158BOxIwRAsP2pTka0a/ZkLR6rpvMErxibrVfViA7U4Y6QC7ZX2VClq/V0II8dgJIb+7FnaTOII6cpfa2vkBx8swJ5mSk5uq8mDHJg4WgU13H0/dCG2gqIpRf8zDaSWKeRvFAOb0Yb5gGxkFbISzfFXJy9LBQRi6UaYNWIMZLnErLMM6PbHT6ARHngGF6VwprwE5p112ndU2th2qSCN1HJdtSPkOj1swPi30RGEccwgfKnpOEHOMCJ4AZT5RYvzeQstqUS6/o7sLND2A5FcMLhk/qz6lWbSx33rICbRYQhd2muE61p5AjjBSMAOQCYrksTe8r0ISvpHCfz9OqGO7r2gtuUdD7tCP/it9TukGnfXM7qsKNPP8Rjyei3QFx8aJ9K5FnUQsN42hmabCj5jIf4//hv9LVpixkAXIVkEpbhU0YTmsoWx0MnJkXYJyY6FvvbyE+w3P3l7CW6TspnXZFVCdrXhiudQ0X9gcQBO7ge44DMo+ePbUE3m6+9MYvyL2JTq8FrOHPo6rOcuvfLFi4REhCaMKy4CX0omkUem/BcVFormoZ7N/7E61yz/X6aA/PgQYics2eTkyqxXMaUJuuqskR+FDUgQA08b0h0WRKjKSDYp+6IapwB+MxmwZp8dM/T5JVkI8E8FcSMALqyd6L26qWSbBlprh4ab2DaxhhwXb7Q5eHKcoYmDozoDlHY10H/cuflCU84FtnqYSOreYhSPi+ROQcOZXK4CbZz09B/bC4J7vJWtX1MajR34MTamYNgV4ikBBD7V6CpMnnGfQokny9B24x35f1zFfVbRjtOW5LGhwDGEno8/bNL2m+aOZfV1JTgL1SliYisTjS9AbWeF07ecYSrDk9ZweilySEIqdP05WVbYn+D/ZBhS4pg9zqTsLCbQLI6c/BAn9tJtQw1cQo3t+Quqrah/AfJmC/KlCzc0fZfwbGniqe/PCl9ENCnfR7TIsjXWyeFMyo4E2QFqA4Ot7OGYpKSoEfHENTSonBlhfqhD08Xt8mwDNnx83a0c2IoaoVElx0tBkePU0C7pe6YzzkzdLt2Tw7CTQMIJqSicRSPVbDz1Yy9b5Irjs/IjZOU0mFCkn7bTazVWS7zVZnwn94UsTYoLJ5yDsxElM/w8c7JAra8oDBzf3HZMVGxpMpz/E6U00eryAvRhQehOg1ZDrSi5D04Gnu/+beonGA9QUpFDi0awPzf/vi8MZIwizCSFPNGGxDSS+R7uLV52pq8HHpRT9KIkA/oS5vthRCi+nIM23BwmHeUQes3Dbz1l/4BN6/ytMWPvqfnrsLdEH4cuQ==',
                'ctl00$RadioButtonList1': 'nl',
                'ctl00$MainContent$tree$treemenu1_brands': brand_value,
                'ctl00$MainContent$tree$treemenu1_types': 'start',
                'ctl00$MainContent$tree$txtSearchArticle': '',
                'ctl00$MainContent$tree$searchoption': '0',
            }
            yield scrapy.FormRequest(url=response.url, formdata=data, headers=self.headers,
                                     callback=self.parse_categories, meta={'brand_name': brand_name})

    def parse_categories(self, response):
        categories = response.xpath("//table[@id='MainContent_showroom_tbl_images']/tr/td/a")
        for categories in categories:
            category_name = categories.xpath("./span/text()").get('')
            categories_url = categories.xpath("./@href").get('')
            meta = {'brand_name': response.meta['brand_name'], 'category_name': category_name}
            yield scrapy.Request(url=response.urljoin(categories_url), callback=self.parse_sub_categories,
                                 headers=self.headers, meta=meta)

    def parse_sub_categories(self, response):
        sub_categories = response.xpath(
            "//div[@id='MainContent_thumbbarpanel']/table/tr/td[@class='thumb']/a")
        for subcategories in sub_categories:
            subcategory_url = subcategories.xpath("./@href").get('')
            yield scrapy.Request(url=response.urljoin(subcategory_url), callback=self.parse_listing,
                                 headers=self.headers, meta=response.meta)

    def parse_listing(self, response):
        products = response.xpath(
            "//table[@id='allproducts']/tr[not(contains(td/text(),'Afbeelding')) and not(contains(td/@class,'table-separator'))]")
        for product in products:
            item = dict()
            item['Merken'] = response.meta['brand_name']
            item['Types'] = response.meta['category_name']
            item['Image URL'] = [product.xpath("./td[2]/img/@src").get('').strip()]
            item['Serial Number'] = product.xpath("./td[4]/div/a/text()").get('').strip()
            item['Description'] = '\n'.join(product.xpath("./td[8]/text()").getall()).strip()
            prices = product.xpath("./td[10]/table//tr/td/text()").getall()
            for index, price in enumerate(prices, start=1):
                item[f'Price {index}'] = price.strip()
            yield item
