import os
from flask import Flask
from controller.mock import imock, imock_match, imock_data
from config import Config

conf = Config.get(os.environ.get('FLASK_ENV'), Config['default'])


def create_app():
    app = Flask(__name__, static_url_path='/do_not_use_this_path__')
    app.config.from_object(conf)

    app.route('/', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS'])(imock)
    app.route('/<path:path>', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS'])(imock_match)
    app.route('/api/_mock_settings_', methods=['GET', 'POST', 'DELETE'])(imock_data)

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=80, debug=True, threaded=True)
