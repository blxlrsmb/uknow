#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By i@BlahGeek.com

"""Simple RSS fetcher"""

from . import register_fetcher
from ukitem import TextOnlyItem
from ukdbconn import DuplicateKeyError
from uklogger import log_info

import feedparser
import socket

def fetch_rss(feed_url):
    socket.setdefaulttimeout(15)
    return feedparser.parse(feed_url)


@register_fetcher('guokr_rss', sleep_time=50)
def guokr_rss_fetcher(ctx):
    """fetcher guokr.com/rss/, save each title with tag `guokr`"""
    URL = 'http://www.guokr.com/rss/'
    coll = ctx.get_mongo_collection()

    for entry in fetch_rss(URL).entries:
        try:
            coll.insert({'_id': entry.id})
        except DuplicateKeyError:
            continue
        ctx.new_item(TextOnlyItem(entry.title, entry.summary), ['guokr'],
                     {'id': entry.id, 'content': entry.content})
        log_info(u'guokr rss: new entry: {} {}'.format(entry.id, entry.title))

