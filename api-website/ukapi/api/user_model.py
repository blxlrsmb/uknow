#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: user_model.py
# Date: Tue Dec 10 14:55:26 2013 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from .. import login_manager
from ukdbconn import get_mongo
from uklogger import log_err


class User(object):
    """User class as an implementation required by flask-login"""

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
        """create authenticated User object from a user document from db"""
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
    return User.from_doc(user[0])
