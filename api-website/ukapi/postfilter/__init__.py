#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Sat Dec 14 22:35:00 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""change mongo doc before inserting into db"""

from ukutil import import_all_modules, MongoDBSet
from ukdbconn import get_mongo
from ukitem import ItemDescBase
import uklogger

from abc import ABCMeta, abstractmethod

_user_enabled_filter_set = MongoDBSet('ukapi_enabled_postfilter')


def get_postfilter_list():
    """:return: list of :class:`PostfilterBase` objects"""
    return list(PostfilterBase._postfilter_list.itervalues())


def get_enabled_user_postfilter(user_id):
    return _user_enabled_filter_set.get(user_id)


def enable_user_postfilter(user_id, filter_name, config):
    f = PostfilterBase._postfilter_list[filter_name]
    f.enable(user_id, config)
    _user_enabled_filter_set.add(user_id, filter_name)


def disable_user_postfilter(user_id, filter_name):
    f = PostfilterBase._postfilter_list[filter_name]
    _user_enabled_filter_set.remove(user_id, filter_name)
    f.disable(user_id)


def apply_postfilter(user_id, docs):
    """:param docs: raw document retrived from mongodb from item collection;
    would be changed in default"""

    for i in docs:
        i['desc'] = ItemDescBase.deserialize(i['desc'])

    ctx = PostfilterContext(user_id)

    for i in get_enabled_user_postfilter(user_id):
        PostfilterBase._postfilter_list[i].apply(ctx, docs)

    docs.sort(key=lambda x: x['creation_time'], reverse=True)


class PostfilterContext(object):
    user_id = None
    """current user id"""

    def __init__(self, user_id):
        self.user_id = user_id


class PostfilterBaseMeta(ABCMeta):
    def __new__(cls, name, base, attr):
        obj = super(PostfilterBaseMeta, cls).__new__(cls, name, base, attr)
        if name != 'PostfilterBase':
            PostfilterBase.register(obj)
        return obj


class PostfilterBase(object):
    __metaclass__ = PostfilterBaseMeta

    _postfilter_list = dict()
    """id => filter class"""

    @abstractmethod
    def _get_name(self):
        """globally unique name of this postfilter"""

    @abstractmethod
    def _get_disp_name(self):
        """display name on webpage"""

    @abstractmethod
    def _get_config_type(self):
        """get user configurable fields"""

    @abstractmethod
    def enable(self, user_id, config):
        """enable this filter for a user"""

    @abstractmethod
    def disable(self, user_id):
        """disable this filter for a user"""

    @abstractmethod
    def apply(self, ctx, docs):
        """apply this postfilter
        :param ctx: :class:`PostfilterContext` object
        :param docs: mongo docs, with `desc' field decoded"""

    @classmethod
    def register(cls, subcls):
        obj = subcls()
        name = obj.name
        assert type(name) is str
        assert name not in cls._postfilter_list, \
            'duplicate postfilter: {}'.format(name)
        cls._postfilter_list[name] = obj

    @property
    def name(self):
        """globally unique name of this postfilter"""
        return self._get_name()

    @property
    def disp_name(self):
        """display name on webpage"""
        return self._get_disp_name()

    @property
    def config_type(self):
        """get user configurable fields"""
        return self._get_config_type()

    def _get_mongo_collection(self):
        """:return a mongo collection for this fetcher"""
        return get_mongo('postfilter_' + self.name)

    def _save_config(self, user_id, config):
        """save the config using default method"""
        self._get_mongo_collection().save({'_id': user_id, 'config': config})

    def _del_config(self, user_id):
        """remove config for a user"""
        self._get_mongo_collection().remove({'_id': user_id})

    def _load_config(self, user_id):
        """load the config using default method"""
        rst = list(self._get_mongo_collection().find({'_id': user_id}))
        if rst:
            return rst[0]['config']


import_all_modules(__file__, __name__)
