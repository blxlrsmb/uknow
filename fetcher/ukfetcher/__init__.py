#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Fri Dec 13 01:54:53 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""provide fetcher background service, and also utilities for managing
fetchers

mongo doc: collection: ukfetcher_user_config
{
    _id: user_id
    fetcher: list of fetchers
    prefilter: list of prefilters
}
"""

from .user import get_celery_task as get_user_fetcher_celery_task
from .user import register_fetcher as _user_register_fetcher
from .user import load_all_fetcher as _load_all_fetcher
from .util import get_db_set


def get_user_fetcher_list():
    """return a list of :class:`_user_register_fetcher` objects"""
    _load_all_fetcher()
    rst = list(_user_register_fetcher.fetcher_map.itervalues())
    return rst


def get_enabled_user_fetcher(user_id):
    return get_db_set(user_id, 'fetcher')


def enable_user_fetcher(user_id, fetcher_name, config):
    _load_all_fetcher()
    _user_register_fetcher.fetcher_map[fetcher_name].enable(user_id, config)


def disable_user_fetcher(user_id, fetcher_name):
    _load_all_fetcher()
    _user_register_fetcher.fetcher_map[fetcher_name].disable(user_id)


# TODO: limit user connection; coroutine for different users
