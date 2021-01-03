import re
from flask import Flask
from controller import proxy


def create_app():
    app = Flask(__name__, static_url_path='/do_not_use_this_path__')
    app.route('/api/_plugs_settings_', methods=['GET', 'POST'])(proxy.hproxy_data)
    app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])(proxy.hproxy)
    app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])(proxy.hproxy_match)

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=80, debug=True)
