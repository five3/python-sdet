from flask import jsonify, request
from model.http import save_file, delete_file, save_api, get_api, get_api_list, debug_request, run_request, get_log
from lib.decorators import log_context


@log_context()
def http_list():
    return get_api_list()


def http_save():
    if request.method == 'GET':
        return jsonify(get_api())
    else:
        return jsonify(save_api())


def http_file():
    if request.method == 'POST':
        ret = save_file()
    else:
        ret = delete_file()

    if ret:
        return jsonify({"code": 0, "data": ret, "msg": ""})
    else:
        return '操作文件失败', 500, {}


def http_debug():
    ret = debug_request()
    return jsonify({"code": 0, "data": ret, "msg": ""})


def http_run(id):
    ret = run_request(id)
    return jsonify({"code": 0, "data": ret, "msg": ""})


def http_log(id):
    ret = get_log(id)
    return jsonify({"code": 0, "data": ret, "msg": ""})
