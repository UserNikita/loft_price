import os


class Config:
    MONGODB_USER = os.environ.get("MONGODB_USER", "root")
    MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD", "123")
    MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "db")
    MONGODB_HOST = os.environ.get("MONGODB_HOST", "localhost")
    MONGODB_PORT = os.environ.get("MONGODB_PORT", "27017")

    MONGODB_URI = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}"

    PORT = int(os.environ.get("PORT", 8080))
    DEBUG = bool(os.environ.get("DEBUG", True))


# class TestConfig(Config):
#     MONGODB_URI = os.environ.get('MONGODB_TEST_URI', f'mongodb://{MONGODB_HOST}:27017/items_test')
#     DEBUG = True
