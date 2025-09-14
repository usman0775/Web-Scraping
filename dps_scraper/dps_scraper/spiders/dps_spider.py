import scrapy
import json

from scrapy.utils.response import open_in_browser


class DpsSpiderSpider(scrapy.Spider):
    name = "dps_spider"
    start_urls = ["https://documents.dps.ny.gov/public/CompanyMaster/EscoCompanies/?_=1697875995828"]
    fields = ['ESCO Company Name', 'Address', 'Phone', 'Fax', 'Email', 'Website', 'Commodity', 'Territory',
              'Service Class']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'RETRY_TIMES': 5,
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1,
        'FEEDS': {'OUTPUT/DPS_data_new.csv': {'format': 'csv', 'overwrite': True, 'fields': fields}}
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'ASP.NET_SessionId=diccn2p2eunhhmqeqkrotw5i; _ga=GA1.1.1570575227.1697874572; _ga_V4T04B1VEN=GS1.1.1697874572.1.0.1697874572.0.0.0; _ga=GA1.4.1570575227.1697874572; _gid=GA1.4.87967625.1697874575; nmstat=f7b49115-4908-8798-e39c-f8b1c12e885b',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=self.headers)

    def parse(self, response, **kwargs):
        # open_in_browser(response)
        companies_list = json.loads(response.body)
        for company in companies_list:
            contact_html = company.get('Contact', '')
            item = dict()
            item['ESCO Company Name'] = company.get('ESCOCompanyName', '').strip()
            item['Address'] = company.get('Address', '')
            item['Commodity'] = scrapy.Selector(text=company.get('Commodity', '')).css("td::text").get('')
            item['Territory'] = ' || '.join(scrapy.Selector(text=company.get('Territory', '')).css("td::text").getall())
            item['Service Class'] = ' || '.join(scrapy.Selector(text=company.get('ServiceClass', '')).css("td::text").getall())
            if contact_html:
                html = scrapy.Selector(text=contact_html)
                if 'Phone:' in contact_html:
                    item['Phone'] = contact_html.split('<br')[0].split('Phone:')[-1].strip()
                if 'Fax:' in contact_html:
                    item['Fax'] = contact_html.split('Fax:')[-1].split('<br')[0].strip()
                item['Email'] = html.css("a[href*=mail]::text").get('').strip()
                item['Website'] = html.css("a[href*=http]::text").get('').strip()
            yield item
