#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask

from app_middleware import HTTPMethodOverrideMiddleware

app = Flask(__name__)


def create_app():
    from memo import memo_blueprint
    app.register_blueprint(memo_blueprint)

    from memo_api import memo_api
    app.register_blueprint(memo_api,url_prefix='/api')

    # method overwrite
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    return app