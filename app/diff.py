#!/usr/bin/python
# -*- coding: utf-8 -*-
import pysvn
import time
from flask import g


class svncheck():

    def __init__(self, svn_root='',svn_path='',svn_st='',svn_ed='', svn_user=None, svn_password=None):
        '''

        :param svn_root: 프로젝트 SVN ROOT 경로
        :param svn_path: ROOT 경로 이후 서브 경로
        :param svn_st: 시작 리비전 번호
        :param svn_ed: 종료 리비전 번호
        :param svn_user: SVN ID
        :param svn_password: SVN PASSWORD
        :return:
        '''
        self.user = svn_user
        self.password = svn_password
        self.root = svn_root
        self.pathurl = svn_path
        self.start_revision = svn_st
        self.end_revision = svn_ed
        self.client = pysvn.Client()
        self.client.commit_info_style = 1
        self.client.callback_notify = self.notify
        self.client.callback_get_login = self.credentials

    def cat(self,fn,rev):
        st_rev = pysvn.Revision(pysvn.opt_revision_kind.number,rev)

        l = self.client.log(self.root+fn,
                       revision_end=st_rev,
                       limit=2)
        print l[0].revision, l[1].revision

        print self.client.list(self.root+fn,
                          recurse=True,
                          dirent_fields=pysvn.SVN_DIRENT_ALL,
                          fetch_locks=False)
    def getLastRevision(self):
        '''
        repository의 마지막 리비전 정보를 가져온다.
        :return: 마지막 리비전 번호
        '''
        return int(self.client.revpropget("revision", url=self.root+self.pathurl)[0].number)

    def diffrence(self,start_revision,last_revision):
        '''
        시작/종료 리비전 사이 변경된 히스토리 조회
        :param start_revision: 시작 리비전
        :param last_revision: 종료 리비전
        :return: 변경된 히스토리 로그 내역 목록
        '''
        log  = self.client.log(
                self.root+self.pathurl,
                revision_start=pysvn.Revision( pysvn.opt_revision_kind.number, start_revision),
                revision_end=pysvn.Revision( pysvn.opt_revision_kind.number, last_revision),
                discover_changed_paths=True,
                strict_node_history=True,
                limit=0,
                include_merged_revisions=False,
            )
        log.reverse()
        return log

    def notify( event_dict ):
        print event_dict
        return

    def credentials(self,realm, username, may_save):
           return True, self.user, self.password, True

    def pastVersion(self,version,file_path):
        '''
        변경된 파일의 수정전 리비전을 가져온다.
        :param version: 파일의 최종 수정 리비전 번호
        :param file_path: 파일 경로
        :return: 최종 수정 바로전 리비전 번호
        '''
        file_log = self.client.log(self.root+file_path, revision_start=pysvn.Revision(pysvn.opt_revision_kind.number,version), limit=2)
        if(len(file_log) == 2):
            return file_log[1].revision.number
        return None

    def getDiffText(self,rev,path):
        '''
        변경된 파일의 변경 전/후 파일의 diff를 실행한다.
        :param rev: 파일의 최종 리비전 번호
        :param path: 파일 경로
        :return: diff 텍스트
        '''
        past_rev = self.pastVersion(rev,path)
        #print pathinfo.copyfrom_revision
        if(past_rev != None):
            diff_text = self.client.diff('.',self.root+path,
                revision1=pysvn.Revision(pysvn.opt_revision_kind.number,past_rev),
                url_or_path2=self.root+path,
                revision2=pysvn.Revision(pysvn.opt_revision_kind.number,rev),
                recurse=True,
                ignore_ancestry=False)
            return diff_text
        return None

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF8')

    print sys.getdefaultencoding()
