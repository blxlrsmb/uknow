#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: thu_learn.py
# $Date: Sat Dec 14 17:34:24 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""sample user fetcher"""

from . import UserFetcherBase

from ukitem import TextOnlyItem
from uklogger import log_fetcher as log_info
from uklogger import log_exc
from ukdbconn import DuplicateKeyError
from lib.thu_learn.fetch import fetch

import time


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
            ctx.new_item(TextOnlyItem(u'网络学堂验证失败', ''), ['THU learn'])
            return

        coll = ctx.get_mongo_collection()
        try:
            entries = fetch(conf['username'], conf['password'])
        except Exception as e:
            ctx.new_item(TextOnlyItem(u'网络学堂抓取失败' + str(e), ''), ['THU learn'])
            log_exc(e)
            return

        for entry in entries:
            try:
                coll.insert({'_id': str(ctx.user_id) + entry['id']})
            except DuplicateKeyError:
                continue
            ctx.new_item(
                TextOnlyItem(entry['title'], entry['content']),
                ['THU learn'], time.strptime(entry['create_time'], '%Y-%m-%d'),
                {'id': entry['id']})
            log_info(u'THU learn: new entry: {} {}'.format(entry['id'],
                                                           entry['title']))
