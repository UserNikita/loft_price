from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


def strip(value):
    return value.strip() or None


class LoftItem(Item):
    url = Field()
    city = Field()
    rent = Field()


class LoftDataItem(Item):
    url = Field()
    address = Field(input_processor=MapCompose(strip), output_processor=TakeFirst())
    price = Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    price_period = Field(input_processor=MapCompose(strip), output_processor=TakeFirst())
    seller_name = Field(input_processor=MapCompose(strip), output_processor=TakeFirst())
    seller_url = Field(output_processor=TakeFirst())
    description = Field(output_processor=TakeFirst())
    params = Field()
    coordinates = Field()


class CoordinateItem(Item):
    lat = Field(input_processor=MapCompose(float), output_processor=TakeFirst())
    lon = Field(input_processor=MapCompose(float), output_processor=TakeFirst())


class ParamItem(Item):
    key = Field(input_processor=MapCompose(strip), output_processor=TakeFirst())
    value = Field(input_processor=MapCompose(strip), output_processor=TakeFirst())


class CianLoftItemLoader(ItemLoader):
    default_item_class = LoftDataItem
    price_in = MapCompose(lambda value: int("".join(value.split()[:-1])))
    price_period_in = MapCompose(lambda value: value.split()[-1])
