#!/usr/bin/python2
# -*- coding: utf-8 -*-
# $File: china_daily.py
# $Date: Thu Dec 12 21:27:38 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

"""China Daily fetcher. As china daily rss has been categorized automatically,
    the corpora can be used to train text classifier"""

from . import register_fetcher
from functools import wraps
import feedparser
import socket
from ukitem import TextOnlyItem
from ukdbconn import DuplicateKeyError
from uklogger import log_fetcher as log_info


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
    ('china_c', u'中国在线', 'http://www.chinadaily.com.cn/rss_c/zgzx.xml'),
    ('picture_c', u'图片', 'http://www.chinadaily.com.cn/rss_c/tupian.xml'),
    ('international_c', u'中文国际',
        'http://www.chinadaily.com.cn/rss_c/zwgj.xml'),
    ('entertainment_c', u'娱乐',
        'http://lifestyle.chinadaily.com.cn/rss/ent.xml'),
    ('fashion_c', u'时尚', 'http://lifestyle.chinadaily.com.cn/rss/fashion.xml'),
    ('health_c', u'健康', 'http://lifestyle.chinadaily.com.cn/rss/health.xml'),
    ('discovery_c', u'博览', 'http://www.chinadaily.com.cn/rss_c/bolan.xml'),
    ('travel_c', u'旅游', 'http://lifestyle.chinadaily.com.cn/rss/travel.xml'),
    ('finance_c', u'财经', 'http://www.chinadaily.com.cn/rss_c/caijing.xml'),
    ('migration_c', u'移民', 'http://lifestyle.chinadaily.com.cn/rss/yimin.xml'),
    ('internet_c', u'科技互联网', 'http://www.chinadaily.com.cn/rss_c/kjhlw.xml'),
    ('car_c', u'汽车', 'http://lifestyle.chinadaily.com.cn/rss/auto.xml'),
    ('sports_c', u'体育', 'http://www.chinadaily.com.cn/rss_c/tiyu.xml'),
    ('luxury_c', u'奢侈品', 'http://lifestyle.chinadaily.com.cn/rss/luxury.xml'),
    ]


def _get_id(category, entry):
    for val in ['guid', 'link']:
        try:
            return entry[val]
        except KeyError:
            continue
    raise RuntimeError('can not find id for category {}' . format(category))


def _get_content(category, entry):
    for val in ['content', 'text', 'description']:
        try:
            return entry[val]
        except KeyError:
            continue

    raise RuntimeError('can not find content for category {}' . format(
        category))


def fetch_rss(feed_url):
    socket.setdefaulttimeout(15)
    return feedparser.parse(feed_url)


@register_fetcher('chinadaily_rss', sleep_time=1800)
def chinadaily_rss_fetcher(ctx):
    """china daily rss fetcher"""
    for item in rss_list:
        if len(item) == 2:
            category, url = item
            suffix = category
        else:
            suffix, category, url = item

        coll = ctx.get_mongo_collection()
        for entry in fetch_rss(url).entries:
            try:
                coll.insert({'_id': _get_id(category, entry)})
            except DuplicateKeyError:
                continue
            tags = ['china daily', category]
            if 'category' in entry:
                tags.append(entry.category.lower())
            ctx.new_item(
                TextOnlyItem(entry.title, entry.summary),
                tags,
                {'id': _get_id(category, entry),
                 'content': _get_content(category, entry)})
            log_info(u'China Daily rss: new entry: {} {}' . format(
                _get_id(category, entry), entry.title))
