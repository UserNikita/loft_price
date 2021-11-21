import scrapy
from loft_parser.items import *


class CianSpider(scrapy.Spider):
    name = "cian"

    def __init__(self, loft_url=None, city='ulyanovsk', rent='month', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loft_url = loft_url

        if not loft_url:
            self.city = city
            self.rent = rent
            url_part = {'month': 'snyat-kvartiru', 'day': 'snyat-kvartiru-posutochno'}[rent]
            self.url = f'https://{city}.cian.ru/{url_part}/'

    def start_requests(self):
        if self.loft_url:
            yield scrapy.Request(url=self.loft_url, callback=self.parse_loft)
        else:
            page = 1
            yield scrapy.Request(
                url=self.url,
                callback=self.parse_loft_list,
                meta={'page': page}
            )

    def parse_loft_list(self, response):
        # Перебираем все ссылки на страницы с описанием квартиры
        links_xpath = '//div[@data-name="LinkArea"]/a[1]'
        for link in response.xpath(links_xpath):
            url = response.urljoin(link.xpath('./@href').get())
            yield LoftItem(url=url, city=self.city, rent=self.rent)

        # Переход к следующей странице
        page = response.meta.get('page') + 1
        next_page = response.xpath(f'//div[@data-name="Pagination"]//ul//a[contains(text(),"{page}")]/@href').get()
        yield response.follow(url=next_page, callback=self.parse_loft_list, meta={'page': page})

    def parse_loft(self, response):
        # Параметры квартиры
        param_items = []
        for param in response.xpath('//*[@id="description"]//div[@itemscope]/div'):
            loader = ItemLoader(item=ParamItem(), selector=param)
            loader.add_xpath('key', './*[contains(@class,"title")]/text()')
            loader.add_xpath('value', './*[contains(@class,"value")]/text()')
            param_items.append(loader.load_item())

        # Параметры дома
        for param in response.xpath('//*[@data-name="BtiHouseData"]//*[contains(@class,"item")]'):
            loader = ItemLoader(item=ParamItem(), selector=param)
            loader.add_xpath('key', './*[contains(@class,"name")]/text()')
            loader.add_xpath('value', './*[contains(@class,"value")]/text()')
            param_items.append(loader.load_item())

        # Вся информация вместе
        loader = CianLoftItemLoader(response=response)
        loader.add_xpath('address', '//span[contains(@class, "item-address__string")]/text()')
        loader.add_xpath('price', '//span[@itemprop="price"]/@content')
        loader.add_xpath('price_period', '//span[@itemprop="price"]/@content')
        loader.add_xpath('seller_name', '//*[@data-name="AuthorAsideBrand"]//a[@data-name="LinkWrapper"]/h2/text()')
        loader.add_xpath('seller_url', '//*[@data-name="AuthorAsideBrand"]//a[@data-name="LinkWrapper"]/@href')
        loader.add_xpath('description', '//p[@itemprop="description"]/text()')
        loft_item = loader.load_item()
        loft_item['url'] = response.url
        loft_item['params'] = param_items
        return loft_item
