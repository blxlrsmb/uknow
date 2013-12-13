#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: tab.py
# Date: Fri Dec 13 16:16:19 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import api_method, request
from flask_login import current_user, login_required
from ukdbconn import get_mongo, get_user
from uklogger import log_api as log_info
from ukfetcher.general import FETCHER_TYPE_GENERAL
from ukfetcher.user import FETCHER_TYPE_USER
from ..util import parse_article

import json


@api_method('/add_tab', methods=['POST'])
@login_required
def add_tab():
    """add a new tab to current user
    {
        name: 'string'      # name of the tab
        priority: integer   # bigger, better. default to be 0
    }
    """
    try:
        data = json.loads(request.data)
        name = data['name']
        priority = int(data.get('priority', 0))
        assert isinstance(name, basestring)
    except:
        return {'error': 'illegal format'}
    username = current_user.username
    doc = get_user(username)
    for tab in doc['tab']:
        if tab['name'] == name:
            return {'error': 'tab with this name already exists!'}
    doc['tab'].append({
        'name': name,
        'priority': priority,
        'tags': []
    })
    get_mongo('user').save(doc)
    log_info('user {0} add tab {1}'.format(username, name))
    return {'success': 1}


@api_method('/get_all_tabs')
@login_required
def get_all_tabs():
    tabs = get_user(current_user.username)['tab']
    return {'tabs': tabs}


@api_method('/del_tab', methods=['POST'])
@login_required
def del_tab():
    """delete a tab
    {
        name: 'tabname'      # name of the tab
    }
    ignore it when tab with 'tabname' doesn't exist
    """
    try:
        data = json.loads(request.data)
        name = data['name']
        assert isinstance(name, basestring)
    except:
        return {'error': 'illegal format'}
    db = get_mongo('user')
    db.update({'username': current_user.username},
              {'$pull': {
                  'tab': {
                      'name': name
                  }}})
    return {'success': 1}


@api_method('/get_tab_article')
@login_required
def get_tab_article():
    """get all article under a tab
    GET /get_tab_article?tab=tabname
    """
    try:
        tabname = request.args['tab']
        assert isinstance(tabname, basestring)
    except:
        return {'error': 'illegal format'}
    db = get_user(current_user.username)
    tab = filter(lambda x: x['name'] == tabname, db['tab'])
    if len(tab) == 0:
        return {'error': 'no such tab'}
    tags = tab[0]['tags']
    itemdb = get_mongo('item')
    rst = list(itemdb.find({'tag': {'$in': tags},
                            '$or': [
                                {'fetcher_type': FETCHER_TYPE_GENERAL},
                                {
                                    'fetcher_type': FETCHER_TYPE_USER,
                                    'other.user_id': current_user.username
                                }
                            ]},
                           {'_id': 0}))
    rst = parse_article(rst)
    return {'data': rst}
