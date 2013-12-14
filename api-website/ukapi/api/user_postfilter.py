#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: user_postfilter.py
# Date: Sat Dec 14 16:17:59 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import api_method

from ..util import get_current_user_id, login_required

from flask import request


@api_method('/filter/list')
@login_required
def get_filter_list():
    """:return: {
        "filter": [
            {"id": "",
             "enabled": bool,
             "name": "",    // display name on webpage
             "config": ""}  // config type, currently ignored
        ]
    }"""
    return {'filter': [{'id': '1', 'enabled': False, 'name': 'haha', 'config':
                       ['Filter Text']}]}
    #enabled = set(get_enabled_user_filter(get_current_user_id()))
    #return {'filter': [{'id': i.filter_name,
                         #'enabled': i.filter_name in enabled,
                         #'name': i.filter_name,
                         #'config': ''}
                        #for i in get_user_filter_list()]}


@api_method('/filter/enable')
@login_required
def enable_filter():
    """arg: filter_id, filter-specific config
    currently, config only includes username and password, for
    authentication to the underlying website"""
    #enable_user_filter(
        #get_current_user_id(), request.values['filter_id'],
        #request.values)
    print request.values
    return {'success': 1}


@api_method('/filter/disable')
@login_required
def disable_filter():
    """arg: filter_id"""
    #disable_user_filter(
        #get_current_user_id(), request.values['filter_id'])
    return {'success': 1}
