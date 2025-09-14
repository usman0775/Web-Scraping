import json
import re

import pandas as pd
import scrapy
from scrapy.utils.response import open_in_browser


class EstateplanningSpiderSpider(scrapy.Spider):
    name = "estateplanning_spider"
    start_urls = ["https://www.estateplanning.com"]
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1,
        'RETRY_TIMES': 5,
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        'FEEDS': {'OUTPUT/estateplanning_data.xlsx': {'format': 'xlsx', 'overwrite': True}}
    }
    headers = {
        'authority': 'read-api.wealthcounsel.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://www.estateplanning.com',
        'referer': 'https://www.estateplanning.com/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    api_url = 'https://read-api.wealthcounsel.com/wco-read/staff'
    json_data = {
        'searchTerm': '',
        'state': '',
        'practiceAreas': '',
        'resultsPerPage': 3502,
        # 'resultsPerPage': 200,
        'site': 'ep.com',
        'page': 1,
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0])

    def parse(self, response, **kwargs):
        yield scrapy.Request(url=self.api_url, headers=self.headers, method='POST', callback=self.listing_page,
                             body=json.dumps(self.json_data))

    def listing_page(self, response):
        lst = json.loads(response.body).get('data', {}).get('results', [])
        final_list = []
        for item in lst:
            item['id'] = 'https://www.estateplanning.com/member/?id=' + item.get('id')
            bios = item.get('bio', '')
            if bios:
                bio = scrapy.Selector(text=bios)
                item['bio'] = re.sub(r'\s+', ' ', ' '.join(bio.xpath("//p//text()").getall()))
            item['practiceAreas'] = ' || '.join(item.get('practiceAreas', []))
            item['licensedStates'] = ' || '.join(item.get('licensedStates', []))
            item['specialtiesListedOnEP'] = ' || '.join(item.get('specialtiesListedOnEP', []))
            final_list.append(item)
        pd.DataFrame(final_list).to_excel('estateplanningsdfgh.xlsx', index=False)
