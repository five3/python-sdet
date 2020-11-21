from flask import Flask
from controller.index import index


def create_app():
    app = Flask(__name__)
    app.route('/')(index)

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=80, debug=True)
