#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Sat Nov 16 20:25:25 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""fetcher for user-specific items"""

from ..base import register_fetcher_base
from ..context import FetcherContext, FETCHER_TYPE_USER

from ukutil import import_all_modules
from ukuser import get_enabled_fetcher
import ukconfig
import uklogger

from celery import Celery


class UserFetcherContext(FetcherContext):

    """FetcherContext for user fetchers"""

    fetcher_name = None

    def __init__(self, fetcher_name, user_id):
        self.fetcher_name = fetcher_name
        self.user_id = user_id

    def new_item(self, desc, inital_tag, other=None):
        return self._do_new_item(
            FETCHER_TYPE_USER,
            self.fetcher_name,
            desc, inital_tag, other)


class register_fetcher(register_fetcher_base):

    """register a fetcher for user items"""

    fetcher_map = {}
    """fetcher_name => :class:`register_fetcher` object"""

    user_id = None

    def _on_new_fetcher(self, func):
        self.fetcher_map[self.fetcher_name] = self
        return func

    def _create_fetcher_context(self):
        return UserFetcherContext(
            self.fetcher_name, self.user_id)

    def run(self, user_id):
        """run the fetcher with specified user id"""
        self.user_id = user_id
        return register_fetcher_base.run(self)

_celery_app = None
_celery_task = None


def get_celery_task():
    """get celery task, which takes user id as its sole argument"""
    global _celery_app
    global _celery_task
    if _celery_task:
        return _celery_task
    import_all_modules(__file__, __name__)
    _celery_app = Celery('ukfetcher', broker=ukconfig.celery_broker)
    _celery_app.conf.update(
        CELERY_ACCEPT_CONTENT=['pickle', 'json', 'msgpack', 'yaml'])

    @_celery_app.task
    def on_user_activated(user_id):
        for i in get_enabled_fetcher(user_id):
            fetcher = register_fetcher.fetcher_map.get(i)
            if fetcher is None:
                uklogger.log_err(
                    'fetcher {} not exist, requested by user {}'.format(
                        i, user_id))
            else:
                uklogger.log_info('run fetcher {} for user {}'.format(
                    i, user_id))
                fetcher.run(user_id)

    _celery_task = on_user_activated.delay
    return _celery_task


def get_celery_app():
    """:return: celery app"""
    get_celery_task()
    return _celery_app
