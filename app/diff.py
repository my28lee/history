#!/usr/bin/python
# -*- coding: utf-8 -*-
import pysvn
import time


class svncheck():

    def __init__(self, svn_root='', svn_user=None, svn_password=None):
        self.user = svn_user
        self.password = svn_password
        self.root = svn_root

    def cat(self,fn,rev):
        client = pysvn.Client()
        client.commit_info_style = 1
        client.callback_notify = self.notify
        client.callback_get_login = self.credentials
        print rev
        st_rev = pysvn.Revision(pysvn.opt_revision_kind.number,rev)

        l = client.log(self.root+fn,
                       revision_end=st_rev,
                       limit=2)
        print l[0].revision, l[1].revision

        print client.list(self.root+fn,
                          recurse=True,
                          dirent_fields=pysvn.SVN_DIRENT_ALL,
                          fetch_locks=False)

    def diffrence(self):

        self.client = pysvn.Client()
        self.client.commit_info_style = 1
        self.client.callback_notify = self.notify
        self.client.callback_get_login = self.credentials

        self.ed_rev = self.client.revpropget("revision", url=self.root)[0].number
        st_rev = 76984
        #print "revision",ed_rev

        print pysvn.Revision( pysvn.opt_revision_kind.committed)

        log  = self.client.log(
        self.root,
        revision_start=pysvn.Revision( pysvn.opt_revision_kind.number, st_rev),
        revision_end=pysvn.Revision( pysvn.opt_revision_kind.number, self.ed_rev),
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
        file_log = self.client.log(self.root+file_path, revision_start=pysvn.Revision(pysvn.opt_revision_kind.number,version), limit=2)
        if(len(file_log) == 2):
            return file_log[1].revision.number
        return None

    def getDiffText(self,rev,path):
        past_rev = self.pastVersion(rev,path)
        #print pathinfo.copyfrom_revision
        if(past_rev != None):
            diff_text = self.client.diff('.',self.root+path,
                revision1=pysvn.Revision(pysvn.opt_revision_kind.number,rev),
                url_or_path2=self.root+path,
                revision2=pysvn.Revision(pysvn.opt_revision_kind.number,past_rev),
                recurse=True,
                ignore_ancestry=False)
            return diff_text
        return None

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF8')

    print sys.getdefaultencoding()
