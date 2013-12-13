#!../manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: test_api_website.py
# $Date: Fri Dec 13 16:10:36 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

import unittest
import random
import string
import cookielib
from interface import APIInterface
from urllib2 import HTTPError
from functools import wraps


def _random_string(length):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(length))


def _fake_user():
    return {
        'username': 'random_username_' + _random_string(6),
        'password': 'random_password_' + _random_string(6)}


class APITestBase(APIInterface):

    """a valid user to register"""
    user = {}

    cookie = ''

    NR_TEST_TABS = 10

    def assertSucceed(self, res):
        self.assertEquals(res, dict(success=1))

    def assertError(self, res, error_msg):
        self.assertEquals(res, dict(error=error_msg))

    def login(self, user=None):
        """Login to api-website.
        If user is not given, login with APITestBase.user"""
        if not user:
            user = APITestBase.user
        return self.get('/login', **user)

    def logout(self):
        """Logout api-website"""
        return self.get('/logout')

    def login_required(user):
        """decorator to login before proceeding"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.clear_cookie()
                self.login(user)
                return func(*args, **kwargs)
            return wrapper
        return decorator


class LoginTest(unittest.TestCase, APITestBase):

    def test000_sample(self):
        res = self.get('/sample')
        self.assertEquals(res, dict(answer=42))

    def test001_login_fail(self):
        res = self.login(_fake_user())
        self.assertEquals(res, dict(error='no such user'))

    def test002_login_register(self):
        APITestBase.user = _fake_user()
        res = self.get('/register', **APITestBase.user)
        self.assertSucceed(res)

    def test003_login_duplicate_register(self):
        res = self.get('/register', **APITestBase.user)
        self.assertEquals(res, dict(error='user {} already exists' . format(
            APITestBase.user['username'])))

    def test004_login_succeed(self):
        self.clear_cookie()
        res = self.login()
        self.assertSucceed(res)

    def test005_logout_succeed(self):
        self.clear_cookie()
        res = self.login()
        res = self.logout()
        self.assertSucceed(res)

    def test006_logout_failed(self):
        self.clear_cookie()
        try:
            res = self.logout()
        except HTTPError as e:
            assert e.code == 401
        else:
            raise Exception()

    def test007_login_incorrect_password(self):
        self.clear_cookie()
        self.assertError(
            self.login(dict(username=APITestBase.user['username'],
                            password=_random_string(100))),
            'wrong password')

    def test008_login_illegal_format(self):
        self.clear_cookie()
        self.assertError(
            self.login(dict(hello=1, world=2)),
            'illegal login format!400: Bad Request')

    def test009_login_register_illegal_format(self):
        self.clear_cookie()
        res = self.get('/register', hello='world')
        self.assertError(res, 'illegal format')

    def test010_login_register_length_too_short(self):
        self.clear_cookie()
        error_msg = 'length of username and password must be at least ' + \
            '3 characters'
        res = self.get('/register', username='a', password='b')
        self.assertError(res, error_msg)
        res = self.get('/register', username='a', password='bbbb')
        self.assertError(res, error_msg)
        res = self.get('/register', username='aaaa', password='b')
        self.assertError(res, error_msg)

    def test099_testlogin(self):
        self.clear_cookie()
        self.login()
        self.assertSucceed(self.get('/test_login', **APITestBase.user))
        self.clear_cookie()


class TabTest(unittest.TestCase, APITestBase):
    def test100_tab_add_fail(self):
        self.clear_cookie()
        try:
            res = self.post('/add_tab', name='tab2', priority=1)
        except HTTPError as e:
            assert e.code == 401
        else:
            raise Exception()

    def test101_tab_add(self):
        self.clear_cookie()
        self.login()
        for i in range(self.NR_TEST_TABS):
            self.assertSucceed(self.post(
                '/add_tab', name='tab{}'.format(i), priority=1))
        for i in range(self.NR_TEST_TABS):
            self.assertError(self.post(
                '/add_tab', name='tab{}'.format(i), priority=1),
                'tab with this name already exists!')

    def test102_tab_getall(self):
        self.clear_cookie()
        self.login()
        res = self.get('/get_all_tabs')
        self.assertTrue('tabs' in res)
        self.assertEqual(len(res['tabs']), 10)

    def test103_tab_get(self):
        self.clear_cookie()
        self.login()
        for i in range(self.NR_TEST_TABS):
            res = self.get('/get_tab_article', tab='tab{}' .format(i))
            self.assertEqual(res, {'data': []})

    def test104_tab_del(self):
        self.clear_cookie()
        self.login()
        for i in range(self.NR_TEST_TABS):
            self.assertSucceed(self.post('/del_tab', name='tab{}' .format(i)))
            res = self.get('/get_all_tabs')
            self.assertEqual(len(res['tabs']), self.NR_TEST_TABS - i - 1)

        for i in range(self.NR_TEST_TABS):
            # if tab does not exists, api ignores it
            self.assertSucceed(self.post('/del_tab', name='tab{}' .format(i)))


class TagTest(unittest.TestCase, APITestBase):

    TEST_TAB_NAME = 'tagtest_tab'
    TEST_TAG_NAME = 'tagtest_tag'

    NR_TEST_TAGS = 10

    def test200_add_tab(self):
        self.clear_cookie()
        self.login()
        self.assertSucceed(self.post(
            '/add_tab', name=self.TEST_TAB_NAME,
            priority=1))

    def test201_add_tag(self):
        self.clear_cookie()
        self.login()
        for i in range(self.NR_TEST_TAGS):
            tagname = self.TEST_TAG_NAME+str(i)
            res = self.post(
                '/add_tag', name=tagname,
                tab=self.TEST_TAB_NAME, priority=1)
            self.assertTrue('tabs' in res)
            self.assertTrue(isinstance(res['tabs'], list))
            self.assertEqual(len(res['tabs']), 1)
            self.assertTrue('tags' in res['tabs'][0])
            self.assertEqual(len(res['tabs'][0]['tags']), i + 1)
            self.assertTrue(tagname in res['tabs'][0]['tags'])

    #def test202_get_tag(self):
        #self.clear_cookie()
        #self.login()
        #res = self.get('/get_tag_article', tag=self.TEST_TAG_NAME + '0')
        #self.assertEqual(res, dict(data=[]))  # nothing here

    def test203_del_tag(self):
        self.clear_cookie()
        self.login()
        for i in range(self.NR_TEST_TAGS):
            tagname = self.TEST_TAG_NAME+str(i)
            res = self.get(
                '/del_tag', name=tagname,
                tab=self.TEST_TAB_NAME)
            self.assertTrue('tabs' in res)
            self.assertTrue(isinstance(res['tabs'], list))
            self.assertEqual(len(res['tabs']), 1)
            self.assertTrue('tags' in res['tabs'][0])
            self.assertEqual(
                len(res['tabs'][0]['tags']),
                self.NR_TEST_TAGS - i - 1)

            # tags that are not removed
            for j in range(i + 1, self.NR_TEST_TAGS):
                tagname = self.TEST_TAG_NAME+str(j)
                self.assertTrue(tagname in res['tabs'][0]['tags'])

    def test204_add_tag_error(self):
        self.clear_cookie()
        self.login()
        self.assertError(
            self.post('/add_tag', hello='world'), 'illegal format')
        self.assertError(
            self.post('/add_tag', name=self.TEST_TAG_NAME,
                      tab='hello-world-this-is-an-non-existent-tab'),
            'no such tab')

    def test205_set_tag(self):
        self.clear_cookie()
        self.login()
        tagname = self.TEST_TAG_NAME + str(self.NR_TEST_TAGS)
        newtabname = self.TEST_TAB_NAME + 'new'

        self.post('/add_tag', name=tagname, tab=self.TEST_TAB_NAME)
        self.post('/add_tab', name=newtabname)

        self.assertError(
            self.post('/set_tag', hello='world'), 'illegal format')

        res = self.post('/set_tag', name=[tagname], tab=newtabname)
        self.assertTrue('tabs' in res)
        self.assertTrue(type(res['tabs']) == list)

#        self.assertError(self.get('/del_tag', name=tagname,
#            tab=self.TEST_TAB_NAME), 'no such tab')
        res = self.get('/del_tag', name=tagname, tab=newtabname)
        self.assertTrue('tabs' in res)
        self.assertTrue(isinstance(res['tabs'], list))
        self.assertError(
            self.get('/del_tag', name=tagname, tab='nonsense'),
            'no such tab')

        self.assertSucceed(self.post('/del_tab', name=newtabname))

    def test299_del_tab(self):
        self.clear_cookie()
        self.login()
        self.assertSucceed(self.post('/del_tab', name=self.TEST_TAB_NAME))


class MiscTest(unittest.TestCase, APITestBase):

    def test900_test_test(self):
        self.assertError(self.get('/test'), 'please visit with uid=1')
        res = self.get('/test', uid=1)
        self.assertTrue(type(res) == dict)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
# vim: foldmethod=marker
