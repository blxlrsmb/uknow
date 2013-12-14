#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: user_fetcher.py
# $Date: Fri Dec 13 02:06:36 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from . import api_method

from ..util import get_current_user_id, login_required

from ukfetcher import (
    get_enabled_user_fetcher,
    get_user_fetcher_list, enable_user_fetcher, disable_user_fetcher)

from flask import request


@api_method('/fetcher/list')
@login_required
def get_fetcher_list():
    """:return: {
        "fetcher": [
            {"id": "",
             "enabled": bool,
             "name": "",    // display name on webpage
             "config": ""}  // config type, currently ignored
        ]
    }"""
    enabled = set(get_enabled_user_fetcher(get_current_user_id()))
    return {'fetcher': [{'id': i.fetcher_name,
                         'enabled': i.fetcher_name in enabled,
                         'name': i.fetcher_name,
                         'config': ''}
                        for i in get_user_fetcher_list()]}


@api_method('/fetcher/enable')
@login_required
def enable_fetcher():
    """arg: fetcher_id, fetcher-specific config
    currently, config only includes username and password, for
    authentication to the underlying website"""
    enable_user_fetcher(
        get_current_user_id(), request.values['fetcher_id'],
        request.values)
    return {'success': 1}


@api_method('/fetcher/disable')
@login_required
def disable_fetcher():
    """arg: fetcher_id"""
    disable_user_fetcher(
        get_current_user_id(), request.values['fetcher_id'])
    return {'success': 1}
