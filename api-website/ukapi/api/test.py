#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: test.py
# $Date: Wed Nov 13 01:27:23 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""test with user id"""

from . import api_method, request

from ukfetcher import get_user_fetcher_celery_task
from ukdbconn import get_mongo
from datetime import datetime

@api_method('/test')
def test():
    """given user id and return all items"""
    uid = request.values.get('uid')
    if not uid:
        return {'error': 'please visit with uid=1'}
    t = get_user_fetcher_celery_task()
    t(uid)
    data = list(get_mongo('item').find())
    def chg(d):
        for k, v in d.iteritems():
            if isinstance(v, datetime):
                d[k] = str(v)
    map(chg, data)
    return {'data': data}


