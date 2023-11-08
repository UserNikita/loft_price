import asyncio
from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from umongo.frameworks import MotorAsyncIOInstance

instance = MotorAsyncIOInstance()
connection = None


async def init_mongo(mongodb_uri: str, mongodb_db_name: str) -> AsyncIOMotorDatabase:
    loop = asyncio.get_event_loop()
    conn = AsyncIOMotorClient(mongodb_uri, io_loop=loop)
    return conn.get_database(name=mongodb_db_name)


async def close_mongo(app: web.Application) -> None:
    app['db'].client.close()


async def setup_mongo(app: web.Application) -> None:
    config = app['config']
    app['db'] = await init_mongo(config.MONGODB_URI, config.MONGODB_DATABASE)
    instance.set_db(app['db'])
    app.on_cleanup.append(close_mongo)
