import os
from flask import Flask
from controller.index import index
from controller.user import login, get_user_info, logout
from controller.todo import todo, get_todo_list
from controller.data import idata
from config import Config

conf = Config.get(os.environ.get('FLASK_ENV'), Config['default'])


def create_app():
    app = Flask(__name__, static_url_path='/do_not_use_this_path__')
    app.config.from_object(conf)

    app.route('/')(index)
    app.route('/api/user/login', methods=['POST'])(login)
    app.route('/api/user/info')(get_user_info)
    app.route('/api/user/logout', methods=['POST'])(logout)
    app.route('/api/todo', methods=['POST'])(todo)
    app.route('/api/todo/list')(get_todo_list)
    app.route('/api/idata', methods=['POST'])(idata)

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=80, debug=True, threaded=True)
