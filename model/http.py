import os
import time
import json
import logging
from flask import request
from . import get_db, query_with_pagination
from lib.http import HTTPRequest


def save_file():
    if not request.files:
        return None

    l = []
    for k, v in request.files.items():
        ext = v.filename.rsplit('.', 1)[1]
        id = int(time.time())
        fn = f'{id}.{ext}'
        fp = os.path.join(os.getcwd(), 'files', fn)
        v.save(fp)
        l.append({'name': v.filename, 'fn': fn, 'url': f'/files/{fn}', 'id': id, 'type': v.content_type})

    return l


def delete_file():
    try:
        data = request.json
        fp = os.path.join(os.getcwd(), data['url'][1:])
        os.remove(fp)

        return True
    except Exception as e:
        logging.exception(e)
        return False


def save_api():
    data = request.json
    if data.get('id'):
        sql = '''update http_api set name=:name, url=:url, method=:method, body=:body, headers=:headers, fileList=:fileList, validate=:validate, express=:express where id=:id'''
    else:
        sql = '''insert into http_api (name, url, method, body, headers, fileList, validate, express) values (:name, :url, :method, :body, :headers, :fileList, :validate, :express)'''

    data['fileList'] = json.dumps(data['fileList'])
    get_db().query(sql, **data)

    return {
        "code": 0,
        "success": True,
        "data": '',
        "msg": None
    }


def get_api():
    id = request.args.get('id')
    sql = '''select * from http_api where id=:id'''
    row = get_db().query(sql, id=id).first(as_dict=True)

    return {
        "code": 0,
        "success": True,
        "data": row,
        "msg": None
    }


def warp_query(data):
    cond = ''
    if data.get('name'):
        cond += ' and name=:name'
    if data.get('url'):
        cond += ' and url=:url'
    if data.get('method'):
        cond += ' and method=:method'
    if data.get('date1'):
        cond += ' and created_time between :date1 and :date2'

    return cond


def get_api_list():
    data = request.args
    page = int(data.get('pageNum', 1))
    size = int(data.get('pageSize', 10))
    cond = warp_query(data)
    sql = f'''select * from http_api where 1=1 {cond} order by id desc'''
    conn = get_db()
    rows, total = query_with_pagination(conn, sql, param=data, page=page, size=size)

    return {
        "code": 0,
        "success": True,
        "data": {
            "list": rows,
            "page": {
                "total": total,
                "pageNum": page,
                "pageSize": size
            }
        },
        "msg": None
    }


def debug_request():
    hr = HTTPRequest(request.json)
    hr.do_request()
    hr.validate()

    return {
        'result': hr.result,
        'log': hr.log
    }


def run_request(id):
    sql = '''select * from http_api where id=:id'''
    row = get_db().query(sql, id=id).first(as_dict=True)
    row['fileList'] = json.loads(row['fileList']) if row['fileList'] else []

    hr = HTTPRequest(row)
    hr.do_request()
    hr.validate()

    sql = '''insert into http_api_log (api_id, result, logtext) values (:id, :result, :logtext)'''
    get_db().query(sql, id=id, result=hr.result, logtext=json.dumps(hr.log))
    sql = '''update http_api set status=:result where id=:id'''
    get_db().query(sql, id=id, result=hr.result)

    return {
        'result': hr.result,
        'log': hr.log
    }


def get_log(id):
    sql = '''select logtext from http_api_log where api_id=:id order by id desc limit 1'''
    row = get_db().query(sql, id=id).first(as_dict=True)

    return row['logtext'] if row else '没有查找到用例日志'
