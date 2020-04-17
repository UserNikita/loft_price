import argparse
import os
import json
import datetime
import logging
from clickhouse_driver import Client
from loft_app import settings


class Loader:
    client = Client(host=settings.CLICKHOUSE_HOST, port=settings.CLICKHOUSE_PORT,
                    user=settings.CLICKHOUSE_USER, password=settings.CLICKHOUSE_PASSWORD)

    def __init__(self, files=None, append=False):
        self.append = append
        if files:
            self.files = files
        else:
            self.files = [
                open(os.path.join('storage', file_name), encoding='UTF-8')
                for file_name in os.listdir('storage')
            ]

    def drop_db(self):
        with open('sql/drop_db.sql') as sql_file:
            self.client.execute(sql_file.read())

    def create_db(self):
        with open('sql/create_db.sql') as sql_file:
            self.client.execute(sql_file.read())

    def create_table(self):
        with open('sql/create_table.sql') as sql_file:
            self.client.execute(sql_file.read())

    def load_data(self):
        f = open('sql/insert.sql')
        insert_sql = f.read()
        f.close()

        if not self.append:
            self.drop_db()
        self.create_db()
        self.create_table()

        now = datetime.datetime.now()

        for f in self.files:
            data = json.loads(f.read())
            loft_list = []
            for i, loft in enumerate(data):
                try:
                    loft_list.append({
                        'datetime': now,
                        'price': int(loft['price']),
                        'lat': loft['coordinates']['lat'],
                        'lon': loft['coordinates']['lon'],
                    })
                except KeyError:
                    # Файлы для которых не удалось получить координаты или цену
                    logging.error('KeyError in json_file={json} line={i}'.format(json=f.name, i=i))
            self.client.execute(insert_sql, loft_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r', encoding='UTF-8'), nargs='*',
                        help="Путь к json файлу для загрузки в бд")
    parser.add_argument('--append', default=False, action='store_true',
                        help="Добавлять записи в бд без пересоздания")
    args = parser.parse_args()
    Loader(files=args.file, append=args.append).load_data()
