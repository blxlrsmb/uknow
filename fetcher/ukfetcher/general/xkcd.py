#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By i@vuryleo.com

"""Simple RSS fetcher"""

from . import register_fetcher, parse_entry_time
from ukitem import TextOnlyItem
from ukdbconn import DuplicateKeyError
from uklogger import log_fetcher as log_info

import feedparser
import socket


def fetch_rss(feed_url):
    socket.setdefaulttimeout(15)
    return feedparser.parse(feed_url)


@register_fetcher('xkcd', sleep_time=1800)
def xkcd_rss_fetcher(ctx):
    """fetcher xkcd.com/rss.xml, save each title with tag `xkcd`"""
    URL = 'http://www.xkcd.com/rss.xml'
    coll = ctx.get_mongo_collection()

    for entry in fetch_rss(URL).entries:
        try:
            coll.insert({'_id': entry.id})
        except DuplicateKeyError:
            continue
        ctx.new_item(TextOnlyItem(entry.title, entry.description),
                     ['xkcd'], parse_entry_time(entry),
                     {'id': entry.id})
        log_info(u'xkcd rss: new entry: {} {}'.format(entry.id,
                                                      entry.title))
