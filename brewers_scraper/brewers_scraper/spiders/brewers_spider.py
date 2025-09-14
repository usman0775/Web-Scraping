import scrapy
import pandas as pd
import json


class BrewersSpiderSpider(scrapy.Spider):
    name = "brewers_spider"
    start_urls = [
        "https://www.brewersassociation.org/wp-content/themes/ba2019/json-store/breweries/breweries.json?nocache=1697298838783"]
    custom_settings = {'ROBOTSTXT_OBEY': False,
                       'RETRY_TIMES': 5,
                       'DOWNLOAD_DELAY': 1,
                       'CONCURRENT_REQUESTS': 1,
                       'FEED_URI': 'output/brewers.xlsx',
                       'FEED_FORMAT': 'xlsx',
                       'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
                       }

    def parse(self, response, **kwargs):
        data = json.loads(response.body)
        final_data = []
        for item in data:
            item['type'] = item.get('attributes', {}).get('type', '')
            item['url'] = item.get('attributes', {}).get('url', '')
            if item.get('BillingAddress', {}):
                item['city'] = item.get('BillingAddress', {}).get('city', '')
                item['country'] = item.get('BillingAddress', {}).get('country', '')
                item['countryCode'] = item.get('BillingAddress', {}).get('countryCode', '')
                item['geocodeAccuracy'] = item.get('BillingAddress', {}).get('geocodeAccuracy', '')
                item['latitude'] = item.get('BillingAddress', {}).get('latitude', '')
                item['longitude'] = item.get('BillingAddress', {}).get('longitude', '')
                item['postalCode'] = item.get('BillingAddress', {}).get('postalCode', '')
                item['state'] = item.get('BillingAddress', {}).get('state', '')
                item['stateCode'] = item.get('BillingAddress', {}).get('stateCode', '')
                item['street'] = item.get('BillingAddress', {}).get('street', '')
            item.pop('attributes')
            item.pop('BillingAddress')
            final_data.append(item)
        df = pd.DataFrame(final_data)
        df.to_excel("final.xlsx", index=False)
        df.to_jsonl('json_file.json')
