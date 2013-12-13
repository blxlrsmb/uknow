#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: thu_learn.py
# $Date: Sat Dec 14 01:44:34 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""sample user fetcher"""

from . import UserFetcherBase

from ukitem import TextOnlyItem
from uklogger import log_fetcher as log_info
from ukdbconn import DuplicateKeyError, get_mongo
from lib.thu_learn.fetch import fetch


class ThuLearFetcher(UserFetcherBase):
    @staticmethod
    def get_name():
        return "THU learn"

    @classmethod
    def enable(cls, user_id, config):
        config = {'username': config['username'],
                  'password': config['password']}
        cls.save_config(user_id, config)

    @classmethod
    def disable(cls, user_id):
        cls.del_config(user_id)

    @classmethod
    def run(cls, ctx):
        conf = cls.load_config(ctx.user_id)
        if not conf:
            return

        coll = get_mongo('fetcher_thu_learn_items_id')
        entries = fetch(conf['username'], conf['password'])
        for entry in entries:
            try:
                coll.insert({'_id': str(ctx.user_id) + entry['id']})
            except DuplicateKeyError:
                continue
            ctx.new_item(
                TextOnlyItem(u"{}--{}".format(entry['title'],
                                              entry['summary']),
                             entry['content']),
                ['THU learn'], None, entry['id'])
            log_info(u'thu learn: new entry: {} {}'.format(entry['id'],
                                                           entry['title']))
