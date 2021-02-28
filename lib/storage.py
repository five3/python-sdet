import abc
import json
import records


class BaseStorage(metaclass=abc.ABCMeta):
    @staticmethod
    def make_key(data):
        return f"{data.pop('host', '*')}:{data.pop('url', '/')}:{data.pop('method', '*').upper()}"

    @abc.abstractmethod
    def get(self, k, d=None):
        pass

    @abc.abstractmethod
    def set(self, k, v):
        pass

    @abc.abstractmethod
    def remove(self, k):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def __contains__(self, k):
        pass


class MemoryStorage(BaseStorage):
    def __init__(self, conf):
        super().__init__()
        self.mem = {}

    def get(self, k, d=None):
        return self.mem.get(k, d)

    def set(self, k, v):
        self.mem[k] = v

    def remove(self, k):
        del self.mem[k]

    def to_dict(self):
        return self.mem

    def __str__(self):
        return json.dumps(self.mem)

    def __contains__(self, k):
        return k in self.mem


class MysqlStorage(BaseStorage):
    def __init__(self, conf):
        super().__init__()
        self.mysql_conn = conf.mysql_conn
        self.db = self.db_conn()

    def db_conn(self):
        return records.Database(self.mysql_conn, pool_recycle=600)

    def get(self, k, d=None):
        sql = '''select code, headers, `data`, no_pattern_response, `type` from http_mock where `key`=:key'''
        row = self.db.query(sql, key=k).one(d, True)
        if row:
            row['headers'] = json.loads(row['headers'])

        return row

    def set(self, k, v):
        sql = '''insert into http_mock (`key`, code, headers, `data`, no_pattern_response, `type`) 
                values (:key, :code, :headers, :data, :no_pattern_response, :type)
                ON DUPLICATE KEY UPDATE code=:code, headers=:headers, `data`=:data, 
                no_pattern_response=:no_pattern_response, `type`=:type'''
        self.db.query(sql, key=k, code=v.get('code', ''), headers=json.dumps(v.get('headers', {}))
                      , data=v.get('data', ''), no_pattern_response=v.get('no_pattern_response', ''),
                      type=v.get('type', ''))

    def remove(self, k):
        sql = '''delete from http_mock where `key`=:key'''
        self.db.query(sql, key=k)

    def to_dict(self):
        sql = '''select `key`, code, headers, `data`, no_pattern_response, `type` from http_mock'''
        return self.db.query(sql).all(as_dict=True)

    def __str__(self):
        sql = '''select `key`, code, headers, `data`, no_pattern_response, `type` from http_mock'''
        return json.dumps(self.db.query(sql).all(as_dict=True))

    def __contains__(self, k):
        sql = '''select count(id) as `total` from http_mock where `key`=:key'''
        total = self.db.query(sql, key=k).one().total

        return True if total > 0 else False


Storage = {
    'memoryStorage': MemoryStorage,
    'mysqlStorage': MysqlStorage,
    'default': MemoryStorage
}
