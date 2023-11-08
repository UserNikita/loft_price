from datetime import datetime
from typing import AsyncIterable
from aiohttp.web_exceptions import HTTPNotFound
from bson import ObjectId
from .models import Apartment


async def get_apartment_list() -> AsyncIterable[Apartment]:
    return Apartment.find()


async def get_apartment(item_id: ObjectId) -> Apartment:
    item = await Apartment.find_one({'_id': item_id})
    if not item:
        raise HTTPNotFound()
    return item


async def create_apartment(data: dict) -> Apartment:
    item = Apartment(**data)
    await item.commit()
    return item


async def update_apartment(item_id: ObjectId, data: dict) -> Apartment:
    item = await get_apartment(item_id)
    item.update(data)
    # item.updated_time = datetime.utcnow()
    await item.commit()
    return item


async def delete_apartment(item_id: ObjectId) -> None:
    item = await get_apartment(item_id)
    await item.delete()
