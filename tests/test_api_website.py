#!../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: test_api_website.py
# $Date: Fri Dec 13 02:26:54 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import unittest
import random
import string
import cookielib
from base import APIInterface
from urllib2 import HTTPError


def _random_string(length):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(length))


def _fake_user():
    return {
        'username': 'random_username_' + _random_string(6),
        'password': 'random_password_' + _random_string(6)}


class APITest(unittest.TestCase, APIInterface):

    """a valid user to register"""
    user = {}

    cookie = ''

    def login(self, user=None):
        """Login to api-website.
        If user is not given, login with APITest.user"""
        if not user:
            user = APITest.user
        return self.post('/login', **user)

    def logout(self):
        """Logout api-website"""
        return self.get('/logout')

    def test0_sample(self):
        res = self.get('/sample')
        self.assertEquals(res, dict(answer=42))

    def test1_login_fail(self):
        res = self.login(_fake_user())
        self.assertEquals(res, dict(error='no such user'))

    def test2_login_register(self):
        APITest.user = _fake_user()
        res = self.post('/register', **APITest.user)
        self.assertEquals(res, dict(success=1))

    def test3_login_duplicate_register(self):
        res = self.post('/register', **APITest.user)
        self.assertEquals(res, dict(error='user {} already exists' . format(
            APITest.user['username'])))

    def test4_login_succeed(self):
        self.clear_cookie()
        res = self.login()
        self.assertEquals(res, dict(success=1))

    def test5_logout_succeed(self):
        self.clear_cookie()
        res = self.login()
        res = self.logout()
        self.assertEquals(res, dict(success=1))

    def test6_logout_failed(self):
        try:
            res = self.logout()
        except HTTPError as e:
            assert e.code == 401
        else:
            raise Exception()


def main():
    unittest.main()

if __name__ == '__main__':
    main()
# vim: foldmethod=marker
