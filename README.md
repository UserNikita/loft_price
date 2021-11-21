# LOFT PRICE
Web-приложение для визуализации стоимости аренды жилья на карте города

### Запуск

1. Клонировать репозиторий
    ```bash
    git clone https://github.com/UserNikita/loft_price.git
    ```
2. Перейти в папку проекта
3. Запустить докер контейнеры
    ```bash
    docker-compose up -d
    ```
4. Заполнить ClickHouse данными
    ```bash
   docker exec -ti web python loaddata.py 
   ```
5. Открыть в браузере страницу с адресом *http://127.0.0.1:5000*

### Сбор данных

Пауки работают в двух режимах
1. Сбор ссылок на страницы с описаниями квартир
2. Сбор информации со страницы конкретной квартиры

**Команда для сбора ссылок на квартиры**

```bash
docker exec -ti backend scrapy crawl <spider> -a city=<city> -a rent=<rent>
```

`spider` - паук для сбора данных, доступные значения `avito` и `cian`

`city` - название города. Пример: `ulyanovsk`.
По умолчанию используется `ulyanovsk`

`rent` - типа аренды. 
Доступные значения: `day` - посуточно, `month` - на длительный срок, `forever` - покупка (доступно для avito). 
По умолчанию используется `month`.

**Команда для сбора информации о конкретной квартире**

```bash
docker-compose exec backend scrapy crawl -a loft_url=<url>
```

`url` - ссылка на страницу квартиры

### Запуск тестов

```bash
python -m unittest discover
```

### Скриншоты
![Screenshot1](./screenshots/screen1.png)
![Screenshot2](./screenshots/screen2.png)