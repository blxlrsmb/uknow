#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# Created at Apr 10 20:18 by BlahGeek@Gmail.com

from . import register_fetcher
from ukitem import TextOnlyItem
from ukdbconn import DuplicateKeyError
from uklogger import log_fetcher as log_info

import requests
from BeautifulSoup import BeautifulSoup


class Tsinghua:

    @staticmethod
    def getInfoNotices():
        ''' info.tsinghua notices, return a list'''
        URL = 'http://info.tsinghua.edu.cn/html/view/notice_beforelogin.htm'
        r = requests.get(URL)
        soup = BeautifulSoup(r.content)
        notices = []
        for i in soup.findAll('td'):
            item = {}
            item['title'] = i.text.strip()
            if len(item['title']) == 0:
                continue
            item['link'] = i.find('a')['href']
            if not item['link'].startswith('http://'):
                item['link'] = URL.replace("notice_beforelogin.htm",
                                           item['link'])
            notices.append(item)
        return notices

    @staticmethod
    def _libNewsParse(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        content = soup.find(id='content').find('tbody')
        notices = []
        for i in content.findAll('td',
                                 {'class': 'views-field views-field-title'}):
            item = {}
            item['title'] = i.text.strip()
            item['link'] = i.find('a')['href']
            if not item['link'].startswith('http://'):
                item['link'] = 'http://lib.tsinghua.edu.cn' + item['link']
            notices.append(item)
        return notices

    @staticmethod
    def getLibNotices():
        ''' notice from lib.tsinghua, return a list'''
        URL = 'http://lib.tsinghua.edu.cn/dra/news/announcement'
        return Tsinghua._libNewsParse(URL)


@register_fetcher('tsinghua_portal', sleep_time=1800)
def tsinghua_portal_fetcher(ctx):
    """fetcher portal.tsinghua.edu.cn, save each title with tag `portal`"""
    coll = ctx.get_mongo_collection()

    for entry in Tsinghua.getInfoNotices():
        try:
            coll.insert({'_id': entry['link']})
        except DuplicateKeyError:
            continue
        ctx.new_item(TextOnlyItem(entry['title'], ""), ['Tsinghua info'],
                     other={"id": entry['link']})
        log_info(u'Tsinghua Info: new entry: {} {}'.format(entry['link'],
                                                           entry['title']))
    for entry in Tsinghua.getLibNotices():
        try:
            coll.insert({'_id': entry['link']})
        except DuplicateKeyError:
            continue
        ctx.new_item(TextOnlyItem(entry['title'], ""), ['Tsinghua library'],
                     {"id": entry['link']})
        log_info(u'Tsinghua Library: new entry: {} {}'.format(entry['link'],
                                                              entry['title']))
