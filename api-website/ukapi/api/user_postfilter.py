#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# $File: user_postfilter.py
# $Date: Sat Dec 14 22:36:42 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""note that currently user-specified prefilter is not implemented, thus only
URL /filter is actually for postfilters only"""

from . import api_method

from ..util import get_current_user_id, login_required
from ..postfilter import (
    get_postfilter_list, get_enabled_user_postfilter,
    enable_user_postfilter, disable_user_postfilter)

from flask import request

import json


@api_method('/filter/list')
@login_required
def api_get_postfilter_list():
    """:return: {
        "filter": [
            {"id": "",
             "enabled": bool,
             "name": "",    // display name on webpage
             "config": ""}  // config type, currently ignored
        ]
    }"""
    enabled = set(get_enabled_user_postfilter(get_current_user_id()))
    return {'filter': [{'id': i.name,
                        'enabled': i.name in enabled,
                        'name': i.disp_name,
                        'config': i.config_type}
                       for i in get_postfilter_list()]}


@api_method('/filter/enable')
@login_required
def api_enable_postfilter():
    """arg: filter_id, postfilter-specific config"""
    enable_user_postfilter(
        get_current_user_id(), request.values['filter_id'],
        request.values)
    return {'success': 1}


@api_method('/filter/disable')
@login_required
def api_disable_postfilter():
    """arg: filter_id"""
    disable_user_postfilter(
        get_current_user_id(), request.values['filter_id'])
    return {'success': 1}
