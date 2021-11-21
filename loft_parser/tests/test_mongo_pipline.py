import unittest
import pymongo

from loft_parser.items import LoftItem, LoftDataItem
from loft_parser.pipelines import MongoPipeline, DB_NAME, COLLECTION_NAME


class MongoPipelineTestCase(unittest.TestCase):
    def setUp(self) -> None:
        connection = pymongo.MongoClient(host='mongo', username='root', password='123')
        db = connection[DB_NAME]
        self.collection = db[COLLECTION_NAME]

        self.loft_item = LoftItem(
            url="https://example.com",
            city="City",
            rent="Rent"
        )
        self.loft_data_item = LoftDataItem(
            **{
                'description': 'Description',
                'params': [
                    {'key': 'Год постройки', 'value': '2016'},
                    {'key': 'Тип дома', 'value': 'Монолитный'},
                    {'key': 'Тип перекрытий', 'value': 'Железобетонные'},
                    {'key': 'Подъезды', 'value': '3'},
                    {'key': 'Отопление', 'value': 'Котел/Квартирное отопление'},
                    {'key': 'Аварийность', 'value': 'Нет'},
                    {'key': 'Газоснабжение', 'value': 'Центральное'},
                ],
                'price': 8500,
                'price_period': '₽/мес.',
                'seller_url': 'https://example.com/seller/id/',
                'url': 'https://example.com'
            }
        )

    def tearDown(self) -> None:
        self.collection.drop()

    def test_save_loft_item(self):
        self.assertEqual(self.collection.find_one({"url": self.loft_item["url"]}), None)

        MongoPipeline().process_item(item=self.loft_item, spider=None)

        saved_loft_item = self.collection.find_one({"url": self.loft_item["url"]})
        self.assertTrue(saved_loft_item.pop("_id"))
        self.assertTrue(saved_loft_item.pop("created"))
        self.assertListEqual(saved_loft_item.pop("data"), [])
        self.assertDictEqual(saved_loft_item, dict(self.loft_item))

    def test_save_loft_data_item(self):
        self.assertEqual(self.collection.find_one({"url": self.loft_data_item["url"]}), None)

        MongoPipeline().process_item(item=self.loft_data_item, spider=None)

        saved_loft_item = self.collection.find_one({"url": self.loft_data_item["url"]})
        self.assertTrue("created" in saved_loft_item)
        self.assertTrue(saved_loft_item["data"][0].pop("version"))
        del self.loft_data_item["url"]
        self.assertListEqual(saved_loft_item["data"], [dict(self.loft_data_item)])

    def test_save_two_versions_of_loft_data_item(self):
        price_diff = 1000
        old_price = self.loft_data_item["price"]
        new_price = self.loft_data_item["price"] + price_diff

        self.assertEqual(self.collection.find_one({"url": self.loft_data_item["url"]}), None)

        MongoPipeline().process_item(item=self.loft_data_item, spider=None)
        self.loft_data_item["price"] = new_price
        MongoPipeline().process_item(item=self.loft_data_item, spider=None)

        saved_loft_item = self.collection.find_one({"url": self.loft_data_item["url"]})
        # Удаление полей добавленных при сохранении в бд
        del saved_loft_item["_id"]
        del saved_loft_item["created"]
        del saved_loft_item["data"][0]["version"]
        del saved_loft_item["data"][1]["version"]
        # Удаление поля из исходных данных, которое не сохраняется в бд за ненадобностью
        del self.loft_data_item["url"]

        expected = {
            "url": self.loft_item["url"],  # Только это поле есть в LoftDataItem
            "data": [
                {
                    **dict(self.loft_data_item, price=old_price),
                },
                {
                    **dict(self.loft_data_item, price=new_price),
                },
            ]
        }
        self.assertDictEqual(saved_loft_item, expected)

    def test_save_loft_data_item_if_loft_item_exist(self):
        self.assertEqual(self.collection.find_one({"url": self.loft_data_item["url"]}), None)
        self.assertEqual(self.loft_item["url"], self.loft_data_item["url"])

        MongoPipeline().process_item(item=self.loft_item, spider=None)
        MongoPipeline().process_item(item=self.loft_data_item, spider=None)

        saved_loft_item = self.collection.find_one({"url": self.loft_data_item["url"]})

        # Удаление полей добавленных при сохранении в бд
        del saved_loft_item["_id"]
        del saved_loft_item["created"]
        del saved_loft_item["data"][0]["version"]
        # Удаление поля из исходных данных, которое не сохраняется в бд за ненадобностью
        del self.loft_data_item["url"]

        expected = {
            **self.loft_item,
            "data": [
                {
                    **dict(self.loft_data_item)
                },
            ]
        }
        self.assertDictEqual(saved_loft_item, expected)
