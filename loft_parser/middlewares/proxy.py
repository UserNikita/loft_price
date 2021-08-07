from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware


class LoftParserDownloaderMiddleware(HttpProxyMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxies = {
            "https": [None, "https://185.38.111.1:8080"]
        }
        print('PROXY MID')
