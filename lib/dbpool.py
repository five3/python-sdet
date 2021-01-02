import records
from urllib import parse


class DBPool:
    db_pool = {}

    @staticmethod
    def get_conn(db_host=None, db_name=None, db_port=3306, db_user='root',
                 db_passwd='root', db_charset='utf8'):
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
