from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from umongo import ValidationError
from bson import ObjectId
from bson.objectid import InvalidId
from . import services
from . import schemas

APARTMENT_API_PATH = r"/api/apartments"
OBJECT_ID_REGEX = r"{apartment_id:\w{24}}"

routes = web.RouteTableDef()


@docs(tags=["apartment"])
@routes.get(APARTMENT_API_PATH)
async def list_apartments(request):
    items = await services.get_apartment_list()
    data = [item.dump() async for item in items]
    return web.json_response(data, status=200)


@docs(tags=["apartment"])
@request_schema(schemas.CreateApartmentSchema)
@response_schema(schemas.ApartmentSchema)
@routes.post(APARTMENT_API_PATH)
async def create_apartment(request):
    try:
        schema = schemas.CreateApartmentSchema()
        data = schema.load(await request.json())
    except ValidationError as e:
        return web.json_response(e.messages_dict, status=web.HTTPBadRequest.status_code)
    item = await services.create_apartment(data)
    return web.json_response(item.dump(), status=201)


@docs(tags=["apartment"])
@response_schema(schemas.ApartmentSchema)
@routes.get(f"{APARTMENT_API_PATH}/{OBJECT_ID_REGEX}")
async def get_apartment(request):
    try:
        item_id = ObjectId(request.match_info["apartment_id"])
    except InvalidId as e:
        raise web.HTTPBadRequest(reason=e.messages)
    item = await services.get_apartment(item_id)
    return web.json_response(item.dump(), status=200)


@docs(tags=["apartment"])
@request_schema(schemas.UpdateApartmentSchema)
@response_schema(schemas.ApartmentSchema)
@routes.put(f"{APARTMENT_API_PATH}/{OBJECT_ID_REGEX}")
async def update_apartments(request: web.Request) -> web.Response:
    try:
        item_id = ObjectId(request.match_info["apartment_id"])
    except InvalidId as e:
        raise web.HTTPBadRequest(reason=e.messages)

    try:
        schema = schemas.UpdateApartmentSchema()
        data = schema.load(await request.json())
    except ValidationError as e:
        return web.json_response(e.messages_dict, status=web.HTTPBadRequest.status_code)
    item = await services.update_apartment(item_id, data)
    return web.json_response(item.dump(), status=200)


@docs(tags=["apartment"])
@routes.delete(f"{APARTMENT_API_PATH}/{OBJECT_ID_REGEX}")
async def delete_apartment(request: web.Request) -> web.Response:
    try:
        item_id = ObjectId(request.match_info["apartment_id"])
    except InvalidId as e:
        raise web.HTTPBadRequest(reason=e.messages)
    await services.delete_apartment(item_id)
    return web.json_response({}, status=204)
