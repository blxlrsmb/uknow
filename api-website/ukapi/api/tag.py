#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: tag.py
# Date: Fri Dec 13 11:01:47 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import api_method, request
from flask_login import current_user, login_required
from ukdbconn import get_mongo, get_user
from uklogger import log_api as log_info
from ukfetcher.general import FETCHER_TYPE_GENERAL
from ukitem import ItemDescBase

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
    try:
        data = json.loads(request.data)
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


@api_method('/set_tag', methods=['POST'])
@login_required
def set_tag():
    """
    {
     name: ['tagname'],
     tab: 'tabname'
    }
    """
    try:
        data = json.loads(request.data)
        tags = data['name']
        tabname = data['tab']
        assert isinstance(tabname, basestring)
        assert isinstance(tags, list)
        for tag in tags:
            assert isinstance(tag, basestring)
    except:
        return {'error': 'illegal format'}
    u = get_user(current_user.username)
    for tab in u['tab']:
        if tabname == tab['name']:
            tab['tags'] = tags
            get_mongo('user').save(u)
            log_info('user {0} set tag to {1} on tab \
                     {2}'.format(current_user.username, tags, tabname))
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
    try:
        data = request.args
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


@api_method('/get_tag_article')
def get_tag_article():
    """get all article under a tag
    GET /get_tag_article?tag=tagname
    """
    try:
        tagname = request.args['tag']
        assert isinstance(tagname, basestring)
    except:
        return {'error': 'illegal format'}
    itemdb = get_mongo('item')
    rst = list(itemdb.find({'tag': tagname,
                            'fetcher_type': FETCHER_TYPE_GENERAL},
                           {'fetcher_name': 0, '_id': 0}))
    for item in rst:
        item['creation_time'] = \
            item['creation_time'].strftime('%Y-%m-%d %H:%M:%S')
        item['desc'] = ItemDescBase.deserialize(item['desc']).render_as_text()
    return {'data': rst}
