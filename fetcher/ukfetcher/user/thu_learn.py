#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: thu_learn.py
# $Date: Sat Dec 14 16:23:55 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""sample user fetcher"""

from . import UserFetcherBase

from ukitem import TextOnlyItem
from uklogger import log_fetcher as log_info
from ukdbconn import DuplicateKeyError
from lib.thu_learn.fetch import fetch


class ThuLearFetcher(UserFetcherBase):
    @staticmethod
    def get_name():
        return "THU learn"

    @staticmethod
    def get_config_param():
        return ['username', 'password']

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
        print 'running'

        coll = ctx.get_mongo_collection()
        entries = fetch(conf['username'], conf['password'])
        for entry in entries:
            try:
                coll.insert({'_id': str(ctx.user_id) + entry['id']})
            except DuplicateKeyError:
                continue
            ctx.new_item(
                TextOnlyItem(entry['title'], entry['content']),
                ['THU learn'], None, {'id': entry['id']})
            log_info(u'thu learn: new entry: {} {}'.format(entry['id'],
                                                           entry['title']))
