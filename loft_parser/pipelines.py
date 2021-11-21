from datetime import datetime
import pymongo

from loft_parser.items import LoftItem, LoftDataItem

DB_NAME = 'db'
COLLECTION_NAME = 'loft'


class MongoPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(host='mongo', username='root', password='123')
        db = connection[DB_NAME]
        self.collection = db[COLLECTION_NAME]

    def _add_loft(self, loft_item):
        if not self.collection.find_one({"_id": loft_item["url"]}):
            document = {
                "_id": loft_item["url"],
                "created": datetime.now(),
                "data": [],
            }
            self.collection.insert_one(document=document)

    def _add_loft_data(self, loft_data_item):
        # Преобразование перед сохранением в бд
        item_data = dict(loft_data_item)
        del item_data["url"]
        item_data["version"] = datetime.now()

        if self.collection.find_one({"_id": loft_data_item["url"]}):
            self.collection.update_one(filter={"_id": loft_data_item["url"]}, update={"$push": {"data": item_data}})
        else:
            document = {
                "_id": loft_data_item["url"],
                "created": datetime.now(),
                "data": [item_data],
            }
            self.collection.insert_one(document=document)

    def process_item(self, item, spider):
        # Сохранение ссылки на страницу с информацией о квартире
        if isinstance(item, LoftItem):
            self._add_loft(loft_item=item)

        # Сохранение информации о квартире
        elif isinstance(item, LoftDataItem):
            self._add_loft_data(loft_data_item=item)

        return item
