from datetime import datetime
import pymongo

from loft_parser.items import LoftItem, LoftDataItem
from loft_parser import settings


def get_collection():
    connection = pymongo.MongoClient(
        host=settings.MONGO_HOST,
        username=settings.MONGO_USERNAME,
        password=settings.MONGO_PASSWORD,
    )
    db = connection[settings.MONGO_DB]
    return db[settings.MONGO_COLLECTION]


class MongoPipeline(object):
    def __init__(self):
        self.collection = get_collection()

    @staticmethod
    def _create_document(item: LoftItem) -> dict:
        return {
            **dict(item),  # Все данные объекта сохраняются как есть
            "created": datetime.now(),  # Добавление даты создания объекта
            "updated": datetime.now(),  # Добавление даты последнего изменения объекта
            "data": [],  # Поле в которое сохраняется подробная информация о квартире
        }

    def _add_loft(self, loft_item):
        if not self.collection.find_one({"url": loft_item["url"]}):
            self.collection.insert_one(document=self._create_document(item=loft_item))

    def _add_loft_data(self, loft_data_item):
        # Преобразование перед сохранением в бд
        item_data = dict(loft_data_item)
        del item_data["url"]  # Это поле не нужно, так как будет содержаться в верхнем уровне объекта
        item_data["version"] = datetime.now()

        if self.collection.find_one({"url": loft_data_item["url"]}):
            self.collection.update_one(
                filter={"url": loft_data_item["url"]},
                update={"$push": {"data": item_data}, "$set": {"updated": datetime.now()}}
            )
        else:  # Если для данных о квартире не нашлось объекта в бд, его можно создать
            document = self._create_document(item=LoftItem(url=loft_data_item["url"]))
            document["data"] = [item_data]
            self.collection.insert_one(document=document)

    def process_item(self, item, spider):
        # Сохранение ссылки на страницу с информацией о квартире
        if isinstance(item, LoftItem):
            self._add_loft(loft_item=item)

        # Сохранение информации о квартире
        elif isinstance(item, LoftDataItem):
            self._add_loft_data(loft_data_item=item)

        return item
