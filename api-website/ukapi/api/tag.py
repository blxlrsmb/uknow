#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: tag.py
# Date: Thu Dec 12 11:55:54 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import api_method, request
from flask_login import current_user, login_required
from ukdbconn import get_mongo, get_user
from uklogger import log_info

import json


@api_method('/add_tag', methods=['POST'])
@login_required
def add_tag():
    """
    {
     name: 'tagname',
     tab: 'tabname'
    }
    """
    data = json.loads(request.data)
    try:
        tagname = data['name']
        tabname = data['tab']
        assert isinstance(tagname, basestring) \
            and isinstance(tabname, basestring)
    except:
        return {'error': 'illegal format'}
    u = get_user(current_user.username)
    for tab in u['tab']:
        if tabname == tab['name']:
            tab['tags'].append(tagname)
            get_mongo('user').save(u)
            log_info('user {0} add tag {1} to tab \
                     {2}'.format(current_user.username, tagname, tabname))
            return {'tabs': u['tab']}
    return {'error': 'no such tab'}


@api_method('/get_all_tags')
@login_required
def get_all_tags():
    """get all general tags to choose from"""
    tags = list(get_mongo('general_tags').find())
    ret = map(lambda doc: {'name': doc['_id'], 'cnt': doc['cnt']}, tags)
    return {'tags': ret}


@api_method('/del_tag')
@login_required
def del_tag():
    """
    GET /del_tag?name=xxx&tab=xxx
    """
    data = request.args
    try:
        tagname = data['name']
        tabname = data['tab']
        assert isinstance(tagname, basestring) \
            and isinstance(tabname, basestring)
    except:
        return {'error': 'illegal format'}
    u = get_user(current_user.username)
    for tab in u['tab']:
        if tabname == tab['name']:
            try:
                tab['tags'].remove(tagname)
            except ValueError:
                return {'error': 'tag {0} not in tab {1}'.format(tagname,
                                                                 tabname)}
            get_mongo('user').save(u)
            log_info('user {0} del tag {1} in tab \
                     {2}'.format(current_user.username, tagname, tabname))
            return {'tabs': u['tab']}
    return {'error': 'no such tab'}
