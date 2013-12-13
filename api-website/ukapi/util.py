#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: util.py
# $Date: Fri Dec 13 13:43:01 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from flask_login import current_user, login_required
from ukitem import ItemDescBase


def get_current_user_id():
    return current_user.username


def parse_article(docs):
    """ parse an item from database,
    return a sorted dict with url, title, content, time"""
    rst = []
    docs.sort(key=lambda x: x['creation_time'], reverse=True)
    for doc in docs:
        ret = {}
        ret['time'] = \
            doc['creation_time'].strftime('%Y/%m/%d %H:%M')
        try:
            ret['url'] = doc['other']['id']
        except:
            pass
        item = ItemDescBase.deserialize(doc['desc'])
        ret['title'] = item.render_title()
        ret['content'] = item.render_content()
        ret['tags'] = doc['tag']
        rst.append(ret)
    return rst
