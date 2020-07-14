import os
import re
import sys
import json
import argparse
import configparser

from gevent import monkey
monkey.patch_all()

import gevent
from gevent import pywsgi
import requests
from flask import (
    Flask,
    Markup,
    render_template,
    request,
    send_from_directory,
)

endpoint_dict = {}
default_dict = {}

default_endpoint = 'defaults'

gevent.get_hub().NOT_ERROR += (KeyboardInterrupt,)

# default values
HOST = '0.0.0.0'
PORT = 1683
SIZE = 100
REFRESH = 1.0

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(*args):
    return render_template('page_not_found.html', names=endpoint_dict.keys(), url=request.host_url), 404


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<name>', methods=['GET', 'PUT'])
def page(name):
    if name not in endpoint_dict:
        return page_not_found()
    if request.method == 'PUT':
        data = json.loads(request.data)
        data['text'] = Markup(re.sub(r'\n|\\n', '<br>', data['text']))
        endpoint_dict[name].update(data)
    return render_template('page.html', title=name, **endpoint_dict[name])


@app.route('/'+default_endpoint, methods=['GET'])
def defaults():
    return default_dict


def run(*args):
    """Run the web server.

    This function is only meant to be called from the command line via the
    `webpage-text` entry point (see setup.py).
    """
    if not args:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Start a web server to handle HTML requests.')
    parser.add_argument('--config', '-c', default='config.ini', help='the path to the configuration file')
    args = parser.parse_args(args)
    if not os.path.isfile(args.config):
        sys.exit('FileNotFoundError: ' + args.config)

    ini = configparser.ConfigParser()
    ini.read(args.config)
    host = ini.get('server', 'host', fallback=HOST)
    port = ini.getint('server', 'port', fallback=PORT)
    use_flask_server = ini.getboolean('server', 'use_flask_server', fallback=False)
    text = ini.get('defaults', 'text', fallback='')
    size = ini.getint('defaults', 'size', fallback=SIZE)
    refresh = ini.getfloat('defaults', 'refresh', fallback=REFRESH)
    for value in ini.get('endpoints', 'values').split(','):
        stripped = value.strip()
        if stripped == default_endpoint:
            sys.exit('The name of an endpoint cannot be {!r} because this name is reserved'.format(default_endpoint))
        endpoint_dict[stripped] = {'text': text, 'size': size, 'refresh': refresh}

    default_dict['size'] = size
    default_dict['refresh'] = refresh

    if use_flask_server:
        # use the development server from flask
        app.run(host=host, port=port, debug=True)
    else:
        print('Running on http://{}:{}/ (Press CTRL+C to quit)'.format(host, port))
        server = pywsgi.WSGIServer((host, port), application=app.wsgi_app, log=None)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


def put(text, endpoint, host=None, port=None, size=None, refresh=None):
    """Update the text that is displayed on a web page.

    The URL of the web page to update follows the ``http://host:port/endpoint`` nomenclature.

    Parameters
    ----------
    text : str
        The text to display on the web page.
    endpoint : str
        The endpoint of the web page's URL.
    host : str, optional
        The hostname or IP address of the web server.
    port : int, optional
        The port number of the web server.
    size : int, optional
        The font size of the `text`.
    refresh : float, optional
        The number of second a web browser will wait before it automatically refreshes.
    """
    h = host or HOST
    if h == '0.0.0.0':
        h = '127.0.0.1'
    p = port or PORT
    url = 'http://{}:{}/'.format(h, p)

    try:
        default = default_dict[url]
    except KeyError:
        default = requests.get(url+'defaults').json()
        default_dict[url] = {'size': default['size'], 'refresh': default['refresh']}

    if size is None:
        size = default['size']

    if refresh is None:
        refresh = default['refresh']

    reply = requests.put(url+endpoint.lstrip('/'), json={'text': text, 'size': size, 'refresh': refresh})
    if not reply.ok:
        matches = re.findall(r'/(\w+)</p>', reply.content.decode())
        raise ValueError('Invalid endpoint {!r}. Must be one of: {}'.format(endpoint, ', '.join(matches)))
