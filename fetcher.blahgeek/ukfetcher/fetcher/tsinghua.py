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
        notices = []
        for i in soup.findAll('td'):
            item = {}
            item['title'] = i.text.strip()
            if len(item['title']) == 0:
                continue
            item['link'] = i.find('a')['href']
            if not item['link'].startswith('http://'):
                item['link'] = URL.replace("notice_beforelogin.htm", item['link'])
            notices.append(item)
        return notices

    @staticmethod
    def _libNewsParse(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        content = soup.find(id='content').find('tbody')
        notices = []
        for i in content.findAll('td', {'class': 'views-field views-field-title'}):
            item = {}
            item['title'] = i.text.strip()
            item['link'] = i.find('a')['href']
            if not item['link'].startswith('http://'):
                item['link'] = 'http://lib.tsinghua.edu.cn' + item['link']
            notices.append(item)
        #news = content.findAll('tr')
        return notices#map(lambda x: x.find('a').text.strip(), news)

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
        print i['title'].encode('utf8'), i['link']
    for i in Tsinghua.getLibNotices():
        print i['title'].encode('utf8'), i['link']
    for i in Tsinghua.getLibEres():
        print i['title'].encode('utf8'), i['link']
    #for i in Tsinghua.getLibEres():
    #    print i
