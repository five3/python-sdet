from . import get_db

conn = get_db()


def get_all_plugins():
    sql = '''select * from hook'''
    return conn.query(sql).all(as_dict=True)


def get_proxy_plugins(params):
    page_num = int(params.get('pageNum', 1))
    page_size = int(params.get('pageSize', 10))

    start = (page_num - 1) * page_size
    sql = '''select * from hook limit :start,:step'''
    rows = conn.query(sql, start=start, step=page_size).all(as_dict=True)

    sql = '''select count(id) as total from hook'''
    row = conn.query(sql).first()

    return {
        "list": rows,
        "page": {
            "pageNum": page_num,
            "pageSize": page_size,
            "total": row.total
        }
    }


def save_proxy_plugin(data):
    id = data.get('id')
    if id:
        sql = '''update hook set name=:name, `type`=:type, source=:source, target=:target, content=:content
                where id=:id'''
    else:
        sql = '''insert into hook (name, `type`, source, target, content) values (:name, :type, :source, :target, :content)'''

    conn.query(sql, **data)
