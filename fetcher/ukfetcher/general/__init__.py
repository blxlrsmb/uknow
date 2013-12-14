#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Sat Dec 14 17:55:00 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""fetcher for general items"""

from ukutil import import_all_modules
import ukconfig
import uklogger

from ..base import register_fetcher_base
from ..context import FetcherContext, FETCHER_TYPE_GENERAL
import gevent


class GeneralFetcherContext(FetcherContext):
    """FetcherContext for general fetchers"""

    def __init__(self, fetcher_name):
        super(GeneralFetcherContext, self).__init__(
            FETCHER_TYPE_GENERAL, fetcher_name)

    def new_item(self, desc, inital_tags, create_time=None, other=None):
        return self._do_new_item(desc, inital_tags, create_time, other)


class register_fetcher(register_fetcher_base):
    """register a fetcher for general items"""

    sleep_time = None

    fetcher_list = []
    """list of :class:`register_fetcher` objects"""

    def __init__(self, *args, **kwargs):
        """see :meth:`register_fetcher_base.__init__` for details;
        additional keyword argument:
            * sleep_time: default sleep time for this fetcher"""

        self.sleep_time = \
            kwargs.pop('sleep_time',
                       ukconfig.general_fetcher_sleep_interval_default)

        register_fetcher_base.__init__(self, *args, **kwargs)

        ust = ukconfig.general_fetcher_sleep_interval_special.get(
            self.fetcher_name, None)
        if ust is not None:
            self.sleep_time = ust

        assert self.sleep_time > 0, 'invalid sleep time: {}'.format(
            self.sleep_time)

    def _on_new_fetcher(self, func):
        self.fetcher_list.append(self)
        return func

    def _create_fetcher_context(self):
        return GeneralFetcherContext(self.fetcher_name)


def start_server():
    """start the server for all general fetchers"""
    import_all_modules(__file__, __name__)

    if not register_fetcher.fetcher_list:
        uklogger.log_err('no general fetcher available, exit')
        return

    def worker(fetcher):
        try:
            while True:
                uklogger.log_info('run fetcher {}'.format(
                    fetcher.fetcher_name))
                fetcher.run()
                gevent.sleep(fetcher.sleep_time)
        except KeyboardInterrupt:
            uklogger.log_info('worker {} got KeyboardInterrupt, exit'.format(
                fetcher.fetcher_name))

    jobs = [gevent.spawn(worker, i) for i in register_fetcher.fetcher_list]
    try:
        for i in jobs:
            i.join()
    except KeyboardInterrupt:
        uklogger.log_info('got KeyboardInterrupt, exit')


def parse_entry_time(entry=None):
    """return 9-tuple time for a given entry"""
    for i in ['published_parsed', 'created_parsed', 'updated_parsed']:
        t = getattr(entry, i, None)
        if t:
            return t
    return time.localtime()
