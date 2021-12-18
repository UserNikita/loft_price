BOT_NAME = 'loft_parser'

SPIDER_MODULES = ['loft_parser.spiders']
NEWSPIDER_MODULE = 'loft_parser.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 3

COOKIES_ENABLED = False

# Раскомментировать для сохранения данных локально в файловой системе
# FEED_FORMAT = 'json'
# FEED_EXPORT_INDENT = 0
# FEED_EXPORT_ENCODING = 'utf-8'
# FEED_URI = 'storage/%(name)s_%(time)s.json'

DOWNLOADER_MIDDLEWARES = {
    # 'loft_parser.middlewares.LoftParserDownloaderMiddleware': 750,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
}

ITEM_PIPELINES = {
    'loft_parser.pipelines.MongoPipeline': 300,
}

# Авито часто возвращает 429 при блокировке. Нет смысла пытаться запрашивать страницу в ту же секунду
RETRY_ENABLED = False

# Часто редиректы ведут на капчу, поэтому нет смысла редиректиться
REDIRECT_ENABLED = False
