import records
from urllib import parse


class DBPool:
    db_pool = {}

    @staticmethod
    def get_conn(db_host=None, db_name=None, db_port=3306, db_user='autoax',
                 db_passwd='FKyw#2020', db_charset='utf8'):
        if db_host is None or db_name is None:
            raise ValueError("host and db_name can't be None.")

        key = DBPool.make_uniq_key(db_host, db_port, db_name)
        if key not in DBPool.db_pool:
            # CONFIG.logger.info(f'new a db connection for {key}')
            sql_str = DBPool.make_conn_str(db_host, db_name, db_port, db_user, db_passwd, db_charset)
            DBPool.db_pool[key] = records.Database(sql_str, pool_pre_ping=True)

        try:
            db = DBPool.db_pool[key]
            db.query('''select 1''')
        except:
            db = None
            del DBPool.db_pool[key]

        return db

    @staticmethod
    def make_uniq_key(db_host, db_name, db_port):
        return f'{db_host}:{db_port}:{db_name}'

    @staticmethod
    def make_conn_str(db_host, db_name, db_port, db_user, db_passwd, db_charset):
        return f'mysql+pymysql://{db_user}:{parse.quote_plus(db_passwd)}@{db_host}:{db_port}/{db_name}?charset={db_charset}'


def loop_project(conn, data):
    sql = '''insert into prd_project (id, text) values (:id, :text)'''
    for i in data:
        # print(i)
        conn.query(sql, **i)

        if i.get('children'):
            loop_project(conn, i['children'])


def sync_project():
    import json, os

    conn_info = {'db_host': '10.168.96.94', 'db_name': 'atmp'}
    conn = DBPool.get_conn(**conn_info)

    f = os.path.join(os.path.dirname(__file__), '../static/project.json')
    with open(f, 'r', encoding='utf-8') as fr:
        content = json.loads(fr.read())

    loop_project(conn, content['data'])


def save_bin():
    sql = '''insert into rap (record_key, url, method, code, response) values ('xx', 'hhh', 'post', 200, :response)'''
    conn_info = {'db_host': '10.168.96.94', 'db_name': 'atmp'}
    DBPool.get_conn(**conn_info).query(sql, response=b'xxxx')

    sql = '''select response from rap order by id desc'''
    row = DBPool.get_conn(**conn_info).query(sql).first(as_dict=True)
    print(row)


if __name__ == '__main__':
    save_bin()
