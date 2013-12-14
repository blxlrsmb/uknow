#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: fetch.py
# $Date: Sat Dec 14 17:32:48 2013 +0800
# $Author: Vury Leo <i@vuryleo.com>

from items import login, course as Course, item as Item, item_name_dict
from uklogger import log_exc

from BeautifulSoup import BeautifulSoup

def innerHTML(soupNode):
    return "".join([unicode(x) for x in soupNode.contents])

def fetch(username, password):
    items = []
    courses = login(username, password)
    for i in courses[:1]:
        print u'parsing {} ...'.format(i['name'])
        course = Course(i)
        for itemtype in item_name_dict:
            for j in course.get_item_list(itemtype):
                thisitem = Item(j, itemtype)
                item = {'id': thisitem.get_url() }
                item['create_time'] = j['time']
                if itemtype == 'notice':
                    desc = u"公告"
                    data = thisitem.get_data()
                    soup = BeautifulSoup(data)
                    item['title'] = soup.find('td', {'class': 'tr_l2'}).getText()
                    item['content'] = innerHTML(
                            soup.findAll('td', {'class': 'tr_l2'})[1])
                elif itemtype == 'homework':
                    desc = u"作业"
                    data = thisitem.get_data()
                    soup = BeautifulSoup(data)
                    item['title'] = soup.find( 'td',
                        {'class':'tr_2'}).getText().replace('&nbsp;', '')
                    item['content'] = u'截止时间: ' + j['due_time'] + '\n'
                    item['content'] += innerHTML(soup.find('textarea'))
                elif itemtype == 'download':
                    desc = u"课程文件"
                    item['title'] = thisitem.item_dict['name']
                    item['content'] = \
                        u'下载地址:<a href="{}">{}</a>'.format(
                            thisitem.get_url(), item['title'])
                item['title'] = i['name'] + ' ' + desc + '\n' + item['title']
                items.append(item)
    return items

if __name__=='__main__':
    from test_config import username, password
    entries = fetch(username, password)
    for entry in entries:
        #print entry['title'], entry['id']
        #print entry['content']
        print entry['create_time']
