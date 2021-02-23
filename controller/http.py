from flask import jsonify
from model.http import *
from lib.http import HTTPRequest
from lib.decorators import log_context


def http_save():
    """
    用例保存、用例信息获取处理函数
    """
    if request.method == 'GET':
        ret = get_api(request.args.get('id', 0))
    else:
        ret = save_api(request.json)

    return jsonify({
        "code": 0,
        "success": True,
        "data": ret,
        "msg": None
    })


def http_file():
    """
    用例文件保存、删除处理函数
    """
    if request.method == 'POST':
        ret = save_file(request.files)
    else:
        ret = delete_file(request.json)

    if ret:
        return jsonify({"code": 0, "data": ret, "msg": ""})
    else:
        return '操作文件失败', 500, {}


def http_debug():
    """用例调试处理函数"""
    hr = HTTPRequest(request.json)
    hr.do_request()
    hr.validate()

    return jsonify({
        "code": 0,
        "data": {
            "result": hr.result,
            "log": hr.log
        },
        "msg": ""
    })


def http_run(aid):
    """
    用例运行处理函数
    """
    row = get_api(aid)
    hr = HTTPRequest(row)
    hr.do_request()
    hr.validate()
    api_log(aid, hr.result, hr.log)

    return jsonify({
        "code": 0,
        "data": {
            "result": hr.result,
            "log": hr.log
        },
        "msg": ""
    })


def http_api_log(aid):
    """
    用例日志查询处理函数
    """
    ret = get_log_by_api_id(aid)
    return jsonify({"code": 0, "data": ret, "msg": ""})


@log_context()
def http_list():
    """
    用例列表查询处理函数
    """
    return {
        "code": 0,
        "success": True,
        "data": get_api_list(request.args),
        "msg": None
    }


@log_context()
def http_log_list():
    """
    用例日志查询处理函数
    """
    return get_log_list()


def http_log(lid):
    """
    用例日志详情处理函数
    """
    ret = get_log_by_id(lid)
    return jsonify({"code": 0, "data": ret, "msg": ""})
