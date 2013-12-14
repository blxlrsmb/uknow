#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: fetch.py
# $Date: Sat Dec 14 14:13:47 2013 +0800
# $Author: Vury Leo <i@vuryleo.com>

from items import login, course as Course, item as Item, item_name_dict
from uklogger import log_exc

from BeautifulSoup import BeautifulSoup

def innerHTML(soupNode):
    return "".join([unicode(x) for x in soupNode.contents])

def fetch(username, password):
    print u'fetch with {}:{}'.format(username, password)
    items = []
    try:
        courses = login(username, password)
        for i in courses:
            print u'parsing {} ...'.format(i['name'])
            course = Course(i)
            for itemtype in item_name_dict:
                for j in course.get_item_list(itemtype):
                    thisitem = Item(j, itemtype)
                    item = {'id': thisitem.get_url() }
                    if itemtype == 'notice':
                        data = thisitem.get_data()
                        soup = BeautifulSoup(data)
                        item['title'] = \
                            soup.find('td', {'class': 'tr_l2'}).getText()
                        item['content'] = \
                            innerHTML(
                                soup.findAll('td', {'class': 'tr_l2'})[1])
                    elif itemtype == 'homework':
                        data = thisitem.get_data()
                        soup = BeautifulSoup(data)
                        item['title'] = soup.find(
                            'td',
                            {'class':'tr_2'}).getText().replace('&nbsp;', '')
                        item['content'] = innerHTML(soup.find('textarea'))
                    elif itemtype == 'download':
                        item['title'] = thisitem.item_dict['name']
                        item['content'] = \
                            u'下载地址:<a href="{}">{}</a>'.format(
                                thisitem.get_url(), item['title'])
                    item['title'] = i['name'] + '\n' + item['title']
                    items.append(item)
    except Exception as e:
        log_exc(str(e))

    return items

if __name__=='__main__':
    from test_config import username, password
    entries = fetch(username, password)
    for entry in entries:
        print u'title:{}\nid:{}\ncontent:{}'.format(entry['title'], entry['id'], entry['content'])
