#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By i@BlahGeek.com

"""Simple RSS fetcher"""

from . import register_fetcher
from ukitem import TextOnlyItem
from ukdbconn import DuplicateKeyError
from uklogger import log_fetcher as log_info

import feedparser
import socket


def fetch_rss(feed_url):
    socket.setdefaulttimeout(15)
    return feedparser.parse(feed_url)


@register_fetcher('guokr_rss', sleep_time=1800)
def guokr_rss_fetcher(ctx):
    """fetcher guokr.com/rss/, save each title with tag `guokr`"""
    URL = 'http://www.guokr.com/rss/'
    coll = ctx.get_mongo_collection()

    for entry in fetch_rss(URL).entries:
        try:
            coll.insert({'_id': entry.id})
        except DuplicateKeyError:
            continue
        try:
            content = entry.content[0].value
        except:
            content = entry.summary
        ctx.new_item(TextOnlyItem(entry.title, content), ['guokr'],
                     {'id': entry.id})
        log_info(u'guokr: new entry: {} {}'.format(entry.id, entry.title))
