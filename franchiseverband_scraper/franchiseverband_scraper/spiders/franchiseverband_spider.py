import json
import scrapy


class FranchiseverbandSpiderSpider(scrapy.Spider):
    name = "franchiseverband_spider"
    start_urls = ["https://www.franchiseverband.com/systeme-finden"]
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'RETRY_TIMES': 5,
        'CONCURRENT_REQUESTS': 5,
        'DOWNLOAD_DELAY': 1,
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        'FEEDS': {'output/franchiseverband_data.xlsx': {'format': 'xlsx', 'overwrite': True}}
    }
    headers = {
        'authority': 'www.franchiseverband.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': 'orejime={"essential":true,"google-analytics":true,"etracker-analytics":true}; _gid=GA1.2.645258726.1699715348; _ga=GA1.1.979310456.1699715348; _ga_55244SL2X0=GS1.1.1699727570.2.1.1699727755.58.0.0',
        'dnt': '1',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=self.headers)

    def parse(self, response, **kwargs):
        urls_list = json.loads(response.css("div#jsondata::attr(data-matrix)").get(''))
        for record in urls_list:
            url = record.get('detaillink', '').strip()
            yield response.follow(url=url, headers=self.headers, callback=self.detail_page)

    def detail_page(self, response):
        item = dict()
        item['Name'] = response.css("h1.heading--light::text").get('').split('-')[0].strip()
        item['Firma'] = response.css("span.fullcontact-companyname::text").get('').strip()
        name1 = response.css("span.fullcontact-1contactname::text").get('').strip()
        name2 = response.css("span.fullcontact-2ndcontactname::text").get('').strip()
        item['Ansprechpartner'] = name1 + ', ' + name2 if name2 else name1
        tel1 = response.css("span.fullcontact-1contactphone::text").get('').replace('Telefon', '').strip()
        tel2 = response.css("span.fullcontact-2ndcontactphone::text").get('').replace('Telefon', '').strip()
        item['Tel.-Nr. AP'] = tel1 + ', ' + tel2 if tel2 else tel1
        mob1 = response.css("span.fullcontact-1contactcellphone::text").get('').replace('Mobile', '').strip()
        mob2 = response.css("span.fullcontact-2ndcontactcellphone::text").get('').replace('Mobile', '').strip()
        item['Mob.-Nr. AP'] = mob1 + ', ' + mob2 if mob2 else mob1
        mail1 = response.css("span.fullcontact-1contactemail>a::attr(href)").get('').replace('mailto:', '').strip()
        mail2 = response.css("span.fullcontact-2ndcontactemail>a::attr(href)").get('').replace('mailto:', '').strip()
        item['E-Mail AP'] = mail1 + ', ' + mail2 if mail2 else mail1
        item['Straße + Hausnr.'] = response.css("span.fullcontact-companystreet::text").get('').strip()
        address = response.css("span.fullcontact-companyzip.fullcontact-companycity::text").get('')
        item['PLZ'] = address.split(' ', 1)[0].strip() if len(address) >= 1 else ''
        item['Stadt'] = address.split(' ', 1)[1].strip() if len(address) >= 2 else ''
        item['Tel.-Nr. Firma'] = response.css("span.fullcontact-companyphone::text").get('').replace('Telefon', '').strip()
        item['E-Mail Firma'] = response.css("span.fullcontact-companyemail>a::attr(href)").get('').replace('mailto:', '').strip()
        item['F-Partner (DE)'] = response.css("div.data-countfranchisee>span:last-of-type::text").get('').strip()
        item['Standorte (DE)'] = response.css("div.data-countlocations>span:last-of-type::text").get('').strip()
        item['F-Partner (Int.)'] = response.css("div.data-int_franchise>span:last-of-type::text").get('').strip()
        item['Standorte (Int.)'] = response.css("div.data-int_locations>span:last-of-type::text").get('').strip()
        item['URL_1'] = response.css("span.fullcontact-companyurl>a::attr(href)").get('').strip()
        item['URL_2'] = response.css("span.fullcontact-companyurl2>a::attr(href)").get('').strip()
        item['Detail_Page_URL'] = response.url
        yield item
