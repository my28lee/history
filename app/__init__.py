#!/usr/bin/python
# -*- coding:utf-8 -*-
import re

from flask import Flask, Markup, escape
from jinja2.filters import evalcontextfilter

from app_middleware import HTTPMethodOverrideMiddleware

app = Flask(__name__)
#app.jinja_env.autoescape = False
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

def create_app():
    from memo import memo_blueprint
    app.register_blueprint(memo_blueprint)

    from memo_api import memo_api
    app.register_blueprint(memo_api,url_prefix='/api')

    # method overwrite
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    return app

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'%s<br>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(value))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result