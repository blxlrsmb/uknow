#!/usr/bin/python2
# -*- coding: utf-8 -*-
# $File: china_daily.py
# $Date: Thu Dec 12 15:55:06 2013 +0800
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

    def __init__(self, category, **kwargs):
        """see :meth:`register_fetcher.__init__`for details;
        additional keyword arguments:
            * category: category of this rss fetcher"""

        register_fetcher.__init__(
            self,
            self.CHINA_DAILY_RSS_FETCHER_NAME_PREFIX + category)

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


def _get_id(category, entry):
    for val in ['guid', 'link']:
        try:
            return entry[val]
        except KeyError:
            continue
    raise RuntimeError('can not find id for category {}' . format(category))


def _get_content(category, entry):
    for val in ['content', 'description']:
        try:
            return entry[val]
        except KeyError:
            continue

    raise RuntimeError('can not find content for category {}' . format(
        category))


def _gen_rss_fetcher(category, url):
    """helper function to generate china daily rss fetcher"""
    def fetcher(ctx):
        """China Daily fetcher of category {}""" . format(category)

        coll = ctx.get_mongo_collection()
        for entry in fetch_rss(url).entries:
            try:
                coll.insert({'_id': _get_id(category, entry)})
            except DuplicateKeyError:
                continue
            tags = ['china_daily', category]
            if 'category' in entry:
                tags.append(entry.category.lower())
            ctx.new_item(
                TextOnlyItem(entry.title, entry.summary),
                tags,
                {'id': _get_id(category, entry),
                    'content': _get_content(category, entry)})
            log_info(u'China Daily rss: new entry: {} {}' . format(
                _get_id(category, entry), entry.title))

    return fetcher


def fetch_rss(feed_url):
    socket.setdefaulttimeout(15)
    return feedparser.parse(feed_url)


for category, url in rss_list:
    decorator = register_china_daily_rss_fetcher(category)
    decorator(_gen_rss_fetcher(category, url))

# vim: foldmethod=marker
