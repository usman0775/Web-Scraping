import scrapy


class EbaySpiderSpider(scrapy.Spider):
    name = "ebay_spider"
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        'FEEDS': {'output/ebay_data_1sample.xlsx': {'format': 'xlsx'}}
    }
    headers = {
        'authority': 'www.ebay.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': '__uzma=22bbe1a2-d042-4598-ac3b-7ec8108ced92; __uzmb=1704527666; __uzme=1435; ak_bmsc=D85E2BACB5AF29AD5937D3D14DAD788F~000000000000000000000000000000~YAAQPts4fakYT9iMAQAA7x/E3RbyJkCc0XMQS3Sz50gRZLWcJzKNnACzG1yTjFer68G3Lt5KS1ItN+KXrWpU7BWdkNlgmIP3g/d5ChhLQYsJbzS/a7amC+b/sZeQ3OMSPEt51Se0L5XFeAE8q4+Iz1NXJcgXUilBEWXtpkLON2cUZFLj4zg92J4VJKZKKhmuXn8ErEY9bKO4vRigyym6ykq8WuRcya6OkiIQemL3qmiGk0WsD5HFfAKyQ6VlRx8PW3BLswVby6ucSzlLPbYGIQCPJ6IDfmt+f0iALiPgwWJ+Q3BJdaqj3IFardgUTKmk6luJHotzB2usB+faMmIeahbd3YoEy1ZGd67Du+I2Sc1Q0EsmQ9CKShNUg+2ZatxcpQhAO3vs; __ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=f8af1bbf-bebb-4d82-9995-f2d4791962c7; __uzmbj2=1704527668; __uzmc=121151689863; __uzmd=1704527898; __uzmf=7f6000dca5b1a2-24af-41ee-842a-3e842d3e79b01704527666805231254-1954edeee2a3703e16; ds2=; s=CgAD4ACBlmlmcZGRjNDFlYjYxOGMwYWRlZTNjYjA2OTM3ZmZmZDM0ZjK2bMq2; bm_sv=54FE037BA64FBEB4405A8A40C18958FC~YAAQPts4fRGkT9iMAQAAhOfH3Ra789OuyJLEi2kaO7q9avNVqmihzYPyBm96PfrmxCSE+SUFnxezC7QSOqrkhWghx0X0C/z0XDYVzXRCJxIhnWu9KPS7lmEcRKpCQ3Ecb1Y3o/vlGxmopPObd4H/b6J08F14ZbMgq8iNW/hG0f3OM7lrzqTA2p6jJsoJ8EECc8wB+rKKx1bzGJmL6c4t5qCj0i9l3xsXCtr7H+LTDFOuZHThD/geOcaxH+Qm~1; dp1=bbl/PK695b6f2b^; ns1=BAQAAAYxL36hOAAaAANgAU2d6O6tjNjl8NjAxXjE3MDQ1Mjc2NjcwMzheXjFeM3wyfDV8NHw3fDEwfDQyfDQzfDExXl5eNF4zXjEyXjEyXjJeMV4xXjBeMV4wXjFeNjQ0MjQ1OTA3NThAWz3N1y9HY0J4qdfZugtdYiSG; __uzmcj2=876372276989; __uzmdj2=1704527915; nonsession=BAQAAAYxL36hOAAaAADMABWd6O6s0NzU4MADKACBpW28rZGRjNDFlYjYxOGMwYWRlZTNjYjA2OTM3ZmZmZDM0ZjIAywACZZkPMzE2KOu5v3423vZ4CCgeYlSL3PiLkIo*; __deba=TCTafNIucGYAxe43N_hYMkmm91GvbPFWtJp3Sd4K9JBIp1Lrclszy50cbdGmPHZCXR8UW1J2_XMwSXzXGqPFGMwwBdwrq89bDUsWyr9AwKlBycpzOBkY5nod7dsssUcPTEn0Kq2-O7G75UtLxhUDTw==; ebay=%5Ejs%3D1%5Esbf%3D%23000000%5Epsi%3DAx96Swz0*%5E',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-full-version': '"120.0.6099.130"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open('inputs/urls.txt', 'r') as file:
            self.urls = file.readlines()

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, headers=self.headers)

    def parse(self, response, **kwargs):
        for product in response.css("div#srp-river-main ul.srp-results>li div.s-item__info>a::attr(href)").getall():
            yield response.follow(product, callback=self.parse_detail_page, headers=self.headers)
        next_page = response.css("nav.pagination>a.pagination__next::attr(href)").get('').strip()
        if next_page:
            yield response.follow(next_page, headers=self.headers, callback=self.parse)

    def parse_detail_page(self, response):
        item = dict()
        item['Title'] = ' '.join(response.css("h1.x-item-title__mainTitle ::text").getall()).strip()
        item['Price'] = response.xpath(
            "//div[@class='x-label'][span[contains(text(), 'Prijs')]]/following-sibling::div/div[@class='x-price-primary']/span/text()").get(
            '').strip()
        item['Stock'] = response.css("div.d-quantity__availability>div>span:first-of-type::text").get('').strip()
        item['EAN/ISBN'] = response.xpath(
            "//div[@class='ux-labels-values__labels' and (contains(.,'EAN') or contains(.,'ISBN'))]/following-sibling::div//span/text()").get(
            '').strip()
        if not item['EAN/ISBN']:
            item['EAN/ISBN'] = response.xpath(
                "//dt[div[(contains(.,'EAN') or contains(.,'ISBN'))]]/following-sibling::dd//span/text()").get(
                '').strip()
        item['Condition'] = response.xpath(
            "//div[@class='x-item-condition-label' and contains(.,'Objectstaat')]/following::span[@class='ux-textspans'][1]/text()").get(
            '').strip()
        images = response.css("div.ux-image-carousel-item img")
        item['Image_URL'] = ' , '.join(images.css("::attr(src)").getall() + images.css("::attr(data-src)").getall())
        yield item
