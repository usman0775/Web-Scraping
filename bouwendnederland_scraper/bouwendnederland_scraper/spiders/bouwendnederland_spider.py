import re

import scrapy


class BouwendnederlandSpiderSpider(scrapy.Spider):
    name = "bouwendnederland_spider"
    start_urls = ["https://www.bouwendnederland.nl/vereniging/lidbedrijf-zoeken"]
    custom_settings = {'ROBOTSTXT_OBEY': False,
                       'RETRY_TIMES': 5,
                       # 'DOWNLOAD_DELAY': 2,
                       'CONCURRENT_REQUESTS': 1,
                       "FEEDS": {'output/bouwendnederland.csv': {'format': 'csv', 'overwrite': True}}
                       }
    headers = {
        'authority': 'www.bouwendnederland.nl',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': 'ARRAffinity=9f138fe40e53e241408034e8cd47d4d452b331805ff6d9018b002451153e871e; ARRAffinitySameSite=9f138fe40e53e241408034e8cd47d4d452b331805ff6d9018b002451153e871e; _gid=GA1.2.534477619.1702108752; _hjFirstSeen=1; _hjIncludedInSessionSample_2024464=1; _hjSession_2024464=eyJpZCI6IjZkZWM3ZjAzLTAxNDItNDNlZi1iMGQ5LTE1MjZlNDlmOWRlZiIsImNyZWF0ZWQiOjE3MDIxMDg3NTIwODMsImluU2FtcGxlIjp0cnVlLCJzZXNzaW9uaXplckJldGFFbmFibGVkIjp0cnVlfQ==; CookieConsent={stamp:%2785fislGI0JWyr71WKM3r9iyxiI2lFxD09PKLM8VMm9SQVHHg9s1m1A==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1702108756205%2Cregion:%27pk%27}; _ga=GA1.2.779185611.1702108752; _hjSessionUser_2024464=eyJpZCI6IjY2MzA5ZmFmLTdmMDktNWRkMi1hNDkxLTIzYjRkMzQzOWU3YSIsImNyZWF0ZWQiOjE3MDIxMDg3NTIwODIsImV4aXN0aW5nIjp0cnVlfQ==; _ga_M93JV67PY7=GS1.2.1702108752.1.1.1702108758.0.0.0; _ga_GX8BSSQCH1=GS1.1.1702108751.1.1.1702108761.50.0.0',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://www.bouwendnederland.nl/vereniging/lidbedrijf-zoeken',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    url = "https://www.bouwendnederland.nl/vereniging/lidbedrijf-zoeken?page={}"

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=self.headers, meta={'page': 1})

    def parse(self, response, **kwargs):
        companies = response.css('div.c-grid>div.c-organisation')
        if companies:
            for company in companies:
                item = dict()
                item['Business Name'] = company.css('div h5::text').get('').strip()
                item['City'] = company.css('div h5+div::text').get('').strip()
                item['Street Name'] = company.css('div h6:contains("ostadres")+div::text').get('').strip()
                if item['Street Name']:
                    item['Street Number'] = re.findall(r'\d+', item['Street Name'])
                    if item['Street Number']:
                        item['Street Number'] = item['Street Number'][0].strip()
                        item['Street Name'] = item['Street Name'].replace(item['Street Number'], '').strip()
                item['State'] = company.css('div h6:contains("ostadres")~div:nth-of-type(2)::text').get('').strip()
                if item['State']:
                    item['Zip Code'] = re.findall(r'\d{4}', item['State'])
                    if item['Zip Code']:
                        item['Zip Code'] = item['Zip Code'][0].strip()
                        item['State'] = item['State'].replace(item['Zip Code'], '').strip()
                item['City2'] = company.css('div h6:contains("ostadres")~div:last-of-type::text').get('').strip()
                item['Postadres'] = ' '.join(company.css('div h6:contains("ostadres")~div::text').getall()).strip()
                item['Bezoekadres'] = ' '.join(company.css('div h6:contains("ezoekadres")~div::text').getall()).strip()
                item['Telephone'] = company.css('div h6:contains("Telefoon")+div::text').get('').strip()
                item['Website URL'] = company.css('div a[title*=website]::attr(href)').get('').strip()
                if not item['Website URL']:
                    item['Website URL'] = company.css('div a[title*=website]::text').get('').strip()
                item['Page URL'] = response.url
                yield item
            yield response.follow(url=self.url.format(response.meta['page'] + 1), headers=self.headers,
                                  callback=self.parse, meta={'page': response.meta['page'] + 1})
