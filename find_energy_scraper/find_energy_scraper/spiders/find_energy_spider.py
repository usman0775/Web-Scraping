import requests
import scrapy
from datetime import datetime
from scrapy import signals


class FindEnergySpiderSpider(scrapy.Spider):
    name = "find_energy_spider"
    start_url = "https://find-energy-certificate.service.gov.uk/find-a-certificate/search-by-postcode?postcode={}"
    current_timestamp = datetime.now().strftime(f"Date %Y_%m_%d Time %Hh_%Mm")
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 1,
        'RETRY_TIMES': 5,
        'DOWNLOAD_DELAY': 2,
        'FEEDS': {f"outputs/{name.replace('_spider', '')}_{current_timestamp}.json": {'format': 'json'}},
    }
    headers = {
        'accept-language': 'en-US,en;q=0.9',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    count = 0
    items = []
    with open('postal_codes.txt', 'r', encoding='utf-8') as file:
        records = [i.strip() for i in file.readlines()]

    def start_requests(self):
        yield scrapy.Request(url='https://www.example.com', headers=self.headers)

    def parse(self, response, **kwargs):
        for url in response.css('tbody.govuk-table__body tr a::attr(href)').getall():
            yield response.follow(url, headers=self.headers, callback=self.parse_detail)

    def parse_detail(self, response):
        item = dict()
        item['URL'] = response.url
        item['Name'] = response.xpath(
            '(//h3[contains(.,"Contacting the assessor")]/following-sibling::dl//dt[contains(text(),"Assessor’s name")]/following-sibling::dd/text())[1]').get(
            '').strip()
        item['Telephone'] = response.xpath(
            '(//h3[contains(.,"Contacting the assessor")]/following-sibling::dl//dt[contains(text(),"Telephone")]/following-sibling::dd/text())[1]').get('').strip()
        item['Email'] = response.xpath(
            '(//h3[contains(.,"Contacting the assessor")]/following-sibling::dl//dt[contains(text(),"Email")]/following-sibling::dd/a/text())[1]').get('').strip()
        item['Agency'] = response.xpath('//dt[contains(.,"Accreditation scheme")]/following-sibling::dd/text()').get('').strip()
        self.items.append(item)
        self.count += 1
        print("Total scraped items:  ", self.count)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(FindEnergySpiderSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self, spider):
        if self.items:
            url = "https://push.slatermarketing.co.uk/webhook/fd59bc55-d259-43b1-8d97-234d2824b1e5"
            response = requests.post(url, json=self.items)
            print(f"Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            print(len(self.items))
            self.items = []
        if self.records:
            postcode = self.records.pop(0)
            try:
                self.crawler.engine.crawl(scrapy.Request(url=self.start_url.format(postcode), headers=self.headers))
            except:
                pass
