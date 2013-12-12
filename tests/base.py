#!/usr/bin/python2
# -*- coding: utf-8 -*-
# $File: base.py
# $Date: Fri Dec 13 02:24:17 2013 +0800
# $Author: Xinyu Zhou <zxytim[at]gmail[dot]com>

"""API webiste test case base"""

import urllib
import urllib2
import cookielib
import json
import config

API_PORT = config.API_PORT
API_HOST = 'localhost'
PROTOCOL = 'http'


class APIInterface(object):
    url_base = "{}://{}:{}" . format(PROTOCOL, API_HOST, API_PORT)

    urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(
        cookielib.CookieJar()))

    def clear_cookie(self):
        self.urlopener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

    def get(self, url, **kwargs):
        """a GET request to url with data.
        url is a location relative to root, e.g '/sample'
        return: json data"""
        url = self._get_url(url, kwargs)
        response = self.urlopener.open(url)
        return json.loads(response.read())

    def post(self, url, **kwargs):
        """a POST request to url with data.
        url is a location relative to root, e.g '/add_tab'
        return: json data
        """
        req = urllib2.Request(
            self._url(url), json.dumps(kwargs),
            {'Content-Type': 'application/json'})

        response = self.urlopener.open(req)
        return json.loads(response.read())

    def _url(self, url):
        return self.url_base + url

    def _get_url(self, url, data={}):
        if len(data):
            url = url + '?' + urllib.urlencode(data)
        return self._url(url)



# vim: foldmethod=marker
