#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: user.py
# Date: Tue Dec 10 09:45:55 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

"""user operation api"""
from . import api_method, request
from ukdbconn import get_mongo, global_counter

import json

@api_method('/register', methods=['POST'])
def register():
    """user registration.
        username: string
        password: string        XXX TODO

    """
    postdata = json.loads(request.data)
    assert 'username' in postdata,\
            'no username in register()'
    assert 'password' in postdata,\
            'no password in register()'
    username = postdata['username']
    password = postdata['password']
    assert isinstance(username, basestring), \
            'uesrname must be string'
    assert isinstance(password, basestring), \
            'password must be string'
    db = get_mongo('user')
    exist = db.find({'username': username}, {"_id": 0}).limit(1).count()
    if exist > 0:
        return {"error": "user {0} already exists".format(username)}
    db.insert({
        'username': username,
        'password': password
    })
    return {}
