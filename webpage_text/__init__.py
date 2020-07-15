import os
import re
import sys
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

gevent.get_hub().NOT_ERROR += (KeyboardInterrupt,)

PORT = 1683

endpoint_dict = {}
default_dict = {}

default_endpoint = 'defaults'

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
        data = request.json
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
    host = '0.0.0.0'
    text = ''
    size = 100
    refresh = 1.0
    use_flask = False
    enable_log = False

    parser = argparse.ArgumentParser(description='Start a web server to display text on a web page.')
    parser.add_argument(
        '-c', '--config',
        help='path to a configuration file (INI format)'
    )
    parser.add_argument(
        '-H', '--host', default=host,
        help='hostname or IP address of the server [default={}]'.format(host)
    )
    parser.add_argument(
        '-p', '--port', default=PORT, type=int,
        help='port to run the server on [default={}]'.format(PORT)
    )
    parser.add_argument(
        '-e', '--endpoints', nargs='*',
        help='the names of the URL endpoints'
    )
    parser.add_argument(
        '-t', '--text', default=text, nargs='*',
        help='initial text to display at each endpoint [default={!r}]'.format(text)
    )
    parser.add_argument(
        '-s', '--size', default=size, type=int,
        help='font size (in px) of the text [default={}]'.format(size)
    )
    parser.add_argument(
        '-r', '--refresh', default=refresh, type=float,
        help='number of seconds for a web browser to wait before automatically '
             'refreshing the web page [default={}]'.format(refresh)
    )
    parser.add_argument(
        '-l', '--log', action='store_true', help='show INFO log messages from the gevent WSGI server'
    )
    parser.add_argument(
        '-f', '--flask', action='store_true', help='use the flask development server in debug mode'
    )

    if not args:
        args = sys.argv[1:]
    args = parser.parse_args(args)

    if args.config is not None:
        if not os.path.isfile(args.config):
            sys.exit('FileNotFoundError: ' + args.config)
        ini = configparser.ConfigParser()
        ini.read(args.config)
        host = ini.get('server', 'host', fallback=host)
        port = ini.getint('server', 'port', fallback=PORT)
        endpoints = [e.strip() for e in ini.get('server', 'endpoints', fallback='').split(',') if e.strip()]
        use_flask = ini.getboolean('server', 'use_flask', fallback=use_flask)
        enable_log = ini.getboolean('server', 'enable_log', fallback=enable_log)
        text = ini.get('text', 'initial', fallback=text)
        size = ini.getint('text', 'size', fallback=size)
        refresh = ini.getfloat('text', 'refresh', fallback=refresh)
    else:
        host = args.host
        port = args.port
        endpoints = args.endpoints
        use_flask = args.flask
        enable_log = args.log
        text = ' '.join(args.text) if args.text else args.text
        size = args.size
        refresh = args.refresh

    if not endpoints:
        sys.exit('You must specify at least 1 endpoint')

    for endpoint in endpoints:
        if endpoint == default_endpoint:
            sys.exit('The name of an endpoint cannot be {!r} because this name is reserved'.format(default_endpoint))
        print('Added endpoint http://{}:{}/{}'.format(host, port, endpoint))
        endpoint_dict[endpoint] = {'text': text, 'size': size, 'refresh': refresh}

    default_dict['size'] = size
    default_dict['refresh'] = refresh

    if use_flask:
        # use the development server from flask
        app.run(host=host, port=port, debug=True)
    else:
        print('Server running on http://{}:{}/ (Press CTRL+C to quit)'.format(host, port))
        log = 'default' if enable_log else None
        server = pywsgi.WSGIServer((host, port), application=app.wsgi_app, log=log)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


def put(text, endpoint, host='127.0.0.1', port=PORT, size=None, refresh=None):
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
    url = 'http://{}:{}/'.format(host, port)

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
