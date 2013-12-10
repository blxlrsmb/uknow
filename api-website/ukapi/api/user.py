#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: user.py
# Date: Tue Dec 10 14:55:39 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

"""user operation api"""
from . import api_method, request
from flask_login import login_user, login_required, logout_user
from ukdbconn import get_mongo, global_counter
from user_model import User

import json


@api_method('/logout')
@login_required
def logout():
    """ logout api"""
    logout_user()
    return {'success': 1}


@api_method('/login', methods=['POST'])
def login():
    """login api"""
    postdata = json.loads(request.data)
    try:
        username = postdata['username']
        password = postdata['password']
        assert isinstance(username, basestring) \
            and isinstance(password, basestring)
    except Exception as e:
        return {'error': 'wrong login format!' + str(e)}

    auth = User(username, password)
    err = auth.get_error()
    if err:
        return err
    login_user(auth)
    return {'success': 1}


@api_method('/register', methods=['POST'])
def register():
    """user registration api.
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

    user_id = global_counter('n_user')
    db.insert({
        'username': username,
        'password': password,
        'uid': user_id
    })
    return {}
