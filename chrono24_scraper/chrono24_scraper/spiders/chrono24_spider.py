import json
import scrapy


class Chrono24SpiderSpider(scrapy.Spider):
    name = "chrono24_spider"
    start_urls = [
        "https://www.chrono24.com/search/index.htm?models=2763&ikmedium=user-mail&redirectToSearchIndex=true&year=2019&year=2023&year=2022&year=2021&year=2020&ikterm=all-watches-button&goal_suggest=1&manufacturerIds=221&dosearch=true&goal_searchtask_mail=1&ikcampaign=SavedSearch&maxAgeInDays=0&ikcontent=SearchResults&eeid=8f59afe825b1975b4360974042cb47d&iksource=c24sm&searchTaskId=5287620&recid=ATsf2_ZnjhuvXkjt9Vl3vpY2TiBy8QHQPI0WpJMOV-cmvP55xnd3-hEQhJUhZ57b_9bLcbihdWT-ux8Cx8xt7F4%3D&sortorder=5"]
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 1,
        'FEEDS': {'output/chrono24_updated.json': {'format': 'json'}}}

    headers = {
        'authority': 'www.chrono24.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': 'search-session=|3df8d762_Ue4hYM|0|32322690.32314182.32312132.32309186.32304519.32293976.32284096.32276041.32275412.32274969.32262865.32262799.32262760.32256547.32251920.32241772.32234782.32222077.32220241.32218056.32213654.32210934.32210411.32204367.32194180.32188179.32187602.32185930.32176245.32169387.32167258.32161567.32155339.32154049.32137427.32131870.32131857.32131649.32131631.32131627.32131169.32125971.32120493.32115229.32110551.32105737.32104206.32104187.32103252.32077508.32072281.32067953.32062536.32053639.32046548.32041767.32039838.32031445.32026010.32025915; chronosessid=b8d72b97-404f-44a6-865c-724ed47f018a; filter-combinations=2:Man|Mod,0:; csrf-token=1704108484.QGieE1quNcTEyM76jUk5zIPzmSLy_P8TXtGUQL6jDh8.AXG1VdgzqjEVazOiOQ4FV887b-5_; cfctGroup=AAA00%3D%26CECE00%3D%26SOLR00%3D%26CDCO00%3D%26SRWA00%3D; __cflb=04dToURFh1eSYhojy3X88ZJvcdNdZGky2C4K9Hhefh; timezone=Asia/Karachi; __ssid=d42b0e0a65a87123fa89fe5fda7a2bb; c24-consent=AAAAIM/vwf4B; last-search-result-ids=32322690.32314182.32312132.32309186.32304519.32293976.32284096.32276041.32275412.32274969.32262865.32262799.32262760.32256547.32251920.32241772.32234782.32222077.32220241.32218056.32213654.32210934.32210411.32204367.32194180.32188179.32187602.32185930.32176245.32169387.32167258.32161567.32155339.32154049.32137427.32131870.32131857.32131649.32131631.32131627.32131169.32125971.32120493.32115229.32110551.32105737.32104206.32104187.32103252.32077508.32072281.32067953.32062536.32053639.32046548.32041767.32039838.32031445.32026010.32025915; pu=true; _gid=GA1.2.1533727881.1704108533; FPID=FPID2.2.fkh4o3aT0qxiF4FoBRoA56GUwERvd9zeOLtHx0CztWw%3D.1704108533; FPLC=UBfpZPiMB1bmoBNFv%2F2xP4MGN24R3%2BKmdijiNk1Fp2lBOrBsN88XjuQwIL70fFyw2xdr57JJlvleRiEXpfRIJs9u%2BvNUBXGXwJ%2FMqun3h%2BtOCBgBAt9%2F%2Bxkqxpguyg%3D%3D; _ga_B8CPBTKGPW=GS1.1.1704108532.1.1.1704108709.0.0.0; _ga=GA1.2.292131179.1704108533; _dc_gtm_UA-527734-1=1; __gads=ID=f17a4be59280357b:T=1704108712:RT=1704108712:S=ALNI_MZbdXbZvuWVdUNodii2gY53Sgpt7Q; __gpi=UID=00000ccf69f2b087:T=1704108712:RT=1704108712:S=ALNI_MamWauMSpST3W0b-M1jMrCLNjz17A; lastRskxRun=1704108713717; rskxRunCookie=0; rCookie=t7iw1ztqyfelzhbr55siknlquubuuu; c24-data=eyI1Ijp7ImUiOiIxNzA2NzAwNzA3IiwidiI6IjMifSwiNiI6eyJlIjoiMTcwNjcwMDcwNyIsInYiOiIzIn0sIjI3Ijp7ImUiOiIxNzM1NjQ0NDg0IiwidiI6IjEifSwiMzYiOnsiZSI6IjE3MzU2NDQ0ODQiLCJ2IjoiMTcwNDEwODQ4NDI1OSJ9LCIzNyI6eyJlIjoiMTczNTY0NDQ4NCIsInYiOiIxNzA0MTA4NDg0MjU5In0sIjM4Ijp7ImUiOiIxNzM1NjQ0NDg0IiwidiI6IjE3MDE0MzAwODQyNTkifSwiNDEiOnsiZSI6IjE3MzU2NDQ0ODQiLCJ2IjoiMTcwNDEwODQ4NDAwMCJ9LCI5OCI6eyJlIjoiMTczNTY0NDcwNyIsInYiOiIzIn0sIjExNSI6eyJ2IjoibGciLCJlIjoiMTcxOTY2MDc0OCJ9LCIyMzIiOnsiZSI6IjE3MzU2NDQ0OTAiLCJ2IjoiMTcwNDEwODQ4NDM2NyJ9LCI0MzMiOnsiZSI6IjE3MDY3MDA3MDciLCJ2IjoiMyJ9LCI0NjUiOnsiZSI6IjE3OTg3MTY1MzEiLCJ2IjoiMTc5ODcxNjUzMTIwMiJ9fQ==',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=self.headers)

    def parse(self, response, **kwargs):
        watches = json.loads(response.css('script[type="application/ld+json"]::text').get(''))
        offers = watches.get('@graph', [])[-1].get('offers', [])
        for watch, offer in zip(response.css("div#wt-watches>div.article-image-carousel"), offers):
            item = dict()
            item['Watch_Title'] = offer.get('name', '')
            item['Tagline'] = watch.css("div.text-ellipsis.m-b-2::text").get('').strip()
            item['Price'] = ''.join(
                watch.xpath(".//div[@class='text-muted text-sm']/preceding-sibling::div//text()").getall()).strip()
            item['Price_2'] = offer.get('price', '')
            item['Shipping_Charges'] = watch.css("div.text-muted.text-sm::text").get('').strip()
            item['Location'] = watch.css("button span.text-uppercase::text").get('').strip()
            item['Image_URL'] = offer.get('image', {}).get('contentUrl', '')
            item['Page_URL'] = offer.get('url', '')
            yield item
        next_page = response.xpath("//span[contains(text(),'Next')]/parent::a/@href").get('')
        if next_page:
            yield response.follow(next_page, headers=self.headers, callback=self.parse)
