from flask import jsonify, request


def login():
    data = request.json
    if data.get('username') == 'admin' and data.get('password') == '111111':
        return jsonify({
            "code": 0,
            "data": {
                "token": "123"
            },
            "msg": ''
        })
    else:
        return jsonify({
            "code": 20001,
            "data": {},
            "msg": '登录失败'
        })


def get_user_info():
    return jsonify({
        "code": 0,
        "data": {
            "roles": ['admin'],
            "name": 'admin',
            "avatar": 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            "introduction": 'introduction'
        },
        "msg": '获取信息成功'
    })


def logout():
    return jsonify({
        "code": 0,
        "data": {},
        "msg": '退出登录成功'
    })
