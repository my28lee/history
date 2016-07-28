#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint

memo_api = Blueprint('memo_api', __name__)

from . import views