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


class SiteProductItem(Item):
    Url = Field()
    CategoryTopology = Field()
    Title = Field()
    TesscoSKU = Field()
    UPC = Field()
    QTY_UOM = Field()
    MFGPart = Field()
    Description = Field()
    ListPrice = Field()
    Price = Field()
    InStock_OutOfStock = Field()
    Manufacturer = Field()


class TesscoScraper (scrapy.Spider):
    name = "scrapingdata"
    allowed_domains = ['www.tessco.com']

    START_URL = 'https://www.tessco.com'
    LOGIN_URL = 'https://www.tessco.com/api/tessco/session/login'
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
                          }
                          )

    def check_login(self, response):

        is_authenticated = json.loads(response.body)['Data']['Session']['IsAuthenticated']
        if is_authenticated:
            yield Request(url=self.START_URL,
                          callback=self.parse_category,
                          headers=self.headers,
                          dont_filter=True
                          )
        else:
            print "login failed"

    def parse_category(self, response):

        assert_category_links = response.xpath('//div[@class="thirdNav"]//ul[@class="unlisted"]/li/a/@href').extract()
        for assert_category_link in assert_category_links:
            category_link = self.START_URL + assert_category_link
            yield Request(url=category_link, callback=self.parse_page, dont_filter=True, headers=self.headers)

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

        page_count = int(first_page_content['totalCount'])


        page_links = []
        page_link = response.xpath('//span[@class="pagnLink"]/a/@href')[0].extract()
        page_link_num = response.xpath('//span[@class="pagnLink"]/a/text()')[0].extract()
        page_count = response.xpath('//span[@class="pagnDisabled"]/text()')[0].extract()

        for page_num in range(1, int(page_count)):
            page_list = page_link.replace('page={page_link_num}'.format(page_link_num=int(page_link_num)),
                                          'page={page_num}'.format(page_num=page_num))
            page_list = self.START_URL + page_list
            page_links.append(page_list)

        for p_link in page_links:
            if 'https' in p_link:
                sub_link = p_link
            else:
                sub_link = self.START_URL + p_link
            yield Request(url=sub_link, callback=self.parse_data, dont_filter=True, headers=self.headers)


    def parse_data(self, response):
        li_list = response.xpath("//div[@id='mainResults']/.//ul/li [contains(@id, 'result')]")
        for li in li_list:
            link = li.xpath(".//div[contains(@class, 'a-spacing-mini')]//a[contains(@class,'s-access-detail-page')]/@href").extract()
            try:
                if link and 'http' in link[0]:
                    yield Request(url=link[0],
                                  callback=self.parse_product,
                                  dont_filter=True,
                                  headers=self.headers)

            except Exception as e:
                print (link[0])

    def parse_product(self, response):
        product = SiteProductItem()

        title = self._parse_title(response)
        product['title'] = title

        brand = self._parse_brand(response)
        product['brand'] = brand

        price = self._parse_price(response)
        product['price'] = price

        original_price = self._parse_original_price(response)
        product['original_price'] = original_price

        yield product

    @staticmethod
    def _parse_title(response):
        title = response.xpath("//span[@id='productTitle']/text()").extract()
        return title[0].strip() if title else None

    @staticmethod
    def _parse_brand(response):
        brand_info = response.xpath('//a[@id="brand"]/@href').extract()
        if not brand_info:
            brand_info = response.xpath('//a[@id="brand"]/text()').extract()
        if not brand_info:
            brand_info = response.xpath('//*[@id="by-line"]/.//a/text()').extract()
        brand = None
        if brand_info:
            brand = brand_info[0].split('/')[1].split('/')[0]
        return brand

    @staticmethod
    def _parse_price(response):
        price = response.xpath('//span[contains(@id,"priceblock")]/text()').extract()
        return price[0].split('-')[0] if price else None

    @staticmethod
    def _parse_original_price(response):
        original_price = response.xpath('//span[contains(@class,"a-text-strike")]/text()').extract()
        if not original_price:
            original_price = response.xpath('//span[contains(@id,"priceblock")]/text()').extract()
        return original_price[0].split('-')[0] if original_price else None