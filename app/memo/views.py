#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from flask import render_template,request,Response,stream_with_context, jsonify
from . import memo_blueprint
from ..diff import svncheck

@memo_blueprint.route('/')
def index():
    return render_template('memo/index.html')

@memo_blueprint.route('/edit',methods=['GET','POST'])
def memo_edit():
    error = None
    if request.method == 'POST':
        return ''

    return render_template('memo/memo_edit.html')

@memo_blueprint.route('/stream')
def streamed_response():
    def generate():
        yield 'Hello'
        yield request.args['name']
        yield '!'
    return Response(stream_with_context(generate()))


@memo_blueprint.route('/history')
def history():
    svnurl = 'abc'
    s = svncheck(svnurl,'abc','abc')
    log = s.diffrence();
    list = []
    for info in log:
        pathlist = []
        for pathinfo in info.changed_paths:
            filedata = dict()
            filedata['path'] = pathinfo.path
            filedata['action'] = pathinfo.action

            if pathinfo.action == 'M':
                difftext = s.getDiffText(info.revision.number,pathinfo.path)
                if difftext != None:
                    filedata['diff'] = difftext
            pathlist.append(filedata)

        list.append({'rev':info.revision.number,'author':info.author,'time':time.ctime(info.date),'message':info.message,'path':pathlist})

    #print list

    return render_template('memo/history.html',data = list,svnurl=svnurl)

@memo_blueprint.route('/history/<name>')
def filecat(name):
    pass