#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Sat Dec 14 16:26:18 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""fetcher for user-specific items"""

from ..base import register_fetcher_base
from ..context import FetcherContext, FETCHER_TYPE_USER
from ..util import insert_db_item, remove_db_item, get_db_set

from ukutil import import_all_modules
import ukconfig
import uklogger

from celery import Celery

from abc import ABCMeta, abstractmethod


class UserFetcherContext(FetcherContext):
    """FetcherContext for user fetchers"""

    def __init__(self, fetcher_name, user_id):
        super(UserFetcherContext, self).__init__(
            FETCHER_TYPE_USER, fetcher_name)
        self.user_id = user_id

    def new_item(self, desc, inital_tag, create_time=None, other=None):
        try:
            other['user_id'] = self.user_id
        except:
            other = {'user_id': self.user_id}
        return self._do_new_item(desc, inital_tag, create_time, other)


class register_fetcher(register_fetcher_base):
    """register a fetcher for user items"""

    fetcher_map = {}
    """fetcher_name => :class:`register_fetcher` object"""

    user_id = None

    _impl = None
    """implementation class"""

    def __init__(self, name, param, impl):
        super(register_fetcher, self).__init__(name, param)
        self._impl = impl
        self(impl.run)

    def _on_new_fetcher(self, func):
        self.fetcher_map[self.fetcher_name] = self
        return func

    def _create_fetcher_context(self):
        return UserFetcherContext(
            self.fetcher_name, self.user_id)

    def run(self, user_id):
        """run this fetcher with specified user id"""
        self.user_id = user_id
        return super(register_fetcher, self).run()

    def enable(self, user_id, config):
        """enable this fetcher for a user"""
        self._impl.enable(user_id, config)
        insert_db_item(user_id, 'fetcher', self.fetcher_name)

    def disable(self, user_id):
        """disable this fetcher for a user"""
        self._impl.disable(user_id)
        remove_db_item(user_id, 'fetcher', self.fetcher_name)


class UserFetcherBaseMeta(ABCMeta):
    def __new__(cls, name, base, attr):
        obj = super(UserFetcherBaseMeta, cls).__new__(cls, name, base, attr)
        if name != 'UserFetcherBase':
            register_fetcher(obj.get_name(), obj.get_config_param(), obj)
        return obj


class UserFetcherBase(object):
    __metaclass__ = UserFetcherBaseMeta

    @abstractmethod
    def get_name():
        """static constant method, return name of this fetcher"""

    @abstractmethod
    def enable(user_id, config):
        """static method, enable this fetcher for a user"""

    @abstractmethod
    def disable(user_id):
        """static method, disable this fetcher for a user"""

    @abstractmethod
    def run(ctx):
        """static method, run this fetcher; see
        :meth:`register_fetcher_base.__call__`"""

    @classmethod
    def get_mongo_collection(cls):
        """:return a mongo collection for this fetcher"""
        return UserFetcherContext.get_mongo_collection_for_fetcher_name(
            cls.get_name())

    @classmethod
    def save_config(cls, user_id, config):
        """save the config using default method"""
        cls.get_mongo_collection().save({'_id': user_id, 'config': config})

    @classmethod
    def del_config(cls, user_id):
        """save the config using default method"""
        cls.get_mongo_collection().remove({'_id': user_id})

    @classmethod
    def load_config(cls, user_id):
        """load the config using default method"""
        rst = list(cls.get_mongo_collection().find({'_id': user_id}))
        if rst:
            return rst[0]['config']


def load_all_fetcher():
    if not getattr(load_all_fetcher, 'done', False):
        import_all_modules(__file__, __name__)
        load_all_fetcher.done = True


_celery_app = None
_celery_task = None


def get_celery_task():
    """get celery task, which takes user id as its sole argument"""
    global _celery_app
    global _celery_task
    if _celery_task:
        return _celery_task
    load_all_fetcher()
    _celery_app = Celery('ukfetcher', broker=ukconfig.celery_broker)
    _celery_app.conf.update(
        CELERY_ACCEPT_CONTENT=['pickle', 'json', 'msgpack', 'yaml'])

    @_celery_app.task
    def on_user_activated(user_id):
        try:
            user_fetcher = get_db_set(user_id, 'fetcher')
            for i in user_fetcher:
                fetcher = register_fetcher.fetcher_map.get(i)
                if fetcher is None:
                    uklogger.log_err(
                        'fetcher {} not exist, requested by user {}'.format(
                            i, user_id))
                else:
                    uklogger.log_info('run fetcher {} for user {}'.format(
                        i, user_id))
                    fetcher.run(user_id)
        except Exception as ex:
            uklogger.log_exc(ex)

    _celery_task = on_user_activated.delay
    return _celery_task


def get_celery_app():
    """:return: celery app"""
    get_celery_task()
    return _celery_app
