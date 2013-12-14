#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Sat Dec 14 22:36:18 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

from .. import PostfilterBase
from ...api import app

import flask
from flask import request

import re
import os.path


class Plotter(PostfilterBase):
    def _get_name(self):
        return 'plotter'

    def _get_disp_name(self):
        return u'走势曲线图'

    def _get_config_type(self):
        return ['reg_exp', 'tag']

    def enable(self, user_id, config):
        reg_exp = config['reg_exp']
        re.compile(reg_exp)
        config = {'reg_exp': reg_exp,
                  'tag': config['tag']}
        self._save_config(user_id, config)

    def disable(self, user_id):
        self._del_config(user_id)

    def apply(self, ctx, docs):
        conf = self._load_config()
        reobj = re.compile(conf['reg_exp'])
        tag = conf['tag']
        newest_time = None
        idx = 0
        while idx < len(docs):
            cur = docs[idx]
            try:
                assert tag in cur['tag']
                value = float(
                    reobj.match(cur['desc'].render_title() + '\n' +
                                cur['desc'].render_content()).group(1))
            except:
                idx += 1
                continue

            time = cur['creation_time']
            if not newest_time or time > newest_time:
                newest_time = time


@app.route('/postfilter_plotter')
def file_server():
    q = request.values.get('q')

    filemap = {
        'jflot.js': 'jquery.flot.min.js',
        'jquery.js': 'jquery.min.js',
        'jflot.time.js': 'jquery.flot.time.min.js',
        'style.css': 'examples.css'
    }

    fname = filemap.get(q, 'x.html')

    return flask.send_file(
        os.path.join(os.path.dirname(__file__), fname))
