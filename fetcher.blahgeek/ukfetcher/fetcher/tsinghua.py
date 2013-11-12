#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# Created at Apr 10 20:18 by BlahGeek@Gmail.com

import requests
from BeautifulSoup import BeautifulSoup

class Tsinghua:

    @staticmethod
    def getInfoNotices():
        ''' info.tsinghua notices, return a list'''
        URL = 'http://info.tsinghua.edu.cn/html/view/notice_beforelogin.htm'
        r = requests.get(URL)
        soup = BeautifulSoup(r.content)
        notices = map(lambda x: x.text.strip(), soup.findAll('td'))
        notices = filter(lambda x: len(x) > 0, notices)
        return notices

    @staticmethod
    def _libNewsParse(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        content = soup.find(id='content').find('tbody')
        news = content.findAll('tr')
        return map(lambda x: x.find('a').text.strip(), news)

    @staticmethod
    def getLibNotices():
        ''' notice from lib.tsinghua, return a list'''
        URL = 'http://lib.tsinghua.edu.cn/dra/news/announcement'
        return Tsinghua._libNewsParse(URL)

    @staticmethod
    def getLibEres():
        ''' return a list'''
        URL = 'http://lib.tsinghua.edu.cn/dra/news/eres'
        return Tsinghua._libNewsParse(URL)


if __name__ == '__main__':
    for i in Tsinghua.getInfoNotices():
        print i.encode('utf8')
    for i in Tsinghua.getLibNotices():
        print i
    for i in Tsinghua.getLibEres():
        print i
