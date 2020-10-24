import time
import logging
from . import get_db


def update_todo(data):
    sql = '''update todo set name=:name, `desc`=:desc, start_time=:start_time,
            end_time=:end_time, assign=:assign, status=:status where id=:id'''

    try:
        get_db().query(sql, **data)
        return True
    except Exception as e:
        logging.exception(e)
        return False


def create_todo(data):
    sql = '''insert into todo (name, `desc`, start_time, end_time, assign, status) 
            values (:name, :desc, :start_time, :end_time, :assign, :status)'''

    try:
        get_db().query(sql, **data)
        return True
    except Exception as e:
        logging.exception(e)
        return False


def get_current_todo():
    sql = '''select * from todo where status in ('INIT', 'INPROCESS') and start_time < :today and :today < end_time'''
    today = time.strftime("%Y-%m-%d", time.localtime())

    try:
        rows = get_db().query(sql, today=today).all(as_dict=True)
        return rows
    except Exception as e:
        logging.exception(e)
        return []


def get_unfinish_todo():
    sql = '''select * from todo where status in ('INIT', 'INPROCESS')'''

    try:
        rows = get_db().query(sql).all(as_dict=True)
        return rows
    except Exception as e:
        logging.exception(e)
        return []


def get_finished_todo():
    sql = '''select * from todo where status in ('FINISHED', 'DISCARD')'''

    try:
        rows = get_db().query(sql).all(as_dict=True)
        return rows
    except Exception as e:
        logging.exception(e)
        return []
