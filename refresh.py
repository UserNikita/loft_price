import argparse
from datetime import datetime, timedelta

import pymongo
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from loft_parser import settings
from loft_parser.spiders.avito_spider import AvitoSpider
from loft_parser.spiders.cian_spider import CianSpider


spiders = {
    'avito': AvitoSpider,
    'cian': CianSpider,
}


def get_collection():
    connection = pymongo.MongoClient(
        host=settings.MONGO_HOST,
        username=settings.MONGO_USERNAME,
        password=settings.MONGO_PASSWORD,
    )
    db = connection[settings.MONGO_DB]
    return db[settings.MONGO_COLLECTION]


def get_filter_object(portal_name):
    """Функция возвращает фильтр для выбора документов из базы"""
    return {
        "url": {
            "$regex": portal_name  # Для выбора адресов определённой площадки
        },
        "$or": [
            {
                "data": []  # У объектов нет данных
            },
            {
                "updated": {
                    "$lte": datetime.utcnow() - timedelta(weeks=1)  # Последнее обновление было неделю назад
                }
            },
        ]
    }


def get_start_urls_by_portal_name(portal_name: str, limit: int = 100):
    collection = get_collection()
    documents = collection.find(filter=get_filter_object(portal_name=portal_name), projection={"url": 1}).limit(limit)
    start_urls = [doc["url"] for doc in documents]
    return start_urls


def start_crawling(portal_name: str):
    spider_class = spiders[portal_name]
    start_urls = get_start_urls_by_portal_name(portal_name=portal_name)

    print("Start refresh data for %s" % spider_class)
    print("urls:", start_urls, sep='\n')

    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_class, start_urls=start_urls)
    process.start()
    print("Refreshed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('portal', choices=["avito", "cian"], help="Площадка с которой нужно парсить данные")
    args = parser.parse_args()

    start_crawling(portal_name=args.portal)
