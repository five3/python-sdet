import os
import json
import requests


class HTTPRequest(object):
    def __init__(self, data):
        self.data = data
        self.response = None
        self.log = []
        self.result = None

    def warp_request(self):
        d = {}
        method = self.data['method']
        d['headers'] = json.loads(self.data['headers']) if self.data['headers'] else None
        if method in ('POST', 'PUT', 'DELETE'):
            if self.data['fileList']:
                d['data'] = json.loads(self.data['body'])
            else:
                d['data'] = self.data['body']
            for f in self.data['fileList']:
                fp = os.path.join(os.getcwd(), 'files', f['fn'])
                d.setdefault('files', []).append((f['key'], (f['name'], open(fp, 'rb'), f['type'])))

        return d

    def do_request(self):
        try:
            req = getattr(requests, self.data['method'].lower())
            self.log.append('method：%s' % self.data['method'])
            kw = self.warp_request()
            self.log.append('url：%s' % self.data['url'])
            for k, v in kw.items():
                self.log.append(f'{k}：{v}')
            self.response = req(self.data['url'], **kw)
            self.log.append('response：\r\n%s' % self.response.content.decode('utf-8'))
        except Exception as e:
            self.log.append('exception：\r\n%s' % e)
            self.result = 3

    def validate(self):
        validate = self.data['validate']
        express = self.data['express']
        text = self.response.content.decode('utf-8') if self.response else None
        response = self.response    # 用于python表达式引用， 勿删

        self.log.append('validate：\r\n%s' % validate)
        self.log.append('express：\r\n%s' % express)
        try:
            if validate == 'contain':
                self.result = 1 if express in text else 2
            elif validate == 'express':
                self.result = 1 if eval(express) is True else 2
            else:   # equal
                self.result = 1 if express == text else 2
        except Exception as e:
            self.log.append('exception：\r\n%s' % e)
            self.result = 3
