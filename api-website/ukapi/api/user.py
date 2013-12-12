#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: user.py
# Date: Fri Dec 13 00:25:09 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

"""user operation api"""
from . import api_method, request
from flask_login import login_user, login_required, logout_user, current_user
from ukdbconn import get_mongo, get_user
from user_model import User
from uklogger import log_api as log_info

import json


@api_method('/logout')
@login_required
def logout():
    """ logout api"""
    log_info('user {0} logged out'.format(current_user.username))
    logout_user()
    return {'success': 1}


@api_method('/test_login')
@login_required
def test_login():
    """test if a cookie is valid"""
    return {'success': 1}


@api_method('/login', methods=['POST'])
def login():
    """login api"""
    try:
        postdata = json.loads(request.data)
        username = postdata['username']
        password = postdata['password']
        assert isinstance(username, basestring) \
            and isinstance(password, basestring)
    except Exception as e:
        return {'error': 'illegal login format!' + str(e)}

    auth = User(username, password)
    err = auth.get_error()
    if err:
        return err
    login_user(auth)
    log_info('user {0} succesfully logged in'.format(username))
    return {'success': 1}


@api_method('/register', methods=['POST', 'OPTIONS'])
def register():
    """user registration api.
        username: string
        password: string        XXX TODO

    """
    try:
        postdata = json.loads(request.data)
        assert 'username' in postdata and 'password' in postdata,\
            'no username or password in register()'
        username = postdata['username']
        password = postdata['password']
        assert isinstance(username, basestring)
        assert isinstance(password, basestring)
    except:
        return {'error': 'illegal format'}
    if len(username) < 3 or len(password) < 3:
        return {'error':
                'length of username and password must \
                be at least 3 characters'}

    exist = get_user(username)
    if exist:
        return {"error": "user {0} already exists".format(username)}

    db = get_mongo('user')
    db.insert({
        'username': username,
        'password': password,
        'tab': []
    })
    log_info('new user: {0}:{1}'.format(username, password))
    return {'success': 1}
