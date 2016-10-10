#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from flask import render_template,request,Response,stream_with_context, jsonify,g,redirect,url_for
from . import memo_blueprint
from ..diff import svncheck
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers.diff import DiffLexer
from pygments.formatters import HtmlFormatter

@memo_blueprint.route('/')
def index():
    return redirect(url_for('.svn_path_select'))

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

ConfigParser = None

@memo_blueprint.route('/history')
def svn_path_select():
    global ConfigParser
    if ConfigParser is None:
        import ConfigParser
    config = ConfigParser.ConfigParser();
    config.read('local_history.ini')
    svnurl = config.get('svn','rooturl')
    svn_list = g.db.execute('select * from svn_info order by product asc,s_path_url desc').fetchall()
    return render_template('memo/history_list.html',data = svn_list,rooturl=svnurl)

@memo_blueprint.route('/history_add',methods = ['POST'])
def svn_path_add():
    query = 'INSERT INTO svn_info(product,s_path_url,s_start_revision,s_last_revision) values(?,?,?,?);'
    g.db.execute(query,[request.form.get('product','mf2'),request.form.get('url',''),request.form.get('frev',''),request.form.get('frev','')])
    g.db.commit()
    return redirect(url_for('.svn_path_select'))

@memo_blueprint.route('/history_del/<int:id>')
def svn_path_delete(id):
    global ConfigParser
    if ConfigParser is None:
        import ConfigParser
    config = ConfigParser.ConfigParser();
    config.read('local_history.ini')
    svnurl = config.get('svn','rooturl')
    svn_list = g.db.execute('select * from svn_history where s_path_id='+str(id)).fetchall()
    for row in svn_list:
        g.db.execute('delete from svn_history_file where id='+str(row[0]))

    g.db.execute('delete from svn_history where s_path_id='+str(id))
    g.db.execute('delete from svn_info where s_path_id='+str(id))
    g.db.commit()
    return redirect(url_for('.svn_path_select'))


@memo_blueprint.route('/history/info',methods=['GET','POST'])
def svn_history():
    global ConfigParser
    if ConfigParser is None:
        import ConfigParser
    config = ConfigParser.ConfigParser();
    #SVN 설정 정보 로딩
    config.read('local_history.ini')
    pSvnId = request.args.get('svnid')
    pSID = request.args.get('id')

    path_info = g.db.execute('select * from svn_info where s_path_id=?',[pSID]).fetchall()

    svnrooturl = ''
    if path_info[0][4] == 'mf2' or path_info[0][4] == 'ae':
        svnrooturl = config.get('svn','rooturl')
        svnurl = svnrooturl+path_info[0][1]
    else:
        svnrooturl = config.get('svn','rootmfiurl')
        svnurl = svnrooturl+path_info[0][1]

    print request.args.get('id'),path_info[0][1],path_info[0][2],path_info[0][3]
    s = svncheck(svnrooturl,path_info[0][1],'','',config.get('svn','uid'),config.get('svn','upass'))

    #마지막 리비전 조회
    last_revision = s.getLastRevision()

    resultlist = []

    print 'last_revision',path_info[0][3],last_revision
    #DB에 저장된 최종 리비전이 리파지토리 최종 리비전 보다 작을 경우 변경 로그 조회
    if int(path_info[0][3]) < last_revision:
        cur = g.db.cursor()
        cur.execute('update svn_info set s_last_revision=? where s_path_url=?',[last_revision,path_info[0][1]])
        log = s.diffrence(int(path_info[0][3])+1,last_revision)

        for info in log:
            query = 'INSERT INTO svn_history (s_path_id,s_revision,s_id,s_time,s_comment) VALUES (?,?,?,?,?)'
            cur.execute(query,[path_info[0][0],info.revision.number,info.author,time.ctime(info.date),info.message.          decode('utf8')])
            id = cur.lastrowid
            print 'cur.lastrowid => '+str(id),info.revision.number
            pathlist = []
            for pathinfo in info.changed_paths:
                difftext = None
                #파일이 수정된 경우에만 diff 실행
                if pathinfo.action == 'M':
                    #인코딩 에러가 발생할 경우 빈값으로 셋팅
                    try:
                        difftext = s.getDiffText(info.revision.number,pathinfo.path).decode('utf-8')
                    except:
                        difftext = ''

                query = 'INSERT INTO svn_history_file (svn_id,file_action,file_path,file_diff) VALUES (?,?,?,?)'
                tmpPath = pathinfo.path.decode('utf-8')
                cur.execute(query,[id,pathinfo.action,tmpPath,difftext])

        g.db.commit()
        cur.close()

    if pSvnId:
        query = 'select * from svn_history where s_path_id=? and s_id LIKE ? order by s_revision desc limit 10'
        cur = g.db.execute(query,[path_info[0][0],'%'+pSvnId+'%'])
    else:
        query = 'select * from svn_history where s_path_id=? order by s_revision desc limit 10'
        cur = g.db.execute(query,[path_info[0][0]])

    for row in cur.fetchall():
        subquery = 'select * from svn_history_file where svn_id=?'
        pathlist = []
        sublist = g.db.execute(subquery,[row[0]]).fetchall()
        for subrow in sublist:
            filedata = dict()
            filedata['path'] = subrow[3].replace(str(path_info[0][1]),'')
            filedata['action'] = subrow[2]
            if subrow[4]:
                #diff 텍스트를 보기좋게 포장한다.
                filedata['diff'] = highlight(subrow[4].decode("utf-8"),DiffLexer(),HtmlFormatter())
            else: filedata['diff'] = ''
            pathlist.append(filedata)
        newlist = list(row)
        newlist.append(pathlist)
        resultlist.append(newlist)

    return render_template('memo/history.html',data = resultlist,svnurl=svnurl,svnid=pSvnId,sid=pSID)
