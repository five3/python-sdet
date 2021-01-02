import time
import json
import logging
import decimal
from json import JSONEncoder
from datetime import datetime, date
from functools import wraps
from flask import current_app


class ComplexEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, bytes):
            return str(obj)
        elif isinstance(obj, decimal.Decimal):
            return int(obj) if int(obj) == float(obj) else float(obj)
        else:
            return super().default(obj)


def log_context(when=['before']):
    def warp(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if 'before' in when:
                print('before')

            ts = time.time()
            ret = func(*args, **kwargs)
            te = time.time()
            if isinstance(ret, dict):
                ret['time_cost'] = te - ts

            if 'after' in when:
                print('after')

            logging.info(f'response: {ret}')
            return current_app.response_class(
                json.dumps(ret, indent=2, cls=ComplexEncoder) + "\n",
                mimetype=current_app.config["JSONIFY_MIMETYPE"],
                headers={'Access-Control-Allow-Origin': '*'}
            )
        return inner
    return warp
