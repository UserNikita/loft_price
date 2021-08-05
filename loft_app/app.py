from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from clickhouse_driver import Client
import requests
from . import settings
from . import color_schemes

app = Flask(__name__)
cors = CORS(app)


def get_color_by_price(price, color_scheme):
    colors = color_scheme
    for c in colors:
        if price < c[0]:
            return c[1]
    return colors[-1]


client = Client(
    host=settings.CLICKHOUSE_HOST, port=settings.CLICKHOUSE_PORT,
    user=settings.CLICKHOUSE_USER, password=settings.CLICKHOUSE_PASSWORD
)


@app.route('/api/h3/')
def h3():
    h3_resolution = int(request.args.get('resolution', default=10))
    color_scheme = getattr(color_schemes, request.args.get('color_scheme', '').upper(), color_schemes.RED)

    query = """
        SELECT count(), round(avg(price), 2), hex(h3_resolution_{resolution}) as h3 FROM loft.price GROUP BY h3
    """.format(resolution=h3_resolution)

    data = []
    for entry in client.execute_iter(query=query):
        avg_price = entry[1]
        color = get_color_by_price(price=avg_price, color_scheme=color_scheme)
        hexagon = {
            'color': color,
            'h3': entry[2],
            'count': entry[0],
            'avg_price': avg_price,
        }
        data.append(hexagon)
    return jsonify(data)


@app.route('/api/detail/')
def detail():
    h3_index = request.args.get('h3_index')
    h3_resolution = int(request.args.get('resolution', default=9))

    query = """
        SELECT price, lat, lon, h3_resolution_{resolution} FROM loft.price 
        WHERE h3_resolution_{resolution} = reinterpretAsUInt64(reverse(unhex(%(h3_index)s)))
    """.format(resolution=h3_resolution)

    data = [x for x in client.execute_iter(query=query, params={'h3_index': h3_index})]
    return jsonify(data)


@app.route('/proxy/')
def proxy_list():
    https_proxies = [
        {
            'id': proxy,
            'proxy': proxy,
            'country': '',
            'elapsed': None,
        }
        for i, proxy in enumerate(set(settings.PROXY_LIST.split()))
    ]

    return jsonify(https_proxies)


@app.route('/proxy/check')
def proxy_check():
    # url = 'https://api.ipify.org/?format=json'
    # url = 'https://api.2ip.ua/geo.json'
    url = 'https://ipwhois.app/json/'

    proxy = request.args.get('proxy')

    try:
        response = requests.get(url, proxies={'https': proxy})
        data = {
            'id': proxy,
            'proxy': proxy,
            'country': response.json().get("country", ""),
            'elapsed': str(response.elapsed),
        }
    except:
        data = {
            'id': proxy,
            'proxy': proxy,
            'country': "",
            'elapsed': None,
        }
    return jsonify(data)


@app.route('/')
def index():
    return render_template('index.html')
