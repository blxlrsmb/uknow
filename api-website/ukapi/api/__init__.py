#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Thu Dec 12 15:17:12 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""website API entry points"""
from .. import _app as app

from flask import Response, request

import json
import re


@app.errorhandler(404)
def page_not_found(_):
    return Response('{"error": "API not found"}', 404,
                    mimetype='application/json')

VALID_CALLBACK_RE = re.compile('^[$A-Za-z_][0-9A-Za-z_$.]*$')


class api_method(object):
    """use as a decorator to register an API"""
    all_url_rule = list()
    """class level attribute for all url rules"""

    url_rule = None
    """url rule for current API"""

    api_implementation = None
    """a callable implementing current API, which takes no argument and
    returns a dict"""

    url_rule_extra_kwargs = None
    """extra keyword arguments for url rule"""

    def __init__(self, url_rule, **kwargs):
        self.url_rule = url_rule
        self.url_rule_extra_kwargs = kwargs
        if 'methods' in self.url_rule_extra_kwargs and 'POST' in self.url_rule_extra_kwargs['methods']:
            self.url_rule_extra_kwargs['methods'].append('OPTIONS')

    def __call__(self, func):
        self.api_implementation = func
        endpoint = func.__module__ + '.' + func.__name__

        app.add_url_rule(self.url_rule,
                         view_func=self.view_func,
                         endpoint=endpoint, **self.url_rule_extra_kwargs)

        return func

    def view_func(self):
        """the view_func passed to Flask.add_url_rule"""
        if request.method == 'OPTIONS':
            resp = Response('', 200)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Origin, Accept'
            return resp
        rst = self.api_implementation()
        assert isinstance(rst, dict), \
            "ret value {0} is not a dict".format(str(rst))
        callback = request.values.get('callback')
        if callback and VALID_CALLBACK_RE.match(callback) is not None:
            rst = '{}({})'.format(callback, json.dumps(rst))
        else:
            rst = json.dumps(rst, indent=4)
        resp = Response(rst, 200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Origin, Accept'
        return resp
