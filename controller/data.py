import json
import time
from flask import request, current_app as app, jsonify
from constant import SQLTYPE, DBKEYTYPE
from lib.dbpool import DBPool


def idata():
    return jsonify(query(request.json))


def warp_db_conn_info(data):
    d = {}
    keys = ['db_host', 'db_port', 'db_name', 'db_user', 'db_passwd', 'db_charset']
    for key in keys:
        if key in data and data[key]:
            d[key] = data[key].strip() if isinstance(data[key], (str, bytes)) else data[key]

    return d


def query(data):
    """
    根据DB和SQL信息执行远程查询并返回结果
    :param data:     {
        "db_host": "x.x.x.x",
        "db_port": 3306,
        "db_name": "test",
        "db_user": "root",
        "db_passwd": "root",
        "db_charset": "utf8",
        "sql": "select * from tbl_key_info where id=:id limit 1",
        "param": {
            "id": 100110
        },
        "key": "all"
    }
    :return: {
        "success": True,
        "data": [{"id": 100110, "xxx", "xxx"}],
        "type": "SELECT",
        "msg": ""
    }
    """
    app.logger.info(f'query data {json.dumps(data)}')
    ret = {
        "success": False,
        "code": -1,
        "data": [],
        "type": None,
        "msg": None
    }

    if not data:
        return ret

    conn_info = warp_db_conn_info(data)
    db_conn = DBPool.get_conn(**conn_info)
    if not db_conn:
        ret['msg'] = '连接目标DB失败，请确认连接信息是否正确'
        return ret

    sql = data.get('sql')
    if not sql:
        ret['msg'] = '查询语句不能为空'
        return ret

    st = time.time()
    app.logger.info(f'查询语句: {sql}, 查询参数: {data.get("param")}')
    rows = db_conn.query(sql, **data.get('param'))
    results = []

    upper_sql = sql.upper().strip()
    if upper_sql.startswith(SQLTYPE.INSERT):
        sql_type = SQLTYPE.INSERT
    elif upper_sql.startswith(SQLTYPE.UPDATE):
        sql_type = SQLTYPE.UPDATE
    elif upper_sql.startswith(SQLTYPE.DELETE):
        sql_type = SQLTYPE.DELETE
    elif upper_sql.startswith(SQLTYPE.SELECT):
        sql_type = SQLTYPE.SELECT
        key = data.get('key', DBKEYTYPE.FIRST)
        if key == DBKEYTYPE.ALL:
            results = rows.as_dict()
        else:  # 为了减少网络传输，默认只查询一行
            first = rows.first(as_dict=True)
            results = [first] if first else []
    else:
        sql_type = SQLTYPE.UNKNOWN

    et = time.time()
    ret.update(
        {
            "success": True,
            "code": 0,
            "data": results,
            "time_cost": et - st,
            "type": sql_type,
            "msg": ''
        }
    )

    app.logger.info(f'查询结果: {results}')
    return ret
