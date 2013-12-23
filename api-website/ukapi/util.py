#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: util.py
# $Date: Mon Dec 23 10:20:13 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from .postfilter import apply_postfilter

from flask_login import current_user, login_required


def get_current_user_id():
    return current_user.username


def parse_article(docs):
    """ parse an item from database,
    return a sorted dict with url, title, content, time"""
    rst = []
    apply_postfilter(get_current_user_id(), docs)
    for doc in docs:
        ret = {}
        ret['time'] = \
            doc['creation_time'].strftime('%Y/%m/%d %H:%M')
        try:
            ret['url'] = doc['other']['id']
        except:
            pass
        item = doc['desc']
        ret['title'] = item.render_title()
        ret['content'] = item.render_content()
        ret['tags'] = doc['tag']
        ret['source'] = doc['fetcher_name']
        rst.append(ret)
        rst = rst[:200]
    return rst
