import re
import time

from scrapy.selector import Selector
from scrapy import signals
from copy import deepcopy
import scrapy
import json
import csv
from scrapy.utils.response import open_in_browser


class Arztsuche116117DeSpiderSpider(scrapy.Spider):
    name = "arztsuche_116117_de_spider"
    url = 'https://arztsuche.116117.de/'
    url1 = 'https://arztsuche.116117.de/pages/arztsuche.xhtml'
    custom_settings = {'ROBOTSTXT_OBEY': False,
                       'RETRY_TIMES': 5,
                       'DOWNLOAD_DELAY': 2,
                       'CONCURRENT_REQUESTS': 1,
                       'FEEDS': {'output/arztsuche_116117_de.csv': {'format': 'csv', 'overwrite': True}}
                       }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'cookieConsent=level1; JSESSIONID=EVbiDY9sZBmKwSbzWJ5_q2Tkw4kmzBfYpOQrRE0Y.localhost; TS013407f0=0111b4ea97df541bba86f8707faefe0613a8a5f449dade8de1ec6b936f51cb54eaacc9c58907b7568b413e9e93f10b99fe67f932e7f621fa4dbc72121a1aba575d1d4591bc',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    headers1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'cookieConsent=level1; JSESSIONID=EVbiDY9sZBmKwSbzWJ5_q2Tkw4kmzBfYpOQrRE0Y.localhost; TS013407f0=0111b4ea97df541bba86f8707faefe0613a8a5f449dade8de1ec6b936f51cb54eaacc9c58907b7568b413e9e93f10b99fe67f932e7f621fa4dbc72121a1aba575d1d4591bc',
        'DNT': '1',
        'Origin': 'https://arztsuche.116117.de',
        'Referer': 'https://arztsuche.116117.de/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    dheaders = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        # 'Cookie': 'cookieConsent=level1; JSESSIONID=u0wkC9mR1foOf7yyWqmR_kxwz_K5dyuL_HAV7Vap.localhost; TS013407f0=0111b4ea975246120568640ff0d463edb420b009c86889f5b3a9d9dcdb1590f021aed12a0951560428ca3e58e949e18c9c266a43096fbb6d0148922d0dc02406e08ce5b215',
        'DNT': '1',
        'Faces-Request': 'partial/ajax',
        'Origin': 'https://arztsuche.116117.de',
        'Referer': 'https://arztsuche.116117.de/pages/arztsuche.xhtml',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = {
        'searchForm': 'searchForm',
        'searchForm:selectedMultiSearch': '',
        'searchForm:locationSimpleSearch[]': '01616 Strehla',
        'searchForm:selectedLocationSimpleSearch': '',
        'searchForm:startSearch': 'Suchen',
        'searchForm:advancedSearchState': 'false',
        'searchForm:hasError': 'false',
        'searchForm:searchPerformed': 'false',
        'searchForm:selectedLocationAdvancedSearch': '',
        'searchForm:selectedArztname': '',
        'searchForm:selectedArztgruppen': '',
        'searchForm:externalArztgruppen': '',
        'searchForm:selectedZusatzbezeichnungen': '',
        'searchForm:selectedFremdsprachen': '',
        'searchForm:externalFremdsprachen': '',
        'searchForm:selectedBarrierefreiheiten': '',
        'searchForm:selectedZweitmeinungen': '',
        'searchForm:externalZweitmeinungen': '',
        'searchForm:externalRequest': 'false',
        'searchForm:selectedPsychotherapieverfahren': '',
        'searchForm:selectedPsychotherapiealtersgruppen': '',
        'searchForm:selectedPsychotherapiesettings': '',
        'searchForm:lat': '',
        'searchForm:lon': '',
        'javax.faces.ViewState': '3910992520741750509:-5695350259517448746',
    }
    ddata = {
        'jsToBackendForm': 'jsToBackendForm',
        'jsToBackendForm:findAndSelectArztById': '1',
        'jsToBackendForm:findAndSelectAerzteByIds': '',
        'jsToBackendForm:keepSessionAliveCall': '',
        'jsToBackendForm:initSearchFormCall': '',
        'javax.faces.ViewState': '-1822922195757770281:-8604309038140790714',
        'javax.faces.source': 'jsToBackendForm:findAndSelectArztById',
        'javax.faces.partial.event': 'change',
        'javax.faces.partial.execute': 'jsToBackendForm:findAndSelectArztById',
        'javax.faces.partial.render': 'searchForm:arztDetailsDialogWrapper',
        'javax.faces.behavior.event': 'valueChange',
        'javax.faces.partial.ajax': 'true',
    }
    zips = []
    with open('zipcodes.csv', mode='r', newline='') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            zips.append(''.join(row))
    zips.pop(0)
    zip_codes = [num.zfill(5) for num in zips]
    scraped_zip_codes = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Arztsuche116117DeSpiderSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(spider.spider_close, signal=signals.spider_closed)
        return spider

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers)

    def parse(self, response, **kwargs):
        zipcode = self.zip_codes.pop(0)
        view_state = response.css("input[id='j_id1:javax.faces.ViewState:0']::attr(value)").get('')
        yield scrapy.Request(url='https://arztsuche.116117.de/data?loc={}'.format(zipcode),
                             callback=self.search_by_zip, meta={'view_state': view_state, 'zip': zipcode},
                             dont_filter=True)

    def search_by_zip(self, response):
        zip_code_list = json.loads(response.body)
        zip_code = zip_code_list[0].get('d', '')
        if zip_code:
            request_data = deepcopy(self.data)
            request_data['searchForm:locationSimpleSearch[]'] = zip_code
            request_data['javax.faces.ViewState'] = response.meta['view_state']
            yield scrapy.FormRequest(url=self.url1, headers=self.headers1, method='POST', formdata=request_data,
                                     callback=self.parse_listing, meta={'zip': response.meta['zip']})

    def parse_listing(self, response):
        doctors_ids = response.css("div#searchResultList>div>div>div::attr(data-arzt-ids)").getall()
        print(doctors_ids, "::::::::::::::::::::::::::::::")
        view_state = response.css("input[id='j_id1:javax.faces.ViewState:0']::attr(value)").get('')
        if doctors_ids:
            for doctor_id in doctors_ids:
                self.scraped_zip_codes.append(response.meta['zip'])
                data = deepcopy(self.ddata)
                data['jsToBackendForm:findAndSelectArztById'] = doctor_id
                data['javax.faces.ViewState'] = view_state
                yield scrapy.FormRequest(url=self.url1, headers=self.dheaders,
                                         method='POST', formdata=data, callback=self.parse_detail)
        else:
            self.zip_codes.append(response.meta['zip'])
            time.sleep(600)

    def parse_detail(self, response):
        response = Selector(text=response.body)
        item = dict()
        name = response.xpath("//h4[@class='name']/text()").get('').strip()
        region = response.xpath("//div[@role='region']/p[@class='title']/text()").get('').strip()
        if region:
            gender = region.rsplit(' ', 1)[0]
            try:
                title = region.rsplit(' ', 1)[1]
            except:
                title = ''
        else:
            gender = ''
            title = ''
        item['Gender'] = gender
        item['Titel'] = title
        item['Name'] = name
        item['Profession'] = response.xpath("//div[@class='modal-body']//p[@class='fachgruppen']/span/text()").get(
            '').strip()
        address = response.xpath("//div[@class='modal-body']//p[@class='address']/text()").getall()
        address = [ad.strip() for ad in address if ad.strip() != '']
        if address:
            pattern = r'(?=\d)'
            parts = re.split(pattern, address[0], 1)
            try:
                strabe = parts[0].strip()
            except:
                strabe = ''
            try:
                nummer = parts[1].strip()
            except:
                nummer = ''
            ort = address[1].rsplit(' ', 1)[1].strip()
            plz = address[1].rsplit(' ', 1)[0].strip()
        else:
            nummer = ''
            strabe = ''
            ort = ''
            plz = ''
        item['Straße'] = strabe
        item['Nummer'] = nummer
        item['PLZ'] = plz
        item['Ort'] = ort
        item['Tel'] = response.xpath(
            "//div[@class='modal-body']//div[@id='kontaktdatenPhoneWeb']/a[contains(@href,'tel')]/@href").get(
            '').replace('tel:', '').replace('%20', '').replace('+', '').strip()
        item['E-Mail'] = response.xpath(
            "//div[@class='modal-body']//div[@id='kontaktdatenPhoneWeb']/a[contains(@href,'mailto:')]/@href").get(
            '').replace('mailto:', '').strip()
        item['Fax'] = response.xpath(
            "//div[@class='modal-body']//div[@id='kontaktdatenPhoneWeb']/span[@aria-label='Fax']/text()").get(
            '').strip()
        item['Fremdsprachen'] = ''.join(
            response.xpath("//div[@class='modal-body']//p[@class='fremdsprachen']/text()").getall()).strip()
        item['Psychotherapien'] = ';'.join(
            response.xpath("//div[@class='modal-body']//ul[@class='psychotherapie-liste']/li/text()").getall())
        yield item

    def spider_idle(self, spider):
        if self.zip_codes:
            request = scrapy.Request(url=self.url, headers=self.headers, callback=self.parse, dont_filter=True)
            self.crawler.engine.crawl(request, self)

    def spider_close(self, spider):
        data = self.scraped_zip_codes
        csv_file = "scraped_zip_codes.csv"
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
