#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: thu_learn.py
# $Date: Fri Dec 13 11:02:51 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""sample user fetcher"""

from . import UserFetcherBase

from ukitem import TextOnlyItem
from uklogger import log_fetcher as log_info


class ThuLearFetcher(UserFetcherBase):
    @staticmethod
    def get_name():
        return "thu learn"

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

        # TODO: fetch thu-learn using username and passwd
        log_info('hahah: {} {}'.format(ctx.user_id, conf))
        ctx.new_item(
            TextOnlyItem(
                'thulearn', 'user:{}; username:{}; passwd:{}'.format(
                    ctx.user_id, conf['username'], conf['password'])),
            ['thu learn'])
