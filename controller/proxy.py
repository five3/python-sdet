import requests
import logging
from flask import request
from .plugins import pre_proxy, post_proxy

DEFAULT_HEADERS = {}


def hproxy_data():
    if request.method == 'GET':
        return 'get'
    else:
        return 'post'


def reload_plugins():
    pre_proxy.clear()
    post_proxy.clear()

    # TODO: get plug info
    # TODO: dinamic load plug


def hproxy():
    return get_proxy_response(request)


def hproxy_match(sub_path):
    return get_proxy_response(request)


def get_proxy_response(req):
    logging.info("starting proxy")
    method = req.method
    url = req.url
    headers = dict(req.headers)
    req_instance = getattr(requests, method.lower())
    context = {'request': req}
    pre_proxy.fire(context)

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

    context['response'] = rep
    post_proxy.fire(context)
    header_str = ['Connection', 'connection', 'Transfer-Encoding', 'transfer-encoding', 'Content-Encoding', 'content-encoding']
    for h in header_str:
        if h in rep.headers:
            rep.headers.pop(h)

    rep_headers = dict(rep.headers)
    return rep.content, rep.status_code, {**rep_headers, **DEFAULT_HEADERS}


reload_plugins()
