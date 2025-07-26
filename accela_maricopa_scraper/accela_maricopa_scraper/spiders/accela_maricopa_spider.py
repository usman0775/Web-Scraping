import re
from copy import deepcopy
from urllib.parse import urlencode
import scrapy
from scrapy.utils.response import open_in_browser


class AccelaMaricopaSpiderSpider(scrapy.Spider):
    name = "accela_maricopa_spider"
    start_urls = ["https://accela.maricopa.gov/CitizenAccessMCOSS/Cap/CapHome.aspx?module=PnD&TabName=PnD"]
    custom_settings = {'ROBOTSTXT_OBEY': False,
                       'RETRY_TIMES': 5,
                       'DOWNLOAD_DELAY': 1,
                       'CONCURRENT_REQUESTS': 1,
                       'FEED_URI': 'output/accela_maricopa.xlsx',
                       # 'FEED_EXPORT_FIELDS': file_headers,
                       'FEED_FORMAT': 'xlsx',
                       'FEED_EXPORT_ENCODING': 'utf-8',
                       'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
                       }
    json_data = {
        'ctl00$ScriptManager1': 'ctl00$PlaceHolderMain$',
        'ACA_CS_FIELD': '6e269db42b1e48638c643b4a8d02f0ea',
        '__EVENTTARGET': 'ctl00$PlaceHolderMain$btnNewSearch',
        '__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': '', '__VIEWSTATEGENERATOR': '3B78B502',
        '__VIEWSTATEENCRYPTED': '', 'ctl00$HeaderNavigation$hdnShoppingCartItemNumber': '',
        'ctl00$HeaderNavigation$hdnShowReportLink': 'N',
        'ctl00$PlaceHolderMain$addForMyPermits$collection': 'rdoNewCollection',
        'ctl00$PlaceHolderMain$addForMyPermits$txtName': 'name',
        'ctl00$PlaceHolderMain$addForMyPermits$txtDesc': '',
        'ctl00$PlaceHolderMain$ddlSearchType': '0',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSPermitNumber': '',
        'ctl00$PlaceHolderMain$generalSearchForm$ddlGSPermitType': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSProjectName': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSStartDate': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSStartDate_ext_ClientState': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSEndDate': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSEndDate_ext_ClientState': '',
        'ctl00$PlaceHolderMain$generalSearchForm$ddlGSLicenseType': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSLicenseNumber': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSFirstName': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSLastName': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSBusiName': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSBusiLicense': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSNumber$ChildControl0': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSNumber$ctl00_PlaceHolderMain_generalSearchForm_txtGSNumber_ChildControl0_watermark_exd_ClientState': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSNumber$ChildControl1': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSNumber$ctl00_PlaceHolderMain_generalSearchForm_txtGSNumber_ChildControl1_watermark_exd_ClientState': '',
        'ctl00$PlaceHolderMain$generalSearchForm$ddlGSDirection': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSStreetName': '',
        'ctl00$PlaceHolderMain$generalSearchForm$ddlGSStreetSuffix': '',
        'ctl00$PlaceHolderMain$generalSearchForm$ddlGSUnitType': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSUnitNo': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSParcelNo': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSCity': '',
        'ctl00$PlaceHolderMain$generalSearchForm$ddlGSState$State1': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSAppZipSearchPermit': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSAppZipSearchPermit_ZipFromAA': '0',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSAppZipSearchPermit_zipMask': '',
        'ctl00$PlaceHolderMain$generalSearchForm$txtGSAppZipSearchPermit_ext_ClientState': '',
        'ctl00$PlaceHolderMain$generalSearchForm$ddlGSCountry': '',
        'ctl00$PlaceHolderMain$hfASIExpanded': '', 'ctl00$PlaceHolderMain$txtHiddenDate': '',
        'ctl00$PlaceHolderMain$txtHiddenDate_ext_ClientState': '', 'ctl00$PlaceHolderMain$hfGridId': '',
        'ctl00$HDExpressionParam': '', 'Submit': 'Submit', '__ASYNCPOST': 'true', '': ''}
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'f5avraaaaaaaaaaaaaaaa_session_=HPIMBGPFEBKAOPEJBAHOGAEHJOHBIAJOLGGKLNPHHOGKCKENKCADPHHPAMJOKIGAPAHDBOFFPGBIJBCPIJJAJGFCNABLIMOOANELKECCCIMECAAIPMMOEEOFBHDLAKEH; .ASPXANONYMOUS=my97fwOFkNq133jtIymxZzDEVg5uL2fP7ADFva293cdO--p5D8TQx5NDhy0eSK71sYyHc8vEVRa-Y9aeFjXaBD7q5ReZM_dxfnRSzS48xXZnR0qgQqw5XN1PSlKyTf6MeJPf5IHLJHoSo0rdbFzaRckjEiCKbUYKwcWCv8ISacr86mWGHCkd4Tfs1Kc3OtmD0; ACA_SS_STORE=npweouhyiys1zxdhzurliks2; ACA_USER_PREFERRED_CULTURE=en-US; ACA_COOKIE_SUPPORT_ACCESSSIBILITY=False; ACA_CS_KEY=6e269db42b1e48638c643b4a8d02f0ea; pecan=412484362.47873.0000; _pendo_accountId.08c27448-9075-481d-584f-0c00aac03d50=MCOSS; _pendo_visitorId.08c27448-9075-481d-584f-0c00aac03d50=31BCA02094EB78126A517B206A88C73CFA9EC6F704C7030D18212CACE820F025F00BF0EA68DBF3F3A5436CA63B53BF7BF80AD8D5DE7D8359D0B7FED9DBC3AB99; _pendo_meta.08c27448-9075-481d-584f-0c00aac03d50=2627249158; LASTEST_REQUEST_TIME=1696859963470',
        'Origin': 'https://accela.maricopa.gov',
        'Referer': 'https://accela.maricopa.gov/CitizenAccessMCOSS/Cap/CapHome.aspx?module=PnD&TabName=PnD',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'X-MicrosoftAjax': 'Delta=true',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    def parse(self, response, **kwargs):
        view_state = response.xpath("//input[@name='__VIEWSTATE']/@value").get('')
        aca = response.xpath("//input[@name='ACA_CS_FIELD']/@value").get('')
        json_data = deepcopy(self.json_data)
        json_data['__VIEWSTATE'] = view_state
        json_data['ctl00$ScriptManager1'] += 'dgvPermitList$updatePanelctl00$PlaceHolderMain$btnNewSearch'
        json_data['ACA_CS_FIELD'] = aca
        json_data['ctl00$PlaceHolderMain$generalSearchForm$txtGSStartDate'] = '10/01/2023'
        json_data['ctl00$PlaceHolderMain$generalSearchForm$txtGSEndDate'] = '10/10/2023'
        yield scrapy.FormRequest(url=self.start_urls[0], formdata=json_data, headers=self.headers, method='POST',
                                 callback=self.parse_listing)
        # s = self.data.split('&')
        # d =dict()
        # for ss in s:
        #     sss=ss.split('=')[0]
        #     sss2 =ss.split('=')[-1]
        #     d.update({sss: sss2})
        # print(d)
        # yield scrapy.Request(url=self.start_urls[0], method='POST', body=urlencode(self.data), callback=self.listing)

    def parse_listing(self, response):
        # open_in_browser(response)
        view_state = response.text.split('__VIEWSTATE|')[1].split('__VIEWSTATEGENERATOR')[0].replace('|8|hiddenField|', '').strip()
        aca = response.text.split('ACA_CS_FIELD')[1].replace('|', '').strip()
        json_data = deepcopy(self.json_data)
        json_data['__VIEWSTATE'] = view_state
        json_data['ctl00$ScriptManager1'] += 'dgvPermitList$gdvPermitList$ctl13$ctl03'
        json_data['__EVENTTARGET'] = 'ctl00$PlaceHolderMain$dgvPermitList$gdvPermitList$ctl13$ctl03'
        json_data['ACA_CS_FIELD'] = aca
        json_data['ctl00$PlaceHolderMain$generalSearchForm$txtGSStartDate'] = '10/01/2023'
        json_data['ctl00$PlaceHolderMain$generalSearchForm$txtGSEndDate'] = '10/10/2023'
        yield scrapy.FormRequest(url=self.start_urls[0], formdata=json_data, headers=self.headers, method='POST',
                                 callback=self.more_listing_pages)
    #     # open_in_browser(response)
    #     # urls = response.xpath("//a[contains(@id,'hlPermitNumber')]/@href").getall()
    #     # for url in urls:
    #     #     print(url)
    #     # next_page = response.xpath(
    #     #     "//td[span[contains(@class,'SelectedPageButton')]]/following-sibling::td[1]/a/@href").get('')
    #
    def more_listing_pages(self, response):
        open_in_browser(response)
