import scrapy
from loft_parser.items import *


class CianSpider(scrapy.Spider):
    name = "cian"

    def __init__(self, city='ulyanovsk', rent='month', *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.start_urls:
            self.city = city
            self.rent = rent
            url_part = {'month': 'snyat-kvartiru', 'day': 'snyat-kvartiru-posutochno'}[rent]
            self.url = f'https://{city}.cian.ru/{url_part}/'

    def start_requests(self):
        yield from super().start_requests()

        if not self.start_urls:
            page = 1
            yield scrapy.Request(
                url=self.url,
                callback=self.parse_list,
                meta={'page': page}
            )

    def parse_list(self, response):
        # Перебираем все ссылки на страницы с описанием квартиры
        links_xpath = '//div[@data-name="LinkArea"]/a[1]'
        for link in response.xpath(links_xpath):
            url = response.urljoin(link.xpath('./@href').get())
            yield LoftItem(url=url, city=self.city, rent=self.rent)

        # Переход к следующей странице
        page = response.meta.get('page') + 1
        next_page = response.xpath(f'//div[@data-name="Pagination"]//ul//a[contains(text(),"{page}")]/@href').get()
        yield response.follow(url=next_page, callback=self.parse_list, meta={'page': page})

    def parse(self, response):
        # Параметры квартиры
        param_items = []
        # Основные параметры квартиры
        for param in response.xpath('//*[@data-name="ObjectSummaryDescription"]//*[@data-testid="object-summary-description-info"]'):
            loader = ItemLoader(item=ParamItem(), selector=param)
            loader.add_xpath('key', './*[@data-testid="object-summary-description-value"]/text()')
            loader.add_xpath('value', './*[@data-testid="object-summary-description-title"]/text()')
            param_items.append(loader.load_item())

        # Параметры заполняемые дополнительно самим автором объявления
        for param in response.xpath('//*[@data-name="GeneralInformation"]//*[contains(@class,"item")]'):
            loader = ItemLoader(item=ParamItem(), selector=param)
            loader.add_xpath('key', './*[contains(@class,"name")]/text()')
            loader.add_xpath('key', './text()')
            loader.add_xpath('value', './*[contains(@class,"value")]/text()')
            param_items.append(loader.load_item())

        # Параметры дома по данным Циан
        for param in response.xpath('//*[@data-name="BtiHouseData"]//*[contains(@class,"item")]'):
            loader = ItemLoader(item=ParamItem(), selector=param)
            loader.add_xpath('key', './*[contains(@class,"name")]/text()')
            loader.add_xpath('value', './*[contains(@class,"value")]/text()')
            param_items.append(loader.load_item())

        # Вся информация вместе
        loader = CianLoftItemLoader(response=response)
        loader.add_xpath('address', '//*[@data-name="Geo"]/span/@content')
        loader.add_xpath('price', '//span[@itemprop="price"]/@content')
        loader.add_xpath('price_period', '//span[@itemprop="price"]/@content')
        loader.add_xpath('seller_name', '//*[@data-name="AuthorAsideBrand"]//a[@data-name="LinkWrapper"]/h4/text()')
        loader.add_xpath('seller_url', '//*[@data-name="AuthorAsideBrand"]//a[@data-name="LinkWrapper"]/@href')
        loader.add_xpath('description', '//p[@itemprop="description"]/text()')
        loft_item = loader.load_item()
        loft_item['url'] = response.url
        loft_item['params'] = param_items
        return loft_item
