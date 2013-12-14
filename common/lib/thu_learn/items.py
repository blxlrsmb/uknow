#!/usr/bin/python
# -*- coding=UTF-8 -*-

baseurl = 'https://learn.tsinghua.edu.cn/MultiLanguage'
loginurl = baseurl + '/lesson/teacher/loginteacher.jsp'
courselist_url = baseurl + '/lesson/student/MyCourse.jsp?language=cn'
noticelist_url = baseurl + '/public/bbs/getnoteid_student.jsp'
downloadlist_url = baseurl + '/lesson/student/download.jsp'
homeworklist_url = baseurl + '/lesson/student/hom_wk_brw.jsp'
homework_url = baseurl + '/lesson/student/hom_wk_detail.jsp'
notice_url = baseurl + '/public/bbs/note_reply.jsp'
download_url = 'http://learn.tsinghua.edu.cn/uploadFile/downloadFile_student.jsp'
url_dict = locals()
version_news_url = 'http://learn.tsinghua.edu.cn:8080/2011011262/version_news'

item_name_dict = {'download':u'课程文件',
        'homework':u'课程作业',
        'notice':u'课程公告'}

import urllib
import cookielib
import urllib2
from MySoupParser import *
from BeautifulSoup import BeautifulSoup, NavigableString

def login(user, password, if_this_only = True):
    try:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        urllib2.install_opener(opener)
        para = urlencode({'userid':user, 'userpass':password})
        urllib2.urlopen(loginurl, para)
        first_html = urllib2.urlopen(courselist_url).read()
        ret = tuple()
        if not if_this_only:
            terms = termlist_parser_soup(first_html).terms
            for i in terms:
                this_html = urllib2.urlopen(courselist_url.rpartition('/')[0] + '/' + i['url']).read()
                ret += courselist_parser_soup(this_html).courses
        ret += courselist_parser_soup(first_html).courses
        return ret
    except urllib2.HTTPError:
        raise RuntimeError(u'用户名密码错误\n')

class course:
    def __init__(self, course_dict):
        self.course_dict = course_dict
    def get_item_list(self, itemtype):
        url = url_dict[itemtype + 'list_url'] + '?' + urlencode(self.course_dict)
        f = urllib2.urlopen(url).read()
        f = f.replace(r'&nbsp;', ' ')
        return itemlist_parser_soup(f, itemtype).items

class item:
    def __init__(self, item_dict, itemtype):
        self.item_dict = item_dict
        self.itemtype = itemtype
    def get_url(self):
        return url_dict[self.itemtype + '_url'] + '?' + urlencode(self.item_dict)
    def get_data(self, if_format = True, out = sys.stdout):
        url = url_dict[self.itemtype + '_url'] + '?' + urlencode(self.item_dict)
        out.write(u'\t正在获取  '+item_name_dict[self.itemtype]+'   '+self.item_dict['name']+'...\n')
        data = urllib2.urlopen(url).read()

        data_soup = BeautifulSoup(data)
        data = unicode(data_soup).encode('UTF-8')
        return data
    def download_data(self, filepath, size_limit=0, type_except=tuple(), type_only=tuple(), out = sys.stdout):
        if self.itemtype == 'homework':
            return self.download_attachment(filepath, out = out)
        url = url_dict[self.itemtype + '_url'] + '?' + urlencode(self.item_dict)
        obj = urllib2.urlopen(url)
        filename = obj.info().get('Content-Disposition')
        if filename == None:
            out.write(u'\t\t文件不存在。\n\n')
            return
        filename = os.path.join(filepath, filename.partition('filename="')[2][:-1].decode('gb18030'))
        obj_type = filename.rpartition('.')[2]
        out.write(u'\t正在处理  ' + item_name_dict[self.itemtype] +'   '+ self.item_dict['name'] + '...\n' )
        if os.path.exists(filename) and int(os.path.getsize(filename)) == int(obj.info().get('Content-Length')):
            out.write(u'\t\t文件已存在，忽略 \n\n')
            return
        if size_limit != 0  and int(obj.info().get('Content-Length')) > size_limit:
            out.write(u'\t\t文件太大，忽略\n\n')
            return
        if (len(type_only) !=0 and obj_type not in type_only) or obj_type in type_except:
            out.write(u'\t\t文件类型不匹配，忽略 \n\n')
            return
        fout = open(filename, 'wb')
        while True:
            _little_data = obj.read(1024)
            if len(_little_data) == 0:
                break
            fout.write(_little_data)
        fout.close()
        out.write(u'\t\t下载成功。\n\n')
    def download_attachment(self, filepath, out = sys.stdout):
        attach_url = urllib2.urlopen(url_dict[self.itemtype+'_url']+'?'+urlencode(self.item_dict)).read().partition('<a target="_top" href="')[2].partition('">')[0]
        if attach_url == '':
            out.write(u'\t正在处理  ' + item_name_dict[self.itemtype] +'   '+ self.item_dict['name'] + '...\n')
            out.write(u'\t\t无附件\n\n')
            return
        attach_dict = urldecode(attach_url)
        attach_dict['name'] = self.item_dict['name']
        return item(attach_dict, 'download').download_data(filepath, out = out)

import pickle
def get_version_news():
    try:
        data = urllib2.urlopen(version_news_url, timeout = 3)
        return pickle.load(data)
    except:
        return None
