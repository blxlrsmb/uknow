#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Wed Nov 13 01:29:02 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""change mongo doc before inserting into db"""

from ukutil import import_all_modules
from ukuser import get_enabled_prefilter
import uklogger

class AbortItemProcessing(Exception):
    """dummy exception to abort processing of current item, causing it to be
    discarded"""

class prefilter(object):
    """decorator to register a new prefilter"""


    prefilter_list = []
    """list of system-wide prefilters, :class:`prefilter` objects"""

    user_customizable_map = {}
    """filter_name => :class:`prefilter` objects
    user could enable/disable filters in this list"""

    priority = None
    func = None
    name = None

    def __init__(self, name, priority = 0, is_user = False):
        """:param priority: int, the smaller value, the earlier executed
        :param is_user: whether could be customized by user; if true, priority
            would be ignored and they would be executed in the order specified by
            the user"""
        self.name = name
        self.priority = priority
        if is_user:
            self.user_customizable_map[name] = self
        else:
            self.prefilter_list.append(self)
            self.prefilter_list.sort(key = lambda x: x.priority)

    def __call__(self, func):
        """:param func: user callable, which takes a :class:`FetcherContext`
        object and a mongo doc as its two arguments; see
        :module:`uknow.context` for details on mongo doc"""
        self.func = func
        return func

    @classmethod
    def apply(cls, ctx, doc):
        """apply all prefilters; invoked by :meth:`FetcherContext.new_item`
        note that user-defined prefilters would be first invoked, and then
        system-wide ones"""
        if ctx.user_id is not None:
            for i in get_enabled_prefilter(ctx.user_id):
                flt = cls.user_customizable_map.get(i)
                if flt is None:
                    uklogger.log_err(
                    'prefilter {} not exist, requested by user {}'.format(
                        i, ctx.user_id))
                else:
                    flt.func(ctx, doc)

        for i in cls.prefilter_list:
            i.func(ctx, doc)


import_all_modules(__file__, __name__)

