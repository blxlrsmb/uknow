#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Sat Dec 14 20:07:30 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""provide fetcher background service, and also utilities for managing
fetchers

public mongo doc: collection: item
{
    _id: unique int64 id
    fetcher_type: int, indexed
    fetcher_name: str, indexed
    desc: binary of ItemDescBase
    tag: list of str, indexed
    other: null, or dict of anything
    creation_time: datetime, UTC, indexed
}
"""

from .user import get_celery_task as get_user_fetcher_celery_task
from .user import register_fetcher as _user_register_fetcher
from .user import load_all_fetcher as _load_all_fetcher
from .util import get_db_set

from .context import FETCHER_TYPE_USER, FETCHER_TYPE_GENERAL


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
