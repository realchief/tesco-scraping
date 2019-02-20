from scrapy.conf import settings
from urllib import urlencode
from scrapy import Request
from lxml import html
import re
import scrapy
import json
from scrapy.item import Item, Field
from scrapy import FormRequest


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