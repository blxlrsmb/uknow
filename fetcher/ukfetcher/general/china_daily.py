#!/usr/bin/python2
# -*- coding: utf-8 -*-
# $File: china_daily.py
# $Date: Thu Dec 12 13:34:41 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

"""China Daily fetcher. As china daily rss has been categorized automatically,
    the corpora can be used to train text classifier"""

from . import register_fetcher
from functools import wraps
import feedparser
import socket
from ukitem import TextOnlyItem
from ukdbconn import DuplicateKeyError
from uklogger import log_info

class register_china_daily_rss_fetcher(register_fetcher):
    """decorator that register a china daily rss fetcher"""

    CHINA_DAILY_RSS_FETCHER_NAME_PREFIX = 'china_daily_rss_'

    def __init__(self, *args, **kwargs):
        """see :meth:`register_fetcher.__init__`for details;
        additional keyword arguments:
            * category: category of this rss fetcher"""
        category = kwargs.pop('category', 'news')
        register_fetcher.__init__(self, self.CHINA_DAILY_RSS_FETCHER_NAME_PREFIX \
                + category)

rss_list = [
        ('china', 'http://www.chinadaily.com.cn/rss/china_rss.xml'),
        ('bizchina', 'http://www.chinadaily.com.cn/rss/bizchina_rss.xml'),
        ('world', 'http://www.chinadaily.com.cn/rss/world_rss.xml'),
        ('opinion', 'http://www.chinadaily.com.cn/rss/opinion_rss.xml'),
        ('sports', 'http://www.chinadaily.com.cn/rss/sports_rss.xml'),
        ('entertainment',
            'http://www.chinadaily.com.cn/rss/entertainment_rss.xml'),
        ('life',
            'http://www.chinadaily.com.cn/rss/lifestyle_rss.xml'),
        ('photo', 'http://www.chinadaily.com.cn/rss/photo_rss.xml'),
        ('video', 'http://www.chinadaily.com.cn/rss/video_rss.xml'),
        ('china_daily', 'http://www.chinadaily.com.cn/rss/cndy_rss.xml'),
        ('Hong_Kong', 'http://www.chinadaily.com.cn/rss/hk_rss.xml'),
        ('usa', 'http://usa.chinadaily.com.cn/usa_kindle.xml'),
        ('european', 'http://europe.chinadaily.com.cn/euweekly_rss.xml'),
        ]


def _gen_rss_fetcher(category, url):
    """helper function to generate china daily rss fetcher"""
    def fetcher(ctx):
        """China Daily fetcher of category {}""" . format(category)

        coll = ctx.get_mongo_collection()
        for entry in fetch_rss(url).entries:
            try:
                print(entry.__dict__)
                coll.insert({'_id', entry.id})
            except DuplicateKeyError:
                continue
        ctx.new_item(TextOnlyItem(entry.title, entry.summary), ['china_daily',
            category], {'id': entry.id, 'content': entry.content})
        log_info(u'China Daily rss: new entry: {} {}' . format(entry.id,
            entry.title))

    return fetcher

def fetch_rss(feed_url):
    socket.setdefaulttimeout(15)
    return feedparser.parse(feed_url)

for category, url in rss_list:
    register_china_daily_rss_fetcher(category = category)(_gen_rss_fetcher(category, url))

# vim: foldmethod=marker

