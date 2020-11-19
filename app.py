from flask import Flask
from controller.proxy import hproxy, hproxy_match, hproxy_data


def create_app():
    app = Flask(__name__)
    app.route('/', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS'])(hproxy)
    app.route('/<path:sub_path>', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS'])(hproxy_match)
    app.route('/api/hproxy', methods=['GET', 'POST'])(hproxy_data)

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=80, debug=True, threaded=True)
