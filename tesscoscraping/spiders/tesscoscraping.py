from scrapy.conf import settings
from urllib import urlencode
from scrapy import Request
from lxml import html
import re
import scrapy
import json
from scrapy.item import Item, Field
from scrapy import FormRequest
import requests
from scrapy import Selector
from urllib import urlencode


class SiteProductItem(Item):
    Url = Field()
    CategoryTopology = Field()
    Title = Field()
    TesscoSKU = Field()
    UPC = Field()
    QTY_UOM = Field()
    MFGPart = Field()
    Description = Field()
    Price = Field()
    ListPrice = Field()
    InStock_OutOfStock = Field()
    Manufacturer = Field()
    ImageURL = Field()
    Length = Field()


class TesscoScraper (scrapy.Spider):
    name = "scrapingdata"
    allowed_domains = ['www.tessco.com']

    START_URL = 'https://www.tessco.com'
    LOGIN_URL = 'https://www.tessco.com/api/tessco/session/login'
    PRODUCT_URL = 'https://www.tessco.com/product/'
    settings.overrides['ROBOTSTXT_OBEY'] = False
    USER_NAME = 'accounting@sellnetny.com'
    PASSWORD = 'Max@302'

    AQ = '(@syssource==("Coveo_web_index - SCRBLUE-SCRCM01-Sitecore8") NOT @ftemplateid51937==' \
         '("adb6ca4f-03ef-4f47-b9ac-9ce2ba53ff97","fe5dd826-48c6-436d-b87a-7c4210c7413b")) ' \
         '(@fstatus51937<>ObsoleteOutOfStock) (@fisz32xdiscontinued51937==0) (@fisez120xposedonweb51937==(1,Yes)) ' \
         '(@fitemtype51937<>(LABOR,PRICING)) (@fsellingrestrictioncode51937==' \
         '("N/A",1MPH,ADOP,AKGS,AUGL,BAN5,BAN6,BINA,BLUE,BODZ,BOND,BRTH,BRVN,C100,CANO,CL3M,CMEC,CMES,CRIK,DEMO,DSP2,' \
         'ELEM,ELIT,EVUT,EXA1,FRT1,FTTH,GEAR,GHCC,GIGA,GOLF,GOOG,GR4B,GRFN,HOLD,HUAW,IBLT,ICOM,INCP,INHC,JABR,JAWB,' \
         'JLAB,KING,KRNZ,KSC2,LAND,LFLX,LIFE,LIFP,MACZ,METR,METT,MOSH,MSFT,MSII,MSIO,MUSE,MWLN,MYCH,NATU,NEET,NEST,' \
         'NOMA,NONO,NSC1,NSC2,NSC3,NSC4,OBSS,OTTC,PLNA,PLNB,POPS,PRRT,RAJ,RAJ1,RDL1,REPS,SAMA,SAMC,SAMD,SAMM,SAMX,SC15' \
         ',SCOS,SENA,SKEC,SKUL,SLC,SOLR,SONA,SONX,SPAW,SPCK,SPEL,SPHM,SQRE,SSC2,SSC3,STAY,SUIT,SWCM,TEDB,TMOB,TMTM,TNL1' \
         ',TWEL,UAGR,URBN,VINE,VNV1,VOIP,WEMO,ZEPP,ZIK1)) (@fcategories51937*="dbae02fc-1e79-7dbb-f118-decf9a10503e*")'

    CQ = '((@fz95xlanguage51937=="en" @fz95xlatestversion51937=="1")) (@fz95xtemplatename51937==Product) ' \
         '(@fisz32xactive51937==1)'

    GROUP_BY = '[{"field":"@fcategories51937","maximumNumberOfValues":1000,"sortCriteria":"occurrences",' \
               '"injectionDepth":1000,"completeFacetWithStandardValues":true},{"field":"@fisonsale51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":false,"allowedValues":["Yes"]},{"field":"@fmanufacturername51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fpurchaseplans51937","maximumNumberOfValues":6,' \
               '"sortCriteria":"alphaAscending","injectionDepth":10000,"completeFacetWithStandardValues":true},' \
               '{"field":"@fcatitemrfconnectorbodystylest51937","maximumNumberOfValues":6,"sortCriteria":' \
               '"alphaAscending","injectionDepth":10000,"completeFacetWithStandardValues":true},' \
               '{"field":"@fcatitemwiregaugest51937","maximumNumberOfValues":6,"sortCriteria":"alphaAscending",' \
               '"injectionDepth":10000,"completeFacetWithStandardValues":true},{"field":"@fcatitemconfiguration51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemvolumecapacityminimumst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemvopst51937","maximumNumberOfValues":6,' \
               '"sortCriteria":"alphaAscending","injectionDepth":10000,"completeFacetWithStandardValues":true},' \
               '{"field":"@fcatitemouterconductormaterialst51937","maximumNumberOfValues":6,' \
               '"sortCriteria":"alphaAscending","injectionDepth":10000,"completeFacetWithStandardValues":true},' \
               '{"field":"@fcatitemshieldedst51937","maximumNumberOfValues":6,"sortCriteria":"alphaAscending",' \
               '"injectionDepth":10000,"completeFacetWithStandardValues":true},' \
               '{"field":"@fcatitemoutercontactattachtypest51937","maximumNumberOfValues":6,' \
               '"sortCriteria":"alphaAscending","injectionDepth":10000,"completeFacetWithStandardValues":true},' \
               '{"field":"@fcatitemfireratingst51937","maximumNumberOfValues":6,"sortCriteria":"alphaAscending",' \
               '"injectionDepth":10000,"completeFacetWithStandardValues":true},{"field":"@fcatitemarmoredst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemcontactsurface51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemcolorst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemfinish51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemjacketcolorst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemnetworkconnectorsst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemrfconnectorst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemcablemanufacturerst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemcablesiz122xest51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemmaterialpin51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemcoaz120xialcableseriesst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitembodyattachmentst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemjacketmaterialst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemminimumbendradinsst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemjumperlengthst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemrfimpedancest51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemfireretardantst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemconnector1manufacturerst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemctrconductorconstructionst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemconnector2manufacturerst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemvolumecapacitymaz120ximumst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitembodymaterialst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatiteminsulatormaterialst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemrfconnectorsst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemcabletypest51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemlowpimst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemacinputvoltagest51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemenvironmentst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemvoltagetype51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemnetworkcategoryst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemminimumbendradopst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemuvresistantst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemcablelengthst51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@fcatitemcenterpintypest51937",' \
               '"maximumNumberOfValues":6,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true},{"field":"@favailabledate51937",' \
               '"maximumNumberOfValues":3,"sortCriteria":"occurrences","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true,"rangeValues":[{"start":"2018-12-21T23:00:00.000Z",' \
               '"end":"2999-12-31T22:59:59.999Z","label":"60 Days","endInclusive":false},' \
               '{"start":"2018-11-21T23:00:00.000Z","end":"2999-12-31T22:59:59.999Z","label":"90 Days",' \
               '"endInclusive":false},{"start":"1969-12-31T23:00:00.000Z","end":"2999-12-31T22:59:59.999Z",' \
               '"label":"All","endInclusive":false}]},{"field":"@fbrandmodelhierarchy51937",' \
               '"maximumNumberOfValues":10001,"sortCriteria":"alphaAscending","injectionDepth":10000,' \
               '"completeFacetWithStandardValues":true}]'

    def __init__(self, **kwargs):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/57.0.2987.133 Safari/537.36"}

    def start_requests(self):
        yield Request(url=self.START_URL,
                      callback=self.login,
                      headers=self.headers,
                      dont_filter=True
                      )

    def login(self, response):

        yield FormRequest(url=self.LOGIN_URL,
                          callback=self.check_login,
                          headers=self.headers,
                          dont_filter=True,
                          method="POST",
                          formdata={
                              'UserName': self.USER_NAME,
                              'Password': self.PASSWORD
                          },
                          meta=response.meta
                          )

    def check_login(self, response):

        is_authenticated = json.loads(response.body)['Data']['Session']['IsAuthenticated']
        if is_authenticated:
            yield Request(url=self.START_URL,
                          callback=self.parse_category,
                          headers=self.headers,
                          dont_filter=True,
                          meta=response.meta
                          )
        else:
            print ("login failed")


    def parse_category(self, response):

        if response.meta.has_key('url'):
            yield Request(url=response.meta['url'], callback=self.parse_product, dont_filter=True, headers=self.headers)
        else:
            assert_category_links = response.xpath('//div[@class="thirdNav"]//ul[@class="unlisted"]/li/a/@href').extract()
            for assert_category_link in assert_category_links:
                category_link = self.START_URL + assert_category_link
                yield Request(url=category_link, callback=self.parse_page, dont_filter=True, headers=self.headers, meta=response.meta)

    def parse_page(self, response):

        page_name = re.search('"pageName" : "(.*?)" ,', response.body).group(1)
        sitecoreItemUri = re.search('"sitecoreItemUri" : "(.*?)" ,', response.body).group(1)
        request_url = 'https://www.tessco.com/coveo/rest/v2/?sitecoreItemUri={sitecoreItemUri}&siteName=TesscoCommerce'\
            .format(sitecoreItemUri=sitecoreItemUri)
        first_page_content = requests.post(request_url,
                                           data={
                                               'aq': self.AQ,
                                               'cq': self.CQ,
                                               'searchHub': page_name,
                                               'language': 'en-US',
                                               'firstResult': '0',
                                               'numberOfResults': '25',
                                               'excerptLength': '200',
                                               'enableDidYouMean': 'true',
                                               'sortCriteria': 'Relevancy',
                                               'queryFunctions': '[]',
                                               'rankingFunctions': '[]',
                                               'groupBy': self.GROUP_BY,
                                               'retrieveFirstSentences': 'true',
                                               'timezone': 'Europe/Berlin',
                                               'disableQuerySyntax': 'false',
                                               'enableDuplicateFiltering': 'false',
                                               'enableCollaborativeRating': 'false',
                                               'debug': 'false',
                                               'context': '{}'
                                           })

        page_count = json.loads(first_page_content.content)['totalCount']
        page_number = int(page_count/25)

        total_product_urls = []
        # for page_index in range(0, page_number):
        for page_index in range(0, 2):

            first_result_num = str(25*page_index)
            page_content = requests.post(request_url,
                                         data={
                                               'aq': self.AQ,
                                               'cq': self.CQ,
                                               'searchHub': page_name,
                                               'language': 'en-US',
                                               'firstResult': '0',
                                               'numberOfResults': first_result_num,
                                               'excerptLength': '200',
                                               'enableDidYouMean': 'true',
                                               'sortCriteria': 'Relevancy',
                                               'queryFunctions': '[]',
                                               'rankingFunctions': '[]',
                                               'groupBy': self.GROUP_BY,
                                               'retrieveFirstSentences': 'true',
                                               'timezone': 'Europe/Berlin',
                                               'disableQuerySyntax': 'false',
                                               'enableDuplicateFiltering': 'false',
                                               'enableCollaborativeRating': 'false',
                                               'debug': 'false',
                                               'context': '{}'
                                           })

            results = json.loads(page_content.content)['results']
            for result in results:
                title = result['Title']
                page_link = self.PRODUCT_URL + title
                if not page_link in total_product_urls:
                    total_product_urls.append(page_link)

        for prod_url in total_product_urls:
            yield Request(url=prod_url, callback=self.parse_product, dont_filter=True, headers=self.headers, meta=response.meta)

    def parse_product(self, response):
        if 'login' in response.url:
            response.meta['url'] = response.url
            self.login(response)

        else:
            product = SiteProductItem()
            product['Url'] = response.url

            CategoryTopology = self._parse_CategoryTopology(response)
            product['CategoryTopology'] = CategoryTopology

            Title = self._parse_Title(response)
            product['Title'] = Title

            TesscoSKU = self._parse_TesscoSKU(response)
            product['TesscoSKU'] = TesscoSKU

            UPC = self._parse_UPC(response)
            product['UPC'] = UPC

            QTY_UOM = self._parse_QTY_UOM(response)
            product['QTY_UOM'] = QTY_UOM

            MFGPart = self._parse_MFGPart(response)
            product['MFGPart'] = MFGPart

            Description = self._parse_Description(response)
            product['Description'] = Description

            Price = self._parse_Price(response)
            product['Price'] = Price

            ListPrice = self._parse_ListPrice(response)
            product['ListPrice'] = ListPrice

            InStock_OutOfStock = self._parse_InStock_OutOfStock(response)
            product['InStock_OutOfStock'] = InStock_OutOfStock

            Manufacturer = self._parse_Manufacturer(response)
            product['Manufacturer'] = Manufacturer

            Length = self._parse_Length(response)
            product['Length'] = Length

            ImageURL = self._parse_ImageURL(response)
            product['ImageURL'] = ImageURL



            yield product

    @staticmethod
    def _parse_CategoryTopology(response):

        path_words = response.xpath('//div[@class="container-fluid"]//ul[@class="unlisted inline"]//a/text()').extract()
        category_topology = ''
        for path_word in path_words:
            category_topology = category_topology + '>' + path_word

        return category_topology

    @staticmethod
    def _parse_Title(response):
        title = response.xpath('//div[@class="container-fluid productDetail"]//h2[@class="heavy"]/text()').extract()
        return title[0] if title else None

    @staticmethod
    def _parse_TesscoSKU(response):
        sku_info = re.search('TESSCO SKU:</span> (.*?)</li>', response.body).group(1)
        return sku_info if sku_info else None

    @staticmethod
    def _parse_UPC(response):
        upc_info = re.search('UPC:</span> (.*?)</li>', response.body).group(1)
        return upc_info if upc_info else None

    @staticmethod
    def _parse_QTY_UOM(response):
        qty_uom = re.search('QTY/UOM:</span> (.*?)</li>', response.body).group(1)
        return qty_uom if qty_uom else None

    @staticmethod
    def _parse_MFGPart(response):
        mfp_part = re.search('MFG PART #:</span> (.*?)</li>', response.body).group(1)
        return mfp_part if mfp_part else None

    @staticmethod
    def _parse_Description(response):
        assert_description = response.xpath('//p[@class="more"]/text()').extract()
        return assert_description[0] if assert_description else None

    @staticmethod
    def _parse_Price(response):
        price = re.search('price:(.*?),', response.body).group(1).replace('"', '')
        return price if price else None

    @staticmethod
    def _parse_ListPrice(response):
        list_price = re.search('listPrice:(.*?),', response.body).group(1).replace('"', '')
        return list_price if list_price else None

    @staticmethod
    def _parse_InStock_OutOfStock(response):

        # sku = re.search('sku: (.*?),', response.body).group(1)
        # status = None
        # data = {'sku': sku}
        # stock_url = 'https://www.tessco.com/api/tessco/inventory/getproductavailability'
        # headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        #            'referer': response.url,
        #            'x-requested-with': 'XMLHttpRequest',
        #            'origin': 'https://www.tessco.com',
        #            'accept': 'application/json, text/javascript, */*; q=0.01',
        #            'content-length': '11',
        #            'accept-encoding': 'gzip, deflate, br'
        #            }
        # cookies = {
        #     'visid_incap_1696314': 'rETeod80SCuEYXU0BeF8ycWsbFwAAAAAQUIPAAAAAADU7XYM6JfhQEDdXNR/1s+k',
        #     'mt.v': '2.1974058.1550626034561',
        #     '_ga': 'GA1.2.1726999955.1550626037',
        #     '_gid': 'GA1.2.1229845563.1550626037',
        #     '_mkto_trk': 'id:217-TMY-439&token:_mch-tessco.com-1550626038354-87018',
        #     'liveagent_oref': '',
        #     'liveagent_ptid': '15d539f3-cca1-44c3-8635-de638b271ea3',
        #     'visitor': 'db8ce657-ded1-4724-b84f-de7ebe851a6c',
        #     'coveo_visitorId': 'db8ce657-ded1-4724-b84f-de7ebe851a6c',
        #     'ASP.NET_SessionId': 'ala2q0vlqdmbwckdsmhcatyt',
        #     'SC_ANALYTICS_GLOBAL_COOKIE': '162168f863fa49a58281fac7a70da47f|True',
        #     'liveagent_sid': '09d70f52-a39a-4d34-9f42-0f5e8f4d6958',
        #     'liveagent_vc': '3',
        #     '_hjIncludedInSample': '1',
        #     'incap_ses_443_1696314': 'G7QeehT6ullzMWW/eNslBhXhbFwAAAAALjC2UADe178jdGYFCmFFTw==',
        #     '_fbp': 'fb.1.1550652135077.1891818976',
        #     '_biz_uid': 'a11b8515fba740c3e49cfeb6eea46610',
        #     '_biz_flagsA': '%7B%22Version%22%3A1%2C%22Mkto%22%3A%221%22%2C%22XDomain%22%3A%221%22%7D',
        #     'incap_ses_360_1696314': 'yoY+C5jw1XsVBDNmqvr+BL1vblwAAAAAXoQP1jsmEcJ/kbslhxUCsg==',
        #     'incap_ses_435_1696314': 'ti8XE5UcJD7B9DRFgW8JBs93blwAAAAABXDUzkC63ZV1acoQCohOqg==',
        #     'nlbi_1696314': 'Xc6Fb5w0hFOGyAz1bQd84QAAAAAycLn2bZ3O1iCr5pHwVSWx',
        #     '_biz_nA': '28',
        #     '_biz_pendingA': '%5B%5D',
        #     'incap_ses_524_1696314': 'QTAof1xtYhS5yPX+WaBFB9OMblwAAAAAZBx6eLh1R4AS+jmJHMcNJw==',
        #     '.ASPXAUTH': '4DA35594D868155A5203B8E6AD7071C40F244ADFC45B203F0B11E55B610C215226305E0182E3CB96CB3DF22296089C706A38EC4258A9767F3E8200D67BE3AC3B266DEFA98E5878D6EA3EB2760E82221947A7801CE39C9E1D62844A80CD56E0502840661AE77A6E942ACCD2C9AD18A91A09D7510611FC4E9707405AB33765CC989E80FAFE4FA86A747C794F79F655C4FC128FE8A8F85EC6921CDF7CF0A580CDA5',
        #     'AccountNumber': '2537075',
        #     'PricingTier': '2',
        #     'MarketCode': '7M',
        #     'MetaMarketCode': 'RTL',
        #     'CustomerCreationDate': '2019-02-19T02:02:58-05:00',
        #     'UserRole': '',
        #     'TcomRegistrationDate': '',
        #     'BetaRegistrationDate': '10/21/2017 9:08:15 PM +00:00',
        #     'previousPage': '/product/261866',
        #     '_gat_UA-4337606-18': '1',
        #     '_gat': '1'
        # }
        #
        # try:
        #     resp = requests.post(stock_url, data=data, cookies=cookies).content
        #     resp = resp
        # except Exception as e:
        #     print(e)
        # return status

    @staticmethod
    def _parse_Manufacturer(response):

        manufacturer_info = None
        assert_specs = response.xpath('//div[contains(@class,"technicalSpecs")]//ul/li')
        for index, assert_spec in enumerate(assert_specs):
            spec_field = assert_spec.xpath('./div[@class="col-xs-6 col-sm-4 col-md-3"]/text()').extract()[0]
            if 'Manufacturer' in spec_field:
                manufacturer_info = assert_spec.xpath('./div[@class="col-xs-6 col-sm-8 col-md-9"]/text()').extract()
            else:
                pass
        return manufacturer_info[0].strip() if manufacturer_info else None

    @staticmethod
    def _parse_Length(response):

        length_info = None
        assert_specs = response.xpath('//div[contains(@class,"technicalSpecs")]//ul/li')
        for index, assert_spec in enumerate(assert_specs):
            spec_field = assert_spec.xpath('./div[@class="col-xs-6 col-sm-4 col-md-3"]/text()').extract()[0]
            if 'Whip Length' in spec_field:
                length_info = assert_spec.xpath('./div[@class="col-xs-6 col-sm-8 col-md-9"]/text()').extract()
            else:
                pass
        return length_info[0].strip() if length_info else None

    @staticmethod
    def _parse_ImageURL(response):
        img_url = response.xpath('//img[@class="currentImage"]/@src').extract()
        return img_url[0] if img_url else None