from flask import jsonify, request
from model.todo import *
from . import warp_date_field


def todo():
    data = request.json

    if data.get('id'):  # 更新任务
        ret = update_todo(data)
    else:   # 新增任务
        ret = create_todo(data)

    code = 0 if ret else -1

    return jsonify({
        "code": code,
        "msg": '',
        "data": ret
    })


def get_todo_list():
    tab = request.args.get('tab')
    if tab == 'current':
        ret = get_current_todo()
    elif tab == 'unfinish':
        ret = get_unfinish_todo()
    elif tab == 'finished':
        ret = get_finished_todo()
    else:
        ret = []

    ret = warp_date_field(ret)

    return jsonify({
        "code": 0,
        "msg": '',
        "data": ret
    })
