#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: context.py
# $Date: Fri Dec 13 15:28:44 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""mongo model and fetcher execution context
mongo document: {
    _id: unique int64 id
    fetcher_type: int, indexed
    fetcher_name: str, indexed
    desc: binary
    tag: list of str, indexed
    other: anything
    creation_time: datetime, UTC, indexed
}"""

from .prefilter import prefilter

from ukitem import ItemDescBase
from ukdbconn import get_mongo, global_counter, Binary, declare_tag


from abc import ABCMeta, abstractmethod
from copy import deepcopy
import time
from datetime import datetime

FETCHER_TYPE_GENERAL = 0
FETCHER_TYPE_USER = 1


class FetcherContext(object):
    """context where a fetcher is executed"""

    __metaclass__ = ABCMeta

    user_id = None
    """user id as integer, or None if unavailable"""

    fetcher_type = None
    """current fetcher type, in (FETCHER_TYPE_GENERAL, FETCHER_TYPE_USER)"""

    fetcher_name = None
    """current fetcher name, str"""

    def __init__(self, fetcher_type, fetcher_name):
        """constructor, only called by subclasses"""
        assert type(self) is not FetcherContext
        assert fetcher_type in (FETCHER_TYPE_USER, FETCHER_TYPE_GENERAL), \
            'bad fetcher_type: {}'.format(fetcher_type)
        assert isinstance(fetcher_name, basestring), \
            'bad fetcher_name: {!r}'.format(fetcher_name)
        self.fetcher_type = fetcher_type
        self.fetcher_name = fetcher_name

    def _do_new_item(self, desc, initial_tag, create_time=None, other=None):
        """helper function for implementing :meth:`new_item`"""
        assert isinstance(desc, ItemDescBase), \
            'bad desc: {!r}'.format(type(desc))
        assert isinstance(initial_tag, list) and \
            all([isinstance(i, basestring) for i in initial_tag]), \
            'bad initial_tag: {!r}'.format(initial_tag)

        declare_tag(initial_tag)
        if create_time is None:
            create_time = time.localtime()
        db = get_mongo('item')
        item_id = global_counter('item')
        db.ensure_index('fetcher_type')
        db.ensure_index('fetcher_name')
        db.ensure_index('tag')
        db.ensure_index('creation_time')
        doc = {
            '_id': item_id,
            'fetcher_type': self.fetcher_type,
            'fetcher_name': self.fetcher_name,
            'desc': deepcopy(desc),
            'tag': initial_tag,
            'other': other,
            'creation_time': datetime.fromtimestamp(time.mktime(create_time))}
        prefilter.apply(self, doc)
        doc['desc'] = Binary(doc['desc'].serialize())
        db.insert(doc)

        return item_id

    @abstractmethod
    def new_item(self, desc, inital_tag, create_time=None, other=None):
        """add an item into database
        :param fetcher_type: one of FETCHER_TYPE_USER or FETCHER_TYPE_GENERAL
        :param fetcher_name: str, name of fetcher
        :param desc: :class:`ItemDescBase` object
        :param initial_tag: list of str, initial tags
        :param other: any bson-serializable object
        :param other: :class: `time.struct_time` object
        :return: int, item id"""

    def get_mongo_collection(self):
        """create a mongo collection to store fetcher-specific data"""
        return self.get_mongo_collection_for_fetcher_name(self.fetcher_name)

    @classmethod
    def get_mongo_collection_for_fetcher_name(cls, fetcher_name):
        """create a mongo collection to store fetcher-specific data"""
        return get_mongo('fetcher_' + fetcher_name)
