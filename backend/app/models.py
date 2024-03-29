from aiohttp import web
from datetime import datetime
from umongo import Document, fields
from .db import instance


@instance.register
class Item(Document):
    name = fields.StringField(required=True)
    created_time = fields.DateTimeField(default=datetime.utcnow)
    updated_time = fields.DateTimeField()

    class Meta:
        indexes = ['-created_time']


async def ensure_indexes(app: web.Application) -> None:
    await Item.ensure_indexes()


@instance.register
class Apartment(Document):
    url = fields.URLField(required=True)
    address = fields.StringField(required=True)
    price = fields.DecimalField()
    price_period = fields.StringField()

    class Meta:
        collection_name = "apartments"
