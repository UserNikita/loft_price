import aiohttp_cors
from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from app.db import setup_mongo
# from .app.models import ensure_indexes
from app.views import routes
from app.config import Config


def create_app(config: Config = None) -> web.Application:
    config = config or Config()
    app = web.Application()
    app['config'] = config
    app.on_startup.append(setup_mongo)
    app.on_startup.append(setup_mongo)
    # app.on_startup.append(ensure_indexes)  # in production should be in CD stage
    app.add_routes(routes)

    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        }
    )
    for route in list(app.router.routes()):
        cors.add(route)

    setup_aiohttp_apispec(app=app, swagger_path=r"/api/docs")
    return app


if __name__ == '__main__':
    config = Config()
    app = create_app(config=config)
    web.run_app(app, port=config.PORT)
