#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: user.py
# Date: Tue Dec 10 12:09:24 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

"""user operation api"""
from . import api_method, request
from .. import login_manager
from flask_login import login_user, login_required, logout_user, current_user
from ukdbconn import get_mongo, global_counter
from uklogger import log_err

import json

class User(object):
    """User class as implementation required by flask-login"""
    def __init__(self, username, password, need_auth=True):
        self.user = None
        self.error = None
        if need_auth:
            self.authenticate(username, password)
        else:
            self._authenticated = True

    def is_authenticated(self):
        return self._authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user['username']

    def authenticate(self, username, password):
        db = get_mongo('user')
        exist = list(db.find({'username': username}, {"_id": 0}).limit(1))
        if len(exist) == 0:
            self.error = {'error': 'no such user'}
            return
        assert len(exist) == 1, 'More than one user!'
        user = exist[0]
        if user['password'] == password:
            self._authenticated = True
            self.user = user
        else:
            self.error = {'error': 'wrong password'}

    def get_error(self):
        return self.error

    @staticmethod
    def from_doc(user_doc):
        """get User object from a user document from db"""
        u = User(user_doc['username'], user_doc['password'], need_auth=False)
        u.user = user_doc
        return u

@login_manager.user_loader
def load_user(username):
    db = get_mongo('user')
    user = list(db.find({'username': username}, {"_id": 0}).limit(1))
    if len(user) != 1:
        log_err('load_user with username = {0} failed,  \
            found {1} users!'.format(username, len(user)))
        return None
    print user
    return User.from_doc(user[0])

@api_method('/logout')
@login_required
def logout():
    logout_user()
    return {'success': 1}

@api_method('/login', methods=['POST'])
def login():
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
    print 'finish login'
    return {'success': 1}

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

    user_id = global_counter('n_user')
    db.insert({
        'username': username,
        'password': password,
        'uid': user_id
    })
    return {}
