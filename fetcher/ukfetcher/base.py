#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: base.py
# $Date: Thu Dec 12 16:22:21 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from .prefilter import AbortItemProcessing
from .context import FetcherContext

import ukconfig
import uklogger

from abc import ABCMeta, abstractmethod
from functools import wraps


class register_fetcher_base(object):
    """base class for decorator to register a new fetcher"""

    __metaclass__ = ABCMeta

    fetcher_name = None

    _on_register_done = None
    _callback = None
    _fetcher_name_registered = set()

    @abstractmethod
    def _on_new_fetcher(self, func):
        """child method to be called when a new fetcher is registered
        :param func: the original user callback function
        :return: transformed func"""

    @abstractmethod
    def _create_fetcher_context(self):
        """:return: a :class:`FetcherContext` object"""

    def __init__(self, name, on_register_done=None):
        """:param name: name of the fetcher, which must be globally unique
        :param on_register_done: callable to be invoked when this fetcher has
            been registerd"""
        assert name not in self._fetcher_name_registered, \
            'multiple fetchers with same name: {}'.format(name)
        self.fetcher_name = name
        self._fetcher_name_registered.add(name)
        self._on_register_done = on_register_done

    def __call__(self, func):
        """:param func: callable to be invoked when this fetcher is requested;
            taking an object of :class:`context.FetcherContext` as its sole
            argument"""

        func = self._on_new_fetcher(func)
        assert func, 'register_fetcher_base subclass did not return callable'

        @wraps(func)
        def wrapper():
            ctx = self._create_fetcher_context()
            assert isinstance(ctx, FetcherContext)
            try:
                return func(ctx)
            except AbortItemProcessing:
                pass
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                uklogger.log_exc(exc)

        self._callback = wrapper
        return wrapper

    def run(self):
        """run the fetcher"""
        self._callback()
