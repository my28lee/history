#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import render_template,jsonify

from . import memo_api

@memo_api.route('/memos',methods=['GET'])
def index():
    list=[
        {'id':'1','memo':'hello test','date':'2016-12-12','tag':'ABC'},
        {'id':'2','memo':'hello test1','date':'2016-12-12','tag':'ABC'},
        {'id':'3','memo':'hello test2','date':'2016-12-12','tag':'ABC'},
        {'id':'4','memo':'hello test3','date':'2016-12-12','tag':'ABC'}
    ]
    return jsonify(results=list)

@memo_api.route('/memos/<id>',methods=['PUT'])
def memo_edit(id):
    memo = {'id':'1','memo':'hello test','date':'2016-12-12','tag':'ABC'}
    return jsonify(results=memo)

@memo_api.route('/memos/<id>',methods=['DELETE'])
def memo_del(id):
    memo = {'id':'1','memo':'hello test','date':'2016-12-12','tag':'ABC'}
    return jsonify(results=memo)

@memo_api.route('/memos',methods=['POST'])
def memo_add():
    memo = {'id':'1','memo':'hello test','date':'2016-12-12','tag':'ABC'}
    return jsonify(results=memo)