#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint

memo_blueprint = Blueprint('memo', __name__)

from . import views
from ..diff import svncheck