#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: tab.py
# Date: Thu Dec 12 14:27:10 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import api_method, request
from flask_login import current_user, login_required
from ukdbconn import get_mongo, get_user
from uklogger import log_info

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
        priority = data.get('priority', 0)
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


@api_method('/del_tab')
@login_required
def del_tab():
    """delete a tab
    GET /del_tab?name=tabname
    ignore it when tab with 'tabname' doesn't exist
    """
    data = request.args
    try:
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
