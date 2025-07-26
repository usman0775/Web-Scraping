import re
import scrapy


class AaepaSpiderSpider(scrapy.Spider):
    name = "aaepa_spider"
    start_urls = ["https://aaepa.com/member-listing/search-results/?state=&text-search="]
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 5,
        'DOWNLOAD_DELAY': 1,
        'RETRY_TIMES': 5,
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        'FEEDS': {'output/aaepa_data.xlsx': {'format': 'xlsx', 'overwrite': True}},
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_GZIP': True

    }
    headers = {
        'authority': 'aaepa.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': 'TOSpop-up=disable',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://aaepa.com/member-listing/',
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
        yield scrapy.Request(url=self.start_urls[0], headers=self.headers)

    def parse(self, response, **kwargs):
        for url in response.css("ul.geodir_category_list_view>li h3.geodir-entry-title>a::attr(href)").getall():
            yield response.follow(url=url, headers=self.headers, callback=self.detail_page)

    def detail_page(self, response):
        addresses = []
        for address in response.xpath("//div[@class='location']/ul[position() > 1]"):
            phone = address.xpath(".//a[contains(@href,'tel')]/text()").get('').strip()
            if phone:
                addresses.append(re.sub(r'\s+', ' ', ' '.join(
                    address.xpath("./li[not(@class)]/span[not(a)]//text()").getall()).split(phone)[0]).strip())
            else:
                addresses.append(re.sub(r'\s+', ' ', ' '.join(
                    address.xpath("./li[not(@class)]/span[not(a)]//text()").getall()).split('Google Map')[0]).strip())
        pphone = response.xpath("(//a[contains(@href,'tel:')])[1]/text()").get('').strip()
        if pphone:
            paddress = re.sub(r'\s+', ' ', ' '.join(
                response.xpath("//div[@class='location']/ul[1]/li[not(@class)]/span[not(a)]//text()").getall()).split(pphone)[0]).strip()
        else:
            paddress = re.sub(r'\s+', ' ', ' '.join(
                response.xpath("//div[@class='location']/ul[1]/li[not(@class)]/span[not(a)]//text()").getall()).split('Google Map')[0]).strip()
        yield {
            'Name': response.css("h1.entry-title::text").get('').strip(),
            'Email': response.css("a[href*=mailto]::attr(href)").get('').split('mailto:')[-1].strip(),
            'Website': response.css("div.websiteurl>a::attr(href)").get('').strip(),
            'Firm Name': response.css("span.firm-name>strong::text").get('').strip(),
            'Primary Office Phone': pphone,
            'Additional Office Phone': ' || '.join(
                response.xpath("(//a[contains(@href,'tel:')])[position()>1]/text()").getall()).strip(),
            'Primary Office Address': paddress,
            'Additional Office Address': ' || '.join(addresses),
            'Member Firm Since': response.xpath("//span[contains(.,'Member Firm Since')]/text()").get('').strip(),
            'Academy Designations': response.xpath("//span[contains(.,'Academy Designations')]/text()").get('').strip(),
            'About Firm': ' '.join(response.css("div.entry-content ::text, div.about-company ::text").getall()).strip(),
            'Lawyer image': response.css("div.featured_image_prac>img::attr(src)").get('').strip(),
            'Page URL': response.url
        }
