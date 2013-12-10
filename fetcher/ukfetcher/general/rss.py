#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By i@BlahGeek.com

"""Simple RSS fetcher"""

from . import register_fetcher
import feedparser
import socket


def fetch_rss(feed_url):
    socket.setdefaulttimeout(15)
    feed = feedparser.parse(feed_url)

    return map(lambda x: x.title, feed.entries)


@register_fetcher('guokr_rss', sleep_time=50)
def guokr_rss_fetcher(ctx):
    """fetcher guokr.com/rss/, save each title with tag `guokr`"""
    URL = 'http://www.guokr.com/rss/'
    for title in fetch_rss(URL):
        ctx.new_item(title, ['guokr'])
