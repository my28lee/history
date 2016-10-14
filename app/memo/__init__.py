#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import g
import sqlite3

memo_blueprint = Blueprint('memo', __name__)

from . import views
from .. import app

@app.before_request
def before_request():
    g.db = sqlite3.connect("database.db",check_same_thread=False)

@app.teardown_appcontext
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()