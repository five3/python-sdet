import records
from urllib import parse


class DBPool:
    db_pool = {}

    @staticmethod
    def get_conn(db_host=None, db_name=None, db_port=3306, db_user='autoax',
                 db_passwd='autoax', db_charset='utf8'):
        if db_host is None or db_name is None:
            raise ValueError("host and db_name can't be None.")

        key = DBPool.make_uniq_key(db_host, db_port, db_name)
        if key not in DBPool.db_pool:
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


def sync_employee():
    import requests

    conn_info = {'db_host': '10.168.96.94', 'db_name': 'atmp'}
    conn = DBPool.get_conn(**conn_info)

    data = requests.get('http://oa.corpautohome.com/sapweb/api/hrdata?name=employee&syscode=dealeradvadmin').json()
    conn.query('truncate employee')
    rows = []
    sql = '''insert into employee (hrcode, email, account, name, sex, dept_id, dept_name, work_city, status) 
            values (:hrcode, :email, :account, :name, :sex, :dept_id, :dept_name, :work_city, :status)'''
    for r in data['Data']:
        d = {
            'hrcode': r['HRCode'],
            'email': r['Email'],
            'account': r['AccountName'],
            'name': r['Name'],
            'sex': r['Sex'],
            'dept_id': r['DeptID'],
            'dept_name': r['DeptName'],
            'work_city': r['WorkCity'],
            'status': r['Status']
        }
        rows.append(d)

        if len(rows) == 50:
            conn.bulk_query(sql, rows)
            rows = []


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


if __name__ == '__main__':
    sync_project()
