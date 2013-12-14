#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Sun Dec 15 00:39:59 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""mongo doc: collection: plotter_cache
{
    _id: key
    v: value
}
"""

from .. import PostfilterBase
from ...api import app

from ukitem import TextOnlyItem
from ukutil import MongoDBLRUCache

import flask
from flask import request

import re
import os.path
import calendar
import uuid

from cStringIO import StringIO

_cache = MongoDBLRUCache(3600, 'postfilter_plotter_val')


def _render_html(xdata, ydata):
    with open(os.path.join(os.path.dirname(__file__), 'plot.html')) as fin:
        content = fin.read()
    data = '[' + ','.join('[{},{}]'.format(i[0], i[1])
                          for i in zip(xdata, ydata)) + ']'
    content = content. \
        replace('__URL__', '/postfilter_plotter'). \
        replace('__DATA__', data)

    return content


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
        conf = self._load_config(ctx.user_id)
        reobj = re.compile(conf['reg_exp'])
        tag = conf['tag']
        tag_lower = tag.lower()
        doc_newest = None
        idx = 0
        data_x = []
        data_y = []
        while idx < len(docs):
            cur = docs[idx]
            try:
                assert tag_lower in [i.lower() for i in cur['tag']]
                value = float(
                    reobj.match(cur['desc'].render_title() + '\n' +
                                cur['desc'].render_content()).group(1))
            except:
                idx += 1
                continue

            time = cur['creation_time']
            if not doc_newest or time > doc_newest['creation_time']:
                doc_newest = cur

            data_x.append(calendar.timegm(time.utctimetuple()) * 1e3)
            data_y.append(value)

            del docs[idx]

        if doc_newest:
            pageid = str(uuid.uuid4())
            _cache.put(pageid, _render_html(data_x, data_y))
            doc_newest['tag'] = ['plotter-' + tag]
            doc_newest['desc'] = TextOnlyItem(
                u'走势曲线：' + tag,
                """<iframe
                    style="border:none; width:800px; height:600px;"
                    src="/postfilter_plotter?v={}"></iframe>""".
                format(pageid))
            docs.append(doc_newest)


@app.route('/postfilter_plotter')
def file_server():
    v = request.values.get('v')
    fcontent = None
    fsrc = None
    if v:
        fcontent = _cache.get(v, 'not found')
    else:
        q = request.values.get('q')

        filemap = {
            'jflot.js': 'jquery.flot.min.js',
            'jquery.js': 'jquery.min.js',
            'jflot.time.js': 'jquery.flot.time.min.js',
            'jflot.selection.js': 'jquery.flot.selection.min.js'
        }

        fname = filemap.get(q)
        if fname:
            fsrc = os.path.join(os.path.dirname(__file__), fname)
            mimetype = None
    if fsrc is None:
        if fcontent is None:
            fcontent = _render_html(
                range(10**5, 9 * 10**5, 10**4), range(0, 100))
        fsrc = StringIO()
        fsrc.write(fcontent)
        fsrc.seek(0)
        mimetype = 'text/html'
    return flask.send_file(fsrc, mimetype=mimetype)
