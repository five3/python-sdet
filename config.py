import os


def get_ip():
    try:
        ips = os.popen("LANG=C ifconfig | grep \"inet addr\" | grep -v \"127.0.0.1\" | awk -F \":\" '{print $2}' | awk '{print $1}'").readlines()
    except:
        ips = []

    if len(ips) > 0:
        return ips[0].strip()


class base:
    DEBUG = True
    SECRET_KEY = b'=\xf3\x18\xf5s\x9b\x7f\x86A\xcb\x99_\x07cB,1>_\xc3r\xfa\xc3/'
    JSON_AS_ASCII = False

    storage = 'memoryStorage'
    no_pattern_response = 'proxy'       # proxy, empty
    proxy_exclude = ['localhost', '127.0.0.1', get_ip()]


class dev(base):
    pass


class test(base):
    storage = 'mysqlStorage'
    mysql_conn = 'mysql+pymysql://admin:admin@testip:3306/pysdet?charset=utf8'


class prod(base):
    DEBUG = False
    storage = 'mysqlStorage'
    mysql_conn = 'mysql+pymysql://admin:admin@onlineip:3306/pysdet?charset=utf8'


Config = {
    'dev': dev,
    'test': test,
    'prod': prod,
    'default': dev
}
