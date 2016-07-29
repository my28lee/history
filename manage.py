#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask.ext.script import Manager

# from werkzeug.contrib.fixers import ProxyFix

from app import create_app

import sys
reload(sys)
sys.setdefaultencoding('UTF8')

app = create_app()
app.config.from_json('..\memo_setting.json')
# app.wsgi_app = ProxyFix(app.wsgi_app)
manager = Manager(app)

@manager.command
def run():
    app.run(host='11.4.9.233',port=80)

if __name__ == "__main__":
    manager.run()