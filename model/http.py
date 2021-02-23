import os
import time
import json
import logging
from flask import request
from . import get_db, query_with_pagination


def save_file(files):
    if not files:
        return None

    l = []
    for k, v in files.items():
        ext = v.filename.rsplit('.', 1)[1]
        uid = int(time.time())
        fn = f'{uid}.{ext}'
        fp = os.path.join(os.getcwd(), 'files', fn)
        v.save(fp)
        l.append({'name': v.filename, 'fn': fn, 'url': f'/files/{fn}', 'id': uid, 'type': v.content_type})

    return l


def delete_file(data):
    try:
        fp = os.path.join(os.getcwd(), data['url'][1:])
        os.remove(fp)

        return True
    except Exception as e:
        logging.exception(e)
        return False


def save_api(data):
    if data.get('id'):
        sql = '''update http_api set name=:name, url=:url, method=:method, body=:body, headers=:headers, fileList=:fileList, validate=:validate, express=:express where id=:id'''
    else:
        sql = '''insert into http_api (name, url, method, body, headers, fileList, validate, express) values (:name, :url, :method, :body, :headers, :fileList, :validate, :express)'''

    data['fileList'] = json.dumps(data['fileList'])
    get_db().query(sql, **data)


def get_api(aid):
    sql = '''select * from http_api where id=:id'''
    row = get_db().query(sql, id=aid).first(as_dict=True)
    row['fileList'] = json.loads(row['fileList']) if row['fileList'] else []

    return row


def warp_query(data):
    cond = ''
    if data.get('name'):
        cond += ' and name=:name'
    if data.get('url'):
        cond += ' and url=:url'
    if data.get('method'):
        cond += ' and method=:method'

    return cond


def get_api_list(data):
    page = int(data.get('pageNum', 1))
    size = int(data.get('pageSize', 10))
    cond = warp_query(data)
    sql = f'''select * from http_api where 1=1 {cond} order by id desc'''
    conn = get_db()
    rows, total = query_with_pagination(conn, sql, param=data, page=page, size=size)

    return {
        "list": rows,
        "page": {
            "total": total,
            "pageNum": page,
            "pageSize": size
        }
    }


def api_log(aid, result, info):
    sql = '''insert into http_api_log (api_id, status, content) values (:id, :status, :content)'''
    get_db().query(sql, id=aid, status=result, content=json.dumps(info))
    sql = '''update http_api set status=:status where id=:id'''
    get_db().query(sql, id=aid, status=result)


def get_log_by_api_id(aid):
    sql = '''select content from http_api_log where api_id=:id order by id desc limit 1'''
    row = get_db().query(sql, id=aid).first(as_dict=True)

    return row['content'] if row else '["没有查找到用例日志"]'


def get_log_list():
    data = request.args
    page = int(data.get('pageNum', 1))
    size = int(data.get('pageSize', 10))
    cond = warp_query(data)
    sql = f'''select b.*, a.name, a.url, a.method from http_api a, http_api_log b where a.id=b.api_id {cond} order by b.id desc'''
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


def get_log_by_id(lid):
    sql = '''select content from http_api_log where id=:id'''
    row = get_db().query(sql, id=lid).first(as_dict=True)

    return row['content'] if row else '["没有查找到用例日志"]'
