#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By i@vuryleo.com

"""Simple RSS fetcher"""

from . import register_fetcher
from ukitem import TextOnlyItem
from ukdbconn import DuplicateKeyError
from uklogger import log_fetcher as log_info
from ..util import parse_entry_time

import feedparser
import socket


def fetch_rss(feed_url):
    socket.setdefaulttimeout(15)
    return feedparser.parse(feed_url)


@register_fetcher('zhihu', sleep_time=1800)
def zhihu_rss_fetcher(ctx):
    """fetcher zhihu.com/rss/, save each title with tag `zhihu`"""
    URL = 'http://www.zhihu.com/rss'
    coll = ctx.get_mongo_collection()

    for entry in fetch_rss(URL).entries:
        try:
            coll.insert({'_id': entry.link})
        except DuplicateKeyError:
            continue
        ctx.new_item(TextOnlyItem(entry.title, entry.description), ['zhihu'],
                     parse_entry_time(entry),
                     {'id': entry.link})
        log_info(u'zhihu: new entry: {} {}'.format(entry.link,
                                                   entry.title))
