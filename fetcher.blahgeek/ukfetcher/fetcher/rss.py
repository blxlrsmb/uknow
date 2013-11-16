#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# By i@BlahGeek.com at 10/11/2013

remove_attributes = ('class', 'id', 'title', 'style', 'width', 'height',
                     'onclick')
remove_tags = ('script', 'object', 'video', 'embed', 'iframe', 'noscript',
               'style', 'img')

import feedparser
import logging
import socket
import time
from datetime import datetime, timedelta, date
from BeautifulSoup import BeautifulSoup


def fetch_rss(feeds_urls):
    socket.setdefaulttimeout(15)
    logging.info('Starting...')
    feeds = [feedparser.parse(x) for x in feeds_urls]
    feeds = [x for x in feeds if 'title' in x.feed]

    for feed in feeds:
        logging.info('Handling ' + feed.feed.title)
        for entry in feed.entries:
            entry.setdefault('author', 'Anonymous')
            entry.setdefault('date_parsed', entry.get('published_parsed', None))

        feed.entries = filter(lambda x: x.date_parsed is not None, feed.entries)

        for entry_number, entry in enumerate(feed.entries):
            entry.description = BeautifulSoup(entry.description).text[:200].strip()
            try: entry.content = entry.content[0].value;
            except: entry.content = entry.summary;
            content = BeautifulSoup(entry.content)
            for attr in remove_attributes:
                for x in content.findAll(attrs={attr:True}):
                    del x[attr]
            for x in content.findAll(remove_tags):
                x.extract()
            #entry.content = content.decode('utf8')
        logging.info('Entries count: ' + str(len(feed.entries)))

    feeds = [x for x in feeds if len(x.entries) > 0]

    for feed_number, feed in enumerate(feeds):
        feed.update({ 'number': feed_number + 1,
                      'title': feed.feed.title })
    return feeds

if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    print fetch_rss(['http://www.guokr.com/rss/', ])


