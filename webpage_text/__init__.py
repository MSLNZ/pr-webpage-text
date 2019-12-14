import os
import sys
import json
import argparse
import configparser

from gevent import monkey
monkey.patch_all()

import gevent
from gevent import pywsgi

from flask import (
    Flask,
    Markup,
    render_template,
    request,
    send_from_directory,
)

lab_dict = {}

gevent.get_hub().NOT_ERROR += (KeyboardInterrupt,)

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(ignore):
    return render_template('page_not_found.html', names=lab_dict, url=request.host_url), 404


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<lab>', methods=['GET', 'PUT'])
def page(lab):
    if lab not in lab_dict:
        return page_not_found(lab)
    if request.method == 'PUT':
        data = json.loads(request.data)
        data['text'] = Markup(data['text'].replace(r'\n', '<br>'))
        lab_dict[lab].update(data)
    return render_template('page.html', lab=lab, **lab_dict[lab])


def run(*args):
    if not args:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Start a web server to handle HTML requests.')
    parser.add_argument('--config', '-c', default='config.ini', help='the path to the configuration file')
    args = parser.parse_args(args)
    if not os.path.isfile(args.config):
        sys.exit('FileNotFoundError: ' + args.config)

    ini = configparser.ConfigParser()
    ini.read(args.config)
    host = ini.get('server', 'host', fallback='127.0.0.1')
    port = ini.getint('server', 'port', fallback=1683)
    use_flask_server = ini.getboolean('server', 'use_flask_server', fallback=False)
    text = ini.get('defaults', 'text', fallback='')
    size = ini.getint('defaults', 'size', fallback=200)
    refresh = ini.getfloat('defaults', 'refresh', fallback=1.0)
    for value in ini.get('endpoints', 'values').split(','):
        lab_dict[value.strip()] = {'text': text, 'size': size, 'refresh': refresh}

    if use_flask_server:
        # use the development server from flask
        app.run(host=host, port=port, debug=True)
    else:
        print('Running on http://{}:{}/ (Press CTRL+C to quit)'.format(host, port))
        server = pywsgi.WSGIServer((host, port), application=app.wsgi_app)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
