from flask import render_template
from model.db import do_something_in_db


def index():
    do_something_in_db()
    return render_template('index.html')
