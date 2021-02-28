import os
import requests
from flask import request, current_app as app, jsonify
from lib.storage import Storage
from config import Config
from constant import NO_PATTERN_RESPONSE

conf = Config.get(os.environ.get('FLASK_ENV'), Config['default'])
storage = Storage.get(conf.storage)(conf)
DEFAULT_HEADERS = {}


def imock_data():
    if request.method == 'DELETE':
        data = request.json
        storage.remove(storage.make_key(data))

        return jsonify({'code': 0, 'data': storage.to_dict()})
    elif request.method == 'POST':
        data = request.json
        key = storage.make_key(data)
        storage.set(key, data)

        return jsonify({'code': 0, 'data': storage.to_dict()})
    else:
        return jsonify({'code': 0, 'data': storage.to_dict()})


def imock():
    url = '/'

    return make_response(url, request, conf, storage)


def imock_match(path):
    url = '/' + path

    return make_response(url, request, conf, storage)


def match_mock(url, request, storage):
    key_default = f"{request.host}:{url}:{request.method}"
    key_without_host = f"*:{url}:{request.method}"
    key_without_method = f"{request.host}:{url}:*"
    key_without_host_method = f"*:{url}:*"

    return storage.get(key_default) or storage.get(key_without_host) or \
            storage.get(key_without_method) or storage.get(key_without_host_method)


def get_proxy_response(req):
    app.logger.info("starting proxy")
    method = req.method
    url = req.url
    headers = dict(req.headers)
    req_instance = getattr(requests, method.lower())

    if method in ['GET', 'HEAD', 'OPTIONS']:
        rep = req_instance(url, headers=headers)
    elif method in ['PUT', 'POST', 'DELETE']:
        data = req.data or req.form
        files = req.files
        if files:
            header_str = ['Content-Type', 'content-type']
            for h in header_str:
                if h in headers:
                    headers.pop(h)
        rep = req_instance(url, data=data, files=files, headers=headers)
    else:
        return '', 200, DEFAULT_HEADERS

    header_str = ['Connection', 'connection', 'Transfer-Encoding', 'transfer-encoding', 'Content-Encoding', 'content-encoding']
    for h in header_str:
        if h in rep.headers:
            rep.headers.pop(h)

    rep_headers = dict(rep.headers)
    return rep.content, rep.status_code, {**rep_headers, **DEFAULT_HEADERS}


def make_response(url, request, conf, storage):
    default_rep = '', 200, DEFAULT_HEADERS
    mock = match_mock(url, request, storage)
    no_pattern_response = None

    if mock:      # mock set
        app.logger.info('match mock mode')
        data = mock.get('data', '')
        if data:
            headers = mock.get('headers', {})
            data = merge_data(mock, request)
            return data, mock.get('code', 200), {**headers, **DEFAULT_HEADERS}

        no_pattern_response = mock.get('no_pattern_response')

    app.logger.info('no mock set')
    no_pattern_response = no_pattern_response or conf.no_pattern_response
    if no_pattern_response == NO_PATTERN_RESPONSE.PROXY:
        app.logger.info('match proxy mode')
        if request.host in conf.proxy_exclude:
            app.logger.info('proxy exclude: %s' % conf.proxy_exclude)
            return default_rep
        return get_proxy_response(request)

    return default_rep


def merge_data(mock, req):
    # 动态参数化类型，返回格式化后的结果作为mock内容
    if mock.get('type') == 'dynamic':
        if req.method in ['POST', 'PUT', 'DELETE']:
            if 'application/json' in req.headers.get('Content-Type', ''):
                kw = req.json()
            else:
                kw = req.form
        else:
            kw = req.args
        data = mock.get('data').format(**kw)
    # Python表达式类型，返回表达式执行的结果作为mock内容
    elif mock.get('type') == 'express':
        data = eval(mock.get('data'))
    # 默认为纯文本
    else:
        data = mock.get('data')

    return data
