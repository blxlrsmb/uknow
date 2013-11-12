#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: context.py
# $Date: Wed Nov 13 00:35:51 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""mongo model and fetcher execution context
mogo document: {
    _id: unique int64 id
    fetcher_type: int, indexed
    fetcher_name: str, indexed
    desc: text
    tag: list of str, indexed
    other: anything
    creation_time: datetime, UTC, indexed
}"""

from .prefilter import prefilter

from ukdbconn import get_mongo, global_counter

from abc import ABCMeta, abstractmethod
from datetime import datetime

FETCHER_TYPE_GENERAL = 0
FETCHER_TYPE_USER = 1

class FetcherContext(object):
    """context where a fetcher is executed"""

    __metaclass__ = ABCMeta

    user_id = None
    """user id as integer, or None if unavailable"""

    def _do_new_item(self,
            fetcher_type, fetcher_name, desc, inital_tag, other):
        """helper function for implementing :meth:`new_item`"""
        assert fetcher_type in (FETCHER_TYPE_USER, FETCHER_TYPE_GENERAL), \
                'bad fetcher_type: {}'.format(fetcher_type)
        assert isinstance(fetcher_name, basestring), \
                'bad fetcher_name: {!r}'.format(fetcher_name)
        assert isinstance(desc, basestring), \
                'bad desc: {!r}'.format(desc)
        assert isinstance(inital_tag, list) and \
                all([isinstance(i, basestring) for i in inital_tag]), \
                'bad inital_tag: {!r}'.format(inital_tag)


        db = get_mongo('item')
        item_id = global_counter('item')
        db.ensure_index('fetcher_type')
        db.ensure_index('fetcher_name')
        db.ensure_index('tag')
        db.ensure_index('creation_time')
        doc = {
                '_id': item_id,
                'fetcher_type': fetcher_type,
                'fetcher_name': fetcher_name,
                'desc': desc,
                'tag': inital_tag,
                'other': other,
                'creation_time': datetime.utcnow()}
        prefilter.apply(self, doc)
        db.insert(doc)

        return item_id

    @abstractmethod
    def new_item(self, desc, inital_tag, other = None):
        """add an item into database
        :param fetcher_type: one of FETCHER_TYPE_USER or FETCHER_TYPE_GENERAL
        :param fetcher_name: str, name of fetcher
        :param desc: str, human-readable description
        :param initial_tag: list of str, initial tags
        :param other: any bson-serializable object
        :return: int, item id"""

