import scrapy
from scrapy.loader import ItemLoader
from loft_parser.items import LoftItem, LoftDataItem, ParamItem, CoordinateItem


class AvitoSpider(scrapy.Spider):
    name = "avito"

    def __init__(self, city='ulyanovsk', rent='month', *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.start_urls:
            self.city = city
            self.rent = rent
            url_part = {
                'month': 'sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg',
                'day': 'sdam/posutochno-ASgBAgICAkSSA8gQ8AeSUg',
                'forever': 'prodam-ASgBAgICAUSSA8YQ',
            }[rent]
            self.url = f'https://www.avito.ru/{city}/kvartiry/{url_part}'

    def start_requests(self):
        yield from super().start_requests()

        if not self.start_urls:
            yield scrapy.Request(url=self.url, callback=self.parse_list)

    def parse_list(self, response):
        """Парсинг списка ссылок на страницы с детальной информацией о квартирах"""
        links_xpath = '//a[contains(@itemprop, "url") and h3]'
        for link in response.xpath(links_xpath):
            url = response.urljoin(link.xpath('./@href').get())
            yield LoftItem(url=url, city=self.city, rent=self.rent)

        first_page = response.xpath('//span[contains(@data-marker,"prev") and contains(@class, "readonly")]').get()
        if first_page is not None:
            page_count = int(response.xpath('//span[contains(@data-marker,"page")]/text()').getall()[-1])
            for page in range(2, page_count + 1):
                url = response.url + '?p=%d' % page
                yield response.follow(url=url, callback=self.parse_list)

    def parse(self, response):
        """Парсинг страницы с детальной информацией о квартире"""
        # Параметры квартиры
        param_items = []
        for param in response.xpath('//li[contains(@class, "item-params-list")]'):
            loader = ItemLoader(item=ParamItem(), selector=param)
            loader.add_xpath('key', './span/text()')
            loader.add_xpath('value', './text()')
            param_items.append(loader.load_item())

        # Координаты дома
        loader = ItemLoader(item=CoordinateItem(), response=response)
        loader.add_xpath('lat', '//div[contains(@class, "item-map-wrapper")]/@data-map-lat')
        loader.add_xpath('lon', '//div[contains(@class, "item-map-wrapper")]/@data-map-lon')
        coord_item = loader.load_item()

        # Вся информация вместе
        loader = ItemLoader(item=LoftDataItem(), response=response)
        loader.add_xpath('address', '//span[contains(@class, "item-address__string")]/text()')
        loader.add_xpath('price', '//span[contains(@class, "js-item-price")]/@content')
        loader.add_xpath('price_period', '//span[contains(@class, "js-item-price")]/../text()')
        loader.add_xpath('seller_name', '//div[contains(@class,"seller-info-name")]/a/text()')
        loader.add_xpath('seller_url', '//div[contains(@class,"seller-info-name")]/a/@href')
        loader.add_xpath('description', '//div[contains(@class, "item-description-text")]')
        loft_item = loader.load_item()
        loft_item['url'] = response.url
        loft_item['params'] = param_items
        loft_item['coordinates'] = coord_item
        return loft_item
